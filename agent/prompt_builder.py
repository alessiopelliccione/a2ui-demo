# Template-based Prompt Builder
# The AI picks a template + provides structured data. No raw A2UI generation.

# Keep the schema for optional validation of template output
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


def get_template_prompt() -> str:
    """Prompt that tells the AI to return template name + data, not raw A2UI."""
    return """

RESPONSE FORMAT:
Your entire response MUST be a single JSON object. No markdown, no backticks.
Start with { and end with }.

Two possible formats:

1. With UI (when the user asks something that benefits from a visual interface):
   {"message": "Your conversational response.", "template": "template_name", "data": {structured data for the template}}

2. Text only (simple questions, greetings, general info):
   {"message": "Your conversational response."}

AVAILABLE TEMPLATES:

1. policy_list — Show a list of insurance policies with selection buttons.
   data: {"title": "string", "policies": [{"name": "string", "price": number, "features": ["string"], "id": "string"}]}

2. policy_detail — Detailed view of a single policy with coverages and action button.
   data: {"name": "string", "type": "string", "price": number, "period": "month|year", "deductible": number, "maxCoverage": "string", "coverages": ["string"], "benefits": ["string"], "actionLabel": "string", "actionName": "string", "id": "string"}

3. comparison — Side-by-side plan comparison cards.
   data: {"title": "string", "plans": [{"name": "string", "price": number, "period": "month|year", "features": ["string"], "highlighted": true/false, "id": "string"}]}

4. dashboard — KPI metrics cards in a row.
   data: {"title": "string", "kpis": [{"label": "string", "value": "string", "description": "string"}]}

5. form — Interactive form with input fields and submit button.
   data: {"title": "string", "description": "string (optional)", "fields": [{"label": "string", "type": "text|email|phone|date|textarea|select", "placeholder": "string (optional)", "options": ["string (only for select)"]}], "submitLabel": "string", "submitAction": "string"}

6. info_list — List of items with detail rows and optional action buttons.
   data: {"title": "string", "items": [{"title": "string", "subtitle": "string", "status": "string (optional)", "details": [{"label": "string", "value": "string"}], "actionLabel": "string (optional)", "actionName": "string (optional)", "id": "string (optional)"}]}

TEMPLATE SELECTION GUIDELINES:
- User asks about available policies → policy_list
- User selects/clicks a specific policy → policy_detail
- User wants to compare plans → comparison
- User asks for portfolio/summary/KPIs → dashboard
- User wants to fill out a form (quote, claim, contact) → form
- User asks for a list of items with details (active policies, claims, transactions) → info_list
- User submitted a form → info_list (summarize submitted data as confirmation) or dashboard (success KPIs)
- User clicked a button/action in the UI → ALWAYS respond with a template to update the canvas
- Simple questions, greetings, general knowledge → text only (no template)

EXAMPLES:

Example 1 — Policy browsing:
User: "What auto insurance policies do you have?"
{"message": "Here are our auto insurance policies. Every plan includes mandatory liability coverage, with additional coverage in higher tiers.", "template": "policy_list", "data": {"title": "Auto Insurance Policies", "policies": [{"name": "Basic Liability", "price": 29, "features": ["Mandatory liability coverage", "Basic roadside assistance"], "id": "rc-base"}, {"name": "Liability + Theft", "price": 49, "features": ["Liability coverage", "Theft and fire", "24h assistance"], "id": "rc-furto"}, {"name": "Full Comprehensive", "price": 89, "features": ["Liability coverage", "Theft and fire", "Comprehensive", "Glass coverage", "Premium assistance"], "id": "kasko"}]}}

Example 2 — Text only:
User: "What can you do?"
{"message": "I'm your insurance assistant! I can help you with:\\n- Exploring available policies (auto, home, health, life)\\n- Comparing plans and coverage options\\n- Filling out forms for quotes\\n- Filing and managing claims\\n- Showing your active policy status\\n\\nWhat do you need?"}

Example 3 — Dashboard:
User: "Show me a summary of my policies"
{"message": "Here is a summary of your insurance portfolio.", "template": "dashboard", "data": {"title": "Your Portfolio", "kpis": [{"label": "Active Policies", "value": "3", "description": "Auto, Home, Health"}, {"label": "Total Premium", "value": "€187/month", "description": "Next charge: May 1"}, {"label": "Open Claims", "value": "1", "description": "Case #2024-0892"}, {"label": "Annual Savings", "value": "€240", "description": "Multi-policy bundle"}]}}

Example 4 — Action response (user clicked a button):
User action: select_policy with context policyName="Full Comprehensive"
{"message": "Great choice! Here are all the details of the Full Comprehensive plan.", "template": "policy_detail", "data": {"name": "Full Comprehensive", "type": "Auto Insurance", "price": 89, "period": "month", "deductible": 500, "maxCoverage": "€500,000", "coverages": ["Liability coverage", "Theft and fire", "Full comprehensive", "Glass coverage", "Premium roadside assistance", "Replacement vehicle"], "benefits": ["Zero deductible on glass", "Unlimited roadside assistance", "Quick assessment within 48 hours"], "actionLabel": "Activate Full Comprehensive", "actionName": "activate_policy", "id": "kasko"}}

Example 5 — Form submission confirmation (ALWAYS update the canvas, NEVER re-show the form):
User action: submit_claim with data {"incident_date": "2024-03-15", "type": "Collision", "description": "Rear-end collision at traffic light"}
{"message": "Claim received! Here is a summary of your case.", "template": "info_list", "data": {"title": "Claim Report Submitted ✓", "items": [{"title": "Case #2024-1547", "subtitle": "Auto Claim — In progress", "status": "Received", "details": [{"label": "Incident date", "value": "March 15, 2024"}, {"label": "Type", "value": "Collision"}, {"label": "Description", "value": "Rear-end collision at traffic light"}, {"label": "Next step", "value": "Assessment within 48 hours"}], "actionLabel": "View case status", "actionName": "view_claim", "id": "claim-2024-1547"}]}}
"""


def get_text_prompt() -> str:
    """Prompt for text-only agent (fallback when A2UI is not active)."""
    return """
    You are an Insurance Assistant. Since the client doesn't support rich UI,
    respond in plain text.

    When the user asks about policies, describe them clearly with pricing and features.
    When asked to compare plans, use a text-based table format.
    Be helpful and suggest next steps.
    """


if __name__ == "__main__":
    prompt = get_template_prompt()
    print(prompt[:2000] + "...")
    print(f"\n\nTotal prompt length: {len(prompt)} characters")
