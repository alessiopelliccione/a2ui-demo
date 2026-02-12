# Generic UI Builder - Main Entry Point
# Demo for Generative Frontend / Server-Driven UI session

import logging
import os
import sys

# Add lib directory to path for local a2ui module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import click
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2ui.extension import get_a2ui_agent_extension
from agent import UIBuilderAgent
from agent_executor import UIBuilderAgentExecutor
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=10003)
def main(host, port):
    try:
        # Check for API key
        if not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
            if not os.getenv("GEMINI_API_KEY"):
                raise MissingAPIKeyError(
                    "GEMINI_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
                )

        capabilities = AgentCapabilities(
            streaming=True,
            extensions=[get_a2ui_agent_extension()],
        )

        skill = AgentSkill(
            id="build_ui",
            name="Generic UI Builder",
            description="Creates any type of UI from natural language descriptions using A2UI.",
            tags=["ui", "builder", "generator", "a2ui"],
            examples=[
                "Create a headline for an insurance company",
                "Build a KPI dashboard with user metrics",
                "Make a comparison table between Product A and Product B",
                "Generate a contact form",
                "Add a stepper for user onboarding",
            ],
        )

        base_url = f"http://{host}:{port}"

        agent_card = AgentCard(
            name="UI Builder Agent",
            description="A generic UI builder that creates rich, interactive interfaces from natural language using A2UI. Perfect for demos of Generative Frontend / Server-Driven UI.",
            url=base_url,
            version="1.0.0",
            default_input_modes=UIBuilderAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=UIBuilderAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        agent_executor = UIBuilderAgentExecutor()

        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
        )

        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        import uvicorn

        app = server.build()

        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=r"http://localhost:\d+",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        logger.info(f"Starting UI Builder Agent on {base_url}")
        logger.info("Demo commands to try:")
        logger.info("  - 'Create a headline for my startup'")
        logger.info("  - 'Build a KPI dashboard'")
        logger.info("  - 'Make a comparison table'")
        logger.info("  - 'Add a contact form'")

        uvicorn.run(app, host=host, port=port)

    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    main()
