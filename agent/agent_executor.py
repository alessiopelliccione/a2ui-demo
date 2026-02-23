# Generic UI Builder Agent Executor
# Demo for Generative Frontend / Server-Driven UI session

import json
import logging
import os
import sys

# Add lib directory to path for local a2ui module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    DataPart,
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_parts_message,
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError
from a2ui.extension import create_a2ui_part, try_activate_a2ui_extension
from agent import UIBuilderAgent

logger = logging.getLogger(__name__)


class UIBuilderAgentExecutor(AgentExecutor):
    """Generic UI Builder AgentExecutor."""

    def __init__(self):
        # Instantiate two agents: one for UI and one for text-only
        self.ui_agent = UIBuilderAgent(use_ui=True)
        self.text_agent = UIBuilderAgent(use_ui=False)

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = ""
        ui_event_part = None
        action = None

        logger.info(f"Client requested extensions: {context.requested_extensions}")
        use_ui = try_activate_a2ui_extension(context)

        if use_ui:
            agent = self.ui_agent
            logger.info("A2UI extension active. Using UI agent.")
        else:
            agent = self.text_agent
            logger.info("A2UI extension not active. Using text agent.")

        # Process message parts
        if context.message and context.message.parts:
            logger.info(f"Processing {len(context.message.parts)} message parts")
            for i, part in enumerate(context.message.parts):
                if isinstance(part.root, DataPart):
                    if "userAction" in part.root.data:
                        logger.info(f"Part {i}: Found A2UI UI ClientEvent payload.")
                        ui_event_part = part.root.data["userAction"]
                    else:
                        logger.info(f"Part {i}: DataPart (data: {part.root.data})")
                elif isinstance(part.root, TextPart):
                    logger.info(f"Part {i}: TextPart (text: {part.root.text})")
                else:
                    logger.info(f"Part {i}: Unknown part type ({type(part.root)})")

        # Handle UI events (button clicks, form submissions, etc.)
        if ui_event_part:
            logger.info(f"Received A2UI ClientEvent: {ui_event_part}")
            # The client sends 'name', not 'actionName'
            action = ui_event_part.get("name")
            ctx = ui_event_part.get("context", {})

            # Generic handling of UI events
            if action == "cta_click":
                query = "The user clicked the main CTA button. Acknowledge this and show a success message or a next step UI (like a sign-up form)."
            elif action == "submit_form":
                form_data = json.dumps(ctx)
                query = f"User submitted form with data: {form_data}. Confirm receipt and show a thank you message or a success state."
            elif action == "select_product":
                product = ctx.get("product", "Unknown")
                query = f"User selected product: {product}. Display detailed specifications and an 'Order Now' button for this product."
            elif action == "view_item":
                item_id = ctx.get("itemId", "Unknown")
                query = f"User wants to view item with ID: {item_id}. Generate a detailed item view."
            elif action == "complete_wizard":
                query = "User completed the wizard. Show a celebration/completion UI with next steps."
            else:
                query = f"The user interacted with the UI element '{action}' with data {ctx}. Respond appropriately by updating the UI."
        else:
            logger.info("No A2UI UI event part found. Using text input.")
            query = context.get_user_input()

        logger.info(f"Final query for LLM: '{query}'")

        task = context.current_task

        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)

        async for item in agent.stream(query, task.context_id):
            is_task_complete = item["is_task_complete"]
            if not is_task_complete:
                await updater.update_status(
                    TaskState.working,
                    new_agent_text_message(item["updates"], task.context_id, task.id),
                )
                continue

            # For UI builder, always stay in input_required state to allow more interactions
            final_state = TaskState.input_required

            content = item["content"]
            final_parts = []

            if "---a2ui_JSON---" in content:
                logger.info("Splitting final response into text and UI parts.")
                text_content, json_string = content.split("---a2ui_JSON---", 1)

                if text_content.strip():
                    final_parts.append(Part(root=TextPart(text=text_content.strip())))

                if json_string.strip():
                    try:
                        json_string_cleaned = (
                            json_string.strip().lstrip("```json").rstrip("```").strip()
                        )
                        json_data = json.loads(json_string_cleaned)

                        if isinstance(json_data, list):
                            logger.info(f"Found {len(json_data)} messages. Creating individual DataParts.")
                            for message in json_data:
                                final_parts.append(create_a2ui_part(message))
                        else:
                            logger.info("Received single JSON object. Creating DataPart.")
                            final_parts.append(create_a2ui_part(json_data))

                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse UI JSON: {e}")
                        final_parts.append(Part(root=TextPart(text=json_string)))
            else:
                final_parts.append(Part(root=TextPart(text=content.strip())))

            logger.info("--- FINAL PARTS TO BE SENT ---")
            for i, part in enumerate(final_parts):
                logger.info(f"  - Part {i}: Type = {type(part.root)}")
                if isinstance(part.root, TextPart):
                    logger.info(f"    - Text: {part.root.text[:200]}...")
                elif isinstance(part.root, DataPart):
                    logger.info(f"    - Data: {str(part.root.data)[:200]}...")
            logger.info("-----------------------------")

            await updater.update_status(
                final_state,
                new_agent_parts_message(final_parts, task.context_id, task.id),
                final=False,  # Always allow more interactions
            )
            break

    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
