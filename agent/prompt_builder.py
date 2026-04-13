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
   data: {"name": "string", "type": "string", "price": number, "period": "mese|anno", "deductible": number, "maxCoverage": "string", "coverages": ["string"], "benefits": ["string"], "actionLabel": "string", "actionName": "string", "id": "string"}

3. comparison — Side-by-side plan comparison cards.
   data: {"title": "string", "plans": [{"name": "string", "price": number, "period": "mese|anno", "features": ["string"], "highlighted": true/false, "id": "string"}]}

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
- Simple questions, greetings, general knowledge → text only (no template)

EXAMPLES:

Example 1 — Policy browsing:
User: "Che polizze auto avete?"
{"message": "Ecco le nostre polizze auto. Ogni piano include la RC obbligatoria con coperture aggiuntive nei piani superiori.", "template": "policy_list", "data": {"title": "Polizze Auto", "policies": [{"name": "RC Base", "price": 29, "features": ["Responsabilità civile obbligatoria", "Assistenza stradale base"], "id": "rc-base"}, {"name": "RC + Furto", "price": 49, "features": ["Responsabilità civile", "Furto e incendio", "Assistenza 24h"], "id": "rc-furto"}, {"name": "Kasko Completa", "price": 89, "features": ["Responsabilità civile", "Furto e incendio", "Kasko", "Cristalli", "Assistenza premium"], "id": "kasko"}]}}

Example 2 — Text only:
User: "Cosa sai fare?"
{"message": "Sono il tuo assistente assicurativo! Posso aiutarti a:\\n- Esplorare le polizze disponibili (auto, casa, salute, vita)\\n- Confrontare piani e coperture\\n- Compilare moduli per preventivi\\n- Aprire e gestire sinistri\\n- Mostrarti lo stato delle tue polizze attive\\n\\nCosa ti serve?"}

Example 3 — Dashboard:
User: "Mostrami il riepilogo delle mie polizze"
{"message": "Ecco il riepilogo del tuo portfolio assicurativo.", "template": "dashboard", "data": {"title": "Il Tuo Portfolio", "kpis": [{"label": "Polizze Attive", "value": "3", "description": "Auto, Casa, Salute"}, {"label": "Premio Totale", "value": "€187/mese", "description": "Prossimo addebito: 1 maggio"}, {"label": "Sinistri Aperti", "value": "1", "description": "Pratica #2024-0892"}, {"label": "Risparmio Annuo", "value": "€240", "description": "Bundle multi-polizza"}]}}

Example 4 — Action response (user clicked a button):
User action: select_policy with context policyName="Kasko Completa"
{"message": "Ottima scelta! Ecco tutti i dettagli della Kasko Completa.", "template": "policy_detail", "data": {"name": "Kasko Completa", "type": "Assicurazione Auto", "price": 89, "period": "mese", "deductible": 500, "maxCoverage": "€500.000", "coverages": ["Responsabilità civile", "Furto e incendio", "Kasko completa", "Cristalli", "Assistenza stradale premium", "Auto sostitutiva"], "benefits": ["Zero franchigia su cristalli", "Soccorso stradale illimitato", "Perizia rapida entro 48h"], "actionLabel": "Attiva Kasko Completa", "actionName": "activate_policy", "id": "kasko"}}
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
