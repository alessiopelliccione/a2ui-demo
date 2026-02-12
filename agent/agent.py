# Generic UI Builder Agent
# Demo for Generative Frontend / Server-Driven UI session

import json
import logging
import os
from collections.abc import AsyncIterable
from typing import Any

import jsonschema
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from prompt_builder import A2UI_SCHEMA, get_text_prompt, get_ui_prompt
from a2ui_examples import UI_BUILDER_EXAMPLES

logger = logging.getLogger(__name__)

AGENT_INSTRUCTION = """
You are a Generic UI Builder assistant. Your goal is to help users create any kind of UI
by generating A2UI JSON that renders rich, interactive interfaces.

You can create:
- Headlines and hero sections for landing pages
- KPI dashboards with metrics and statistics
- Comparison tables with pros and cons
- Forms with various input fields
- Steppers and wizards for onboarding flows
- Lists with images and cards
- Any combination of the above

When the user describes what they want, analyze their request and:
1. Choose the most appropriate UI pattern from the examples
2. Customize the content based on their specific needs
3. Generate valid A2UI JSON that renders the requested UI

If the user asks to modify an existing UI:
- Keep the same surfaceId
- Update only the components or data that need to change
- Explain what changes you made

Be creative but always ensure the JSON is valid according to the A2UI schema.
"""


class UIBuilderAgent:
    """A generic UI Builder agent that creates any type of UI using A2UI."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self, use_ui: bool = False):
        self.use_ui = use_ui
        self._agent = self._build_agent(use_ui)
        self._user_id = "ui_builder_user"
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

        # Load and wrap the schema for validation
        try:
            single_message_schema = json.loads(A2UI_SCHEMA)
            self.a2ui_schema_object = {"type": "array", "items": single_message_schema}
            logger.info("A2UI_SCHEMA successfully loaded.")
        except json.JSONDecodeError as e:
            logger.error(f"CRITICAL: Failed to parse A2UI_SCHEMA: {e}")
            self.a2ui_schema_object = None

    def get_processing_message(self) -> str:
        return "Generating your UI..."

    def _build_agent(self, use_ui: bool) -> LlmAgent:
        """Builds the LLM agent for the UI builder.

        Supported models via LiteLLM:
        - Gemini: gemini/gemini-2.5-flash, gemini/gemini-2.5-pro, gemini/gemini-1.5-pro
        - OpenAI: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo
        - Anthropic: claude-3-5-sonnet-20241022, claude-3-opus-20240229
        - Azure: azure/gpt-4o, azure/gpt-4
        - And many more: https://docs.litellm.ai/docs/providers

        Set via environment variable:
        - LITELLM_MODEL=gpt-4o (for OpenAI)
        - LITELLM_MODEL=gemini/gemini-2.5-flash (for Gemini)
        - LITELLM_MODEL=claude-3-5-sonnet-20241022 (for Anthropic)
        """
        # Default to Gemini, but easily switchable via env var
        LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gemini/gemini-2.5-flash")

        logger.info(f"Using LLM model: {LITELLM_MODEL}")

        if use_ui:
            instruction = AGENT_INSTRUCTION + get_ui_prompt(UI_BUILDER_EXAMPLES)
        else:
            instruction = get_text_prompt()

        return LlmAgent(
            model=LiteLlm(model=LITELLM_MODEL),
            name="ui_builder_agent",
            description="A generic UI builder that creates rich interfaces from natural language.",
            instruction=instruction,
            tools=[],  # No external tools needed - pure UI generation
        )

    async def stream(self, query, session_id) -> AsyncIterable[dict[str, Any]]:
        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )
        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )

        # Validation and retry logic
        max_retries = 1
        attempt = 0
        current_query_text = query

        if self.use_ui and self.a2ui_schema_object is None:
            logger.error("A2UI_SCHEMA is not loaded. Cannot perform UI validation.")
            yield {
                "is_task_complete": True,
                "content": "Internal configuration error. Please contact support.",
            }
            return

        while attempt <= max_retries:
            attempt += 1
            logger.info(f"UI Builder: Attempt {attempt}/{max_retries + 1} for session {session_id}")

            current_message = types.Content(
                role="user", parts=[types.Part.from_text(text=current_query_text)]
            )
            final_response_content = None

            async for event in self._runner.run_async(
                user_id=self._user_id,
                session_id=session.id,
                new_message=current_message,
            ):
                logger.info(f"Event from runner: {event}")
                if event.is_final_response():
                    if (
                        event.content
                        and event.content.parts
                        and event.content.parts[0].text
                    ):
                        final_response_content = "\n".join(
                            [p.text for p in event.content.parts if p.text]
                        )
                    break
                else:
                    yield {
                        "is_task_complete": False,
                        "updates": self.get_processing_message(),
                    }

            if final_response_content is None:
                logger.warning(f"No final response content (Attempt {attempt})")
                if attempt <= max_retries:
                    current_query_text = f"Please retry: '{query}'"
                    continue
                else:
                    final_response_content = "Sorry, I couldn't process your request."

            is_valid = False
            error_message = ""

            if self.use_ui:
                logger.info(f"Validating UI response (Attempt {attempt})...")
                try:
                    if "---a2ui_JSON---" not in final_response_content:
                        raise ValueError("Delimiter '---a2ui_JSON---' not found.")

                    text_part, json_string = final_response_content.split(
                        "---a2ui_JSON---", 1
                    )

                    if not json_string.strip():
                        raise ValueError("JSON part is empty.")

                    json_string_cleaned = (
                        json_string.strip().lstrip("```json").rstrip("```").strip()
                    )

                    if not json_string_cleaned:
                        raise ValueError("Cleaned JSON string is empty.")

                    parsed_json_data = json.loads(json_string_cleaned)

                    logger.info("Validating against A2UI_SCHEMA...")
                    jsonschema.validate(
                        instance=parsed_json_data, schema=self.a2ui_schema_object
                    )

                    logger.info(f"UI JSON validated successfully (Attempt {attempt})")
                    is_valid = True

                except (
                    ValueError,
                    json.JSONDecodeError,
                    jsonschema.exceptions.ValidationError,
                ) as e:
                    logger.warning(f"A2UI validation failed: {e} (Attempt {attempt})")
                    error_message = f"Validation failed: {e}."
            else:
                is_valid = True

            if is_valid:
                logger.info(f"Response valid. Sending final response (Attempt {attempt})")
                yield {
                    "is_task_complete": True,
                    "content": final_response_content,
                }
                return

            if attempt <= max_retries:
                logger.warning(f"Retrying... ({attempt}/{max_retries + 1})")
                current_query_text = (
                    f"Your previous response was invalid. {error_message} "
                    "Generate a valid A2UI JSON response. "
                    f"Original request: '{query}'"
                )

        logger.error("Max retries exhausted. Sending text-only error.")
        yield {
            "is_task_complete": True,
            "content": "Sorry, I'm having trouble generating the UI. Please try again.",
        }
