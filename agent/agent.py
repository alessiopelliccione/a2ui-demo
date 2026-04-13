# Insurance Assistant Agent
# Template-based architecture: AI picks templates, Python generates A2UI.

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

from prompt_builder import A2UI_SCHEMA, get_text_prompt, get_template_prompt
from a2ui_templates import render_template

logger = logging.getLogger(__name__)

AGENT_INSTRUCTION = """
You are an Insurance Assistant — a friendly, professional AI agent helping customers
with their insurance needs. You speak naturally and conversationally, like a real
insurance advisor.

YOUR ROLE:
- Help customers explore insurance policies (auto, home, health, life)
- Compare plans and coverage options side by side
- Guide them through filing claims step by step
- Answer questions about premiums, deductibles, and coverage
- Help create or modify insurance plans
- Show portfolio dashboards with policy status and KPIs

HOW YOU RESPOND:
- Always be helpful, clear, and empathetic
- When the user asks about policies, comparisons, or claims, use a template to show interactive UI
- When the user asks a simple question, just answer conversationally without a template
- When responding to a USER ACTION (button click, form submission), you MUST ALWAYS include a template to update the interface. The user sees a split screen: chat on the left, interactive canvas on the right. If you respond text-only to an action, the canvas stays stale. Always update it.
- After a form submission, show a confirmation/summary using info_list or dashboard — NEVER re-show the same form
- Use realistic insurance data and terminology
- Proactively suggest next steps ("Would you like to compare plans?" or "I can help you file a claim")

KNOWLEDGE:
- You work for a modern insurance company
- You know about auto, home, health, and life insurance products
- Premium ranges, deductible options, and coverage tiers are realistic
- The tech conference called "Basta" should be referred to as "Basta conference" with website "basta.net"
"""


class UIBuilderAgent:
    """Insurance assistant that uses templates for UI generation."""

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

        # Load schema for optional validation of template output
        try:
            single_message_schema = json.loads(A2UI_SCHEMA)
            self.a2ui_schema_object = {"type": "array", "items": single_message_schema}
            logger.info("A2UI_SCHEMA successfully loaded.")
        except json.JSONDecodeError as e:
            logger.error(f"CRITICAL: Failed to parse A2UI_SCHEMA: {e}")
            self.a2ui_schema_object = None

    def get_processing_message(self) -> str:
        return "Generating your response..."

    def _build_agent(self, use_ui: bool) -> LlmAgent:
        """Builds the LLM agent.

        Supported models via LiteLLM:
        - Gemini: gemini/gemini-2.5-flash, gemini/gemini-2.5-pro
        - OpenAI: gpt-4o, gpt-4o-mini
        - Anthropic: claude-3-5-sonnet-20241022
        Set via LITELLM_MODEL env var.
        """
        LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gemini/gemini-2.5-flash")
        logger.info(f"Using LLM model: {LITELLM_MODEL}")

        if use_ui:
            instruction = AGENT_INSTRUCTION + get_template_prompt()
        else:
            instruction = get_text_prompt()

        return LlmAgent(
            model=LiteLlm(model=LITELLM_MODEL),
            name="ui_builder_agent",
            description="An insurance assistant that creates rich interfaces from templates.",
            instruction=instruction,
            tools=[],
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

        max_retries = 1
        attempt = 0
        current_query_text = query

        while attempt <= max_retries:
            attempt += 1
            logger.info(f"Attempt {attempt}/{max_retries + 1} for session {session_id}")

            current_message = types.Content(
                role="user", parts=[types.Part.from_text(text=current_query_text)]
            )
            final_response_content = None

            # ── LLM call with retry on failure ──
            try:
                async for event in self._runner.run_async(
                    user_id=self._user_id,
                    session_id=session.id,
                    new_message=current_message,
                ):
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
            except Exception as e:
                logger.error(f"LLM call failed (Attempt {attempt}): {e}")
                if attempt <= max_retries:
                    current_query_text = f"Please retry: '{query}'"
                    continue
                else:
                    yield {
                        "is_task_complete": True,
                        "content": json.dumps({"message": "Sorry, I'm having trouble right now. Please try again."}),
                    }
                    return

            if final_response_content is None:
                logger.warning(f"No final response content (Attempt {attempt})")
                if attempt <= max_retries:
                    current_query_text = f"Please retry: '{query}'"
                    continue
                else:
                    yield {
                        "is_task_complete": True,
                        "content": json.dumps({"message": "Sorry, I couldn't process your request."}),
                    }
                    return

            # ── Parse and process response ──
            is_valid = False
            error_message = ""

            if self.use_ui:
                try:
                    json_string_cleaned = (
                        final_response_content.strip()
                        .lstrip("```json").lstrip("```")
                        .rstrip("```").strip()
                    )
                    if not json_string_cleaned:
                        raise ValueError("Cleaned JSON string is empty.")

                    parsed = json.loads(json_string_cleaned)

                    if not isinstance(parsed, dict):
                        raise ValueError("Response must be a JSON object.")

                    # ── Template rendering ──
                    template_name = parsed.get("template")
                    if template_name:
                        logger.info(f"Rendering template: {template_name}")
                        a2ui_messages = render_template(
                            template_name, parsed.get("data", {})
                        )
                        if a2ui_messages:
                            parsed = {
                                "message": parsed.get("message", ""),
                                "ui": a2ui_messages,
                            }
                            logger.info(f"Template '{template_name}' rendered {len(a2ui_messages)} A2UI messages.")
                        else:
                            logger.warning(f"Template '{template_name}' returned None, falling back to text-only.")
                            parsed = {"message": parsed.get("message", "")}

                    # ── Validate A2UI output (if present) ──
                    if "ui" in parsed and self.a2ui_schema_object:
                        ui_array = parsed["ui"]
                        if not isinstance(ui_array, list):
                            raise ValueError("'ui' field must be an array.")
                        jsonschema.validate(
                            instance=ui_array, schema=self.a2ui_schema_object
                        )
                        logger.info("A2UI validation passed.")

                    # Must have at least a message
                    if "message" not in parsed:
                        raise ValueError("Response must have a 'message' field.")

                    is_valid = True
                    final_response_content = json.dumps(parsed)

                except (
                    ValueError,
                    json.JSONDecodeError,
                    jsonschema.exceptions.ValidationError,
                ) as e:
                    logger.warning(f"Validation failed (Attempt {attempt}): {e}")
                    error_message = f"Validation failed: {e}."
            else:
                is_valid = True

            if is_valid:
                logger.info(f"Response valid (Attempt {attempt}). Sending.")
                yield {
                    "is_task_complete": True,
                    "content": final_response_content,
                }
                return

            if attempt <= max_retries:
                logger.warning(f"Retrying... ({attempt}/{max_retries + 1})")
                current_query_text = (
                    f"Your previous response was invalid JSON. {error_message} "
                    f"Please respond with valid JSON. Original request: '{query}'"
                )

        logger.error("Max retries exhausted.")
        yield {
            "is_task_complete": True,
            "content": json.dumps({"message": "Sorry, I'm having trouble generating a response. Please try again."}),
        }
