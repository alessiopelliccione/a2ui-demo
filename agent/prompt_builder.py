# Generic UI Builder Prompt Builder
# Demo for Generative Frontend / Server-Driven UI session

from a2ui_examples import UI_BUILDER_EXAMPLES

# The A2UI schema - copied from the A2UI framework for standalone usage
A2UI_SCHEMA = r'''
{
  "title": "A2UI Message Schema",
  "description": "Describes a JSON payload for an A2UI (Agent to UI) message.",
  "type": "object",
  "properties": {
    "beginRendering": {
      "type": "object",
      "description": "Signals the client to begin rendering a surface.",
      "properties": {
        "surfaceId": { "type": "string" },
        "root": { "type": "string" },
        "styles": {
          "type": "object",
          "properties": {
            "font": { "type": "string" },
            "primaryColor": { "type": "string", "pattern": "^#[0-9a-fA-F]{6}$" }
          }
        }
      },
      "required": ["root", "surfaceId"]
    },
    "surfaceUpdate": {
      "type": "object",
      "description": "Updates a surface with components.",
      "properties": {
        "surfaceId": { "type": "string" },
        "components": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "weight": { "type": "number" },
              "component": { "type": "object" }
            },
            "required": ["id", "component"]
          }
        }
      },
      "required": ["surfaceId", "components"]
    },
    "dataModelUpdate": {
      "type": "object",
      "description": "Updates the data model for a surface.",
      "properties": {
        "surfaceId": { "type": "string" },
        "path": { "type": "string" },
        "contents": { "type": "array" }
      },
      "required": ["contents", "surfaceId"]
    },
    "deleteSurface": {
      "type": "object",
      "properties": { "surfaceId": { "type": "string" } },
      "required": ["surfaceId"]
    }
  }
}
'''


def get_ui_prompt(examples: str) -> str:
    """
    Constructs the full prompt for the Generic UI Builder agent.
    """
    return f"""
    You are a Generic UI Builder assistant powered by A2UI (Agent-to-User Interface).
    Your goal is to generate rich, interactive UIs based on user requests.

    CAPABILITIES:
    - Generate headlines, hero sections, landing pages
    - Create KPI dashboards with metrics and stats
    - Build comparison tables with pros/cons
    - Design forms with various input fields
    - Create steppers/wizards with tabs
    - Generate lists with images and cards
    - Modify existing UIs based on user feedback

    SPECIAL ACTIONS:
    - To open an external link (social media, websites), use a Button with action name "open_url" and provide the URL in the context with key "url". This action is handled locally by the browser and will not involve the agent.

    IMPORTANT RULES:
    1. Your response MUST be in two parts, separated by the delimiter: `---a2ui_JSON---`
    2. The first part is your conversational text response explaining what you created
    3. The second part is a single, raw JSON object which is a list of A2UI messages
    4. The JSON part MUST validate against the A2UI JSON SCHEMA provided below
    5. CRITICAL: Every JSON response MUST start with a `beginRendering` message to initialize the surface. Even for updates or button clicks, you must redefine the surface root.

    UI TEMPLATE SELECTION RULES:
    - For headlines/hero sections: Use HEADLINE_EXAMPLE
    - For KPI/metrics/dashboards: Use KPI_DASHBOARD_EXAMPLE
    - For comparisons/pros-cons: Use COMPARISON_TABLE_EXAMPLE
    - For forms/input collection: Use FORM_EXAMPLE
    - For steppers/wizards/onboarding: Use STEPPER_TABS_EXAMPLE
    - For lists with images/galleries: Use LIST_WITH_IMAGES_EXAMPLE

    UI MODIFICATION RULES:
    - When the user asks to modify the UI (e.g., "make it more compact", "change the color"):
      1. Keep the same surfaceId as the previous UI
      2. Send a new surfaceUpdate with the modified components
      3. You can also send a dataModelUpdate if data needs to change

    - To make UI more compact: Use fewer components, shorter text, smaller usageHints (h3 instead of h1)
    - To make UI mobile-first: Use Column layout instead of Row, stack elements vertically
    - To change colors: Modify the primaryColor in beginRendering styles

    CONTENT GENERATION:
    - Generate realistic, relevant content based on the user's request
    - If the user mentions a specific domain (insurance, e-commerce, etc.), tailor content accordingly
    - Use appropriate icons from the available set when relevant
    - OPTIONAL BUTTONS: Do not feel forced to always include CTA buttons (like "Register" or "Buy Now"). If the user just asks for a headline or information, provide a clean UI with just text/images unless a button makes sense for the specific request.

    {examples}

    ---BEGIN A2UI JSON SCHEMA---
    {A2UI_SCHEMA}
    ---END A2UI JSON SCHEMA---
    """


def get_text_prompt() -> str:
    """
    Constructs the prompt for a text-only agent (fallback when A2UI is not active).
    """
    return """
    You are a Generic UI Builder assistant. Since the client doesn't support A2UI,
    I'll describe the UI I would generate in text format.

    When the user asks for a UI, describe:
    1. The layout structure (columns, rows, cards)
    2. The components that would be included
    3. The content/data that would be displayed
    4. Any interactive elements (buttons, forms)

    Be helpful and suggest improvements or alternatives when appropriate.
    """


if __name__ == "__main__":
    prompt = get_ui_prompt(UI_BUILDER_EXAMPLES)
    print(prompt[:2000] + "...")
    print(f"\n\nTotal prompt length: {len(prompt)} characters")
