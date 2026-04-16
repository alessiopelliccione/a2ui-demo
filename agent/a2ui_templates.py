# A2UI Template Engine
# Pre-built templates that generate valid A2UI JSON from structured data.
# The AI picks a template name + provides data; this code does the rest.

import logging

logger = logging.getLogger(__name__)


class A2UIBuilder:
    """Helper to build A2UI component trees in the correct wire format."""

    def __init__(self):
        self._components = []
        self._n = 0

    def _id(self, prefix):
        self._n += 1
        return f"{prefix}{self._n}"

    # ── Leaf components ──

    def text(self, value, hint="body"):
        cid = self._id("t")
        comp = {"Text": {"text": {"literalString": str(value)}}}
        if hint:
            comp["Text"]["usageHint"] = hint
        self._components.append({"id": cid, "component": comp})
        return cid

    def icon(self, name):
        cid = self._id("i")
        self._components.append({"id": cid, "component": {"Icon": {"name": {"literalString": name}}}})
        return cid

    def divider(self):
        cid = self._id("d")
        self._components.append({"id": cid, "component": {"Divider": {}}})
        return cid

    # ── Interactive components ──

    def button(self, label, action_name, context=None):
        label_id = self.text(label)
        cid = self._id("b")
        action = {"name": action_name}
        if context:
            action["context"] = []
            for k, v in context.items():
                if isinstance(v, dict) and "path" in v:
                    action["context"].append({"key": k, "value": v})
                else:
                    action["context"].append({"key": k, "value": {"literalString": str(v)}})
        self._components.append({
            "id": cid,
            "component": {"Button": {"child": label_id, "action": action}}
        })
        return cid

    def text_field(self, label, data_path, placeholder=""):
        cid = self._id("tf")
        comp = {
            "TextField": {
                "label": {"literalString": label},
                "text": {"path": data_path},
            }
        }
        if placeholder:
            comp["TextField"]["placeholder"] = {"literalString": placeholder}
        self._components.append({"id": cid, "component": comp})
        return cid

    def date_input(self, label, data_path):
        cid = self._id("dt")
        self._components.append({
            "id": cid,
            "component": {
                "DateTimeInput": {
                    "label": {"literalString": label},
                    "value": {"path": data_path},
                }
            }
        })
        return cid

    def multiple_choice(self, label, options, data_path, max_selections=1):
        """options: list of (display_label, value) tuples."""
        cid = self._id("mc")
        self._components.append({
            "id": cid,
            "component": {
                "MultipleChoice": {
                    "selections": {"path": data_path},
                    "options": [
                        {"label": {"literalString": lbl}, "value": val}
                        for lbl, val in options
                    ],
                    "maxAllowedSelections": max_selections,
                }
            }
        })
        return cid

    # ── Layout components ──

    def column(self, children, alignment=None):
        cid = self._id("col")
        comp = {"Column": {"children": {"explicitList": children}}}
        if alignment:
            comp["Column"]["alignment"] = alignment
        self._components.append({"id": cid, "component": comp})
        return cid

    def row(self, children, distribution="start"):
        cid = self._id("row")
        comp = {"Row": {"children": {"explicitList": children}}}
        if distribution != "start":
            comp["Row"]["distribution"] = distribution
        self._components.append({"id": cid, "component": comp})
        return cid

    def card(self, children):
        """Card wrapping a list of child IDs (auto-wrapped in Column)."""
        inner = self.column(children)
        cid = self._id("card")
        self._components.append({
            "id": cid,
            "component": {"Card": {"child": inner}}
        })
        return cid

    def tabs(self, items):
        """items: list of (title_str, child_component_id) tuples."""
        cid = self._id("tabs")
        self._components.append({
            "id": cid,
            "component": {
                "Tabs": {
                    "tabItems": [
                        {"title": {"literalString": title}, "child": child_id}
                        for title, child_id in items
                    ]
                }
            }
        })
        return cid

    # ── Build ──

    def build(self, root_id, data_model=None):
        """Return list of A2UI server messages."""
        msgs = [
            {"beginRendering": {"surfaceId": "default", "root": root_id}},
            {"surfaceUpdate": {"surfaceId": "default", "components": self._components}},
        ]
        if data_model:
            msgs.append({
                "dataModelUpdate": {
                    "surfaceId": "default",
                    "path": "/",
                    "contents": data_model,
                }
            })
        return msgs


# ═══════════════════════════════════════════════════════════════
#  TEMPLATE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def render_template(name, data):
    """Dispatch to the correct template function. Returns A2UI messages or None."""
    templates = {
        "policy_list": _render_policy_list,
        "policy_detail": _render_policy_detail,
        "comparison": _render_comparison,
        "dashboard": _render_dashboard,
        "form": _render_form,
        "info_list": _render_info_list,
    }
    fn = templates.get(name)
    if fn is None:
        logger.warning(f"Unknown template: {name}")
        return None
    try:
        return fn(data or {})
    except Exception as e:
        logger.error(f"Template '{name}' failed: {e}")
        return None


# ── policy_list ──

def _render_policy_list(data):
    b = A2UIBuilder()
    title = b.text(data.get("title", "Available Policies"), "h2")

    card_ids = []
    for p in data.get("policies", []):
        children = [
            b.text(p["name"], "h3"),
            b.text(f"\u20ac{p['price']}/month", "h4"),
        ]
        for feat in p.get("features", []):
            children.append(
                b.row([b.icon("check_circle"), b.text(feat)], "start")
            )
        children.append(b.divider())
        children.append(b.button("Select", "select_policy", {
            "policyName": p["name"],
            "policyId": p.get("id", p["name"].lower().replace(" ", "-")),
        }))
        card_ids.append(b.card(children))

    if len(card_ids) > 1:
        body = b.row(card_ids, "spaceEvenly")
    else:
        body = b.column(card_ids)

    root = b.column([title, body])
    return b.build(root)


# ── policy_detail ──

def _render_policy_detail(data):
    b = A2UIBuilder()
    children = [
        b.text(data.get("name", "Policy Details"), "h2"),
        b.text(data.get("type", ""), "caption"),
        b.text(f"\u20ac{data.get('price', 0)}/{data.get('period', 'month')}", "h3"),
        b.divider(),
    ]

    if data.get("deductible") is not None:
        children.append(
            b.row([b.text("Deductible:", "h5"), b.text(f"\u20ac{data['deductible']}")], "start")
        )
    if data.get("maxCoverage"):
        children.append(
            b.row([b.text("Max Coverage:", "h5"), b.text(str(data["maxCoverage"]))], "start")
        )

    children.append(b.divider())
    children.append(b.text("Included Coverage", "h4"))
    for c in data.get("coverages", []):
        children.append(
            b.row([b.icon("check_circle"), b.text(c)], "start")
        )

    if data.get("benefits"):
        children.append(b.divider())
        children.append(b.text("Benefits", "h4"))
        for ben in data["benefits"]:
            children.append(
                b.row([b.icon("star"), b.text(ben)], "start")
            )

    children.append(b.divider())
    children.append(b.button(
        data.get("actionLabel", "Activate this policy"),
        data.get("actionName", "activate_policy"),
        {"policyName": data.get("name", ""), "policyId": data.get("id", "")},
    ))

    root = b.card(children)
    return b.build(root)


# ── comparison ──

def _render_comparison(data):
    b = A2UIBuilder()
    title = b.text(data.get("title", "Plan Comparison"), "h2")

    card_ids = []
    for plan in data.get("plans", []):
        children = []
        if plan.get("highlighted"):
            children.append(b.row([b.icon("star"), b.text("Recommended", "caption")], "start"))
        children.append(b.text(plan["name"], "h3"))
        children.append(b.text(
            f"\u20ac{plan['price']}/{plan.get('period', 'month')}", "h4"
        ))
        children.append(b.divider())
        for feat in plan.get("features", []):
            children.append(
                b.row([b.icon("check_circle"), b.text(feat)], "start")
            )
        children.append(b.divider())
        children.append(b.button("Select", "select_policy", {
            "policyName": plan["name"],
            "policyId": plan.get("id", plan["name"].lower().replace(" ", "-")),
        }))
        card_ids.append(b.card(children))

    body = b.row(card_ids, "spaceEvenly")
    root = b.column([title, body])
    return b.build(root)


# ── dashboard ──

def _render_dashboard(data):
    b = A2UIBuilder()
    title = b.text(data.get("title", "Dashboard"), "h2")

    card_ids = []
    for kpi in data.get("kpis", []):
        children = [
            b.text(kpi.get("value", "—"), "h2"),
            b.text(kpi.get("label", ""), "caption"),
        ]
        if kpi.get("description"):
            children.append(b.text(kpi["description"], "body"))
        card_ids.append(b.card(children))

    body = b.row(card_ids, "spaceEvenly")
    root = b.column([title, body])
    return b.build(root)


# ── form ──

def _render_form(data):
    b = A2UIBuilder()
    children = [b.text(data.get("title", "Form"), "h2")]

    if data.get("description"):
        children.append(b.text(data["description"]))

    # Data model for form field bindings
    form_data = {}
    for i, field in enumerate(data.get("fields", [])):
        ftype = field.get("type", "text")
        label = field.get("label", f"Field {i+1}")
        path_key = label.lower().replace(" ", "_")
        data_path = f"/form/{path_key}"
        form_data[path_key] = ""

        if ftype == "date":
            children.append(b.date_input(label, data_path))
        elif ftype == "select":
            options = [(o, o.lower().replace(" ", "_")) for o in field.get("options", [])]
            children.append(b.text(label, "h5"))
            children.append(b.multiple_choice(label, options, data_path))
        else:
            children.append(b.text_field(label, data_path, field.get("placeholder", "")))

    # Submit button includes all form field values via path references
    form_context = {k: {"path": f"/form/{k}"} for k in form_data}
    children.append(b.button(
        data.get("submitLabel", "Submit"),
        data.get("submitAction", "submit_form"),
        form_context,
    ))

    root = b.column(children)

    # Build data model contents
    dm = [{"key": "form", "valueMap": [
        {"key": k, "valueString": v} for k, v in form_data.items()
    ]}]

    return b.build(root, data_model=dm)


# ── info_list ──

def _render_info_list(data):
    b = A2UIBuilder()
    title = b.text(data.get("title", "List"), "h2")

    card_ids = []
    for item in data.get("items", []):
        children = []

        # Header row: title + optional status
        header_parts = [b.text(item.get("title", ""), "h4")]
        if item.get("status"):
            header_parts.append(b.text(item["status"], "caption"))
        children.append(b.row(header_parts, "spaceBetween"))

        if item.get("subtitle"):
            children.append(b.text(item["subtitle"], "body"))

        # Detail rows
        for detail in item.get("details", []):
            children.append(
                b.row([
                    b.text(detail.get("label", ""), "h5"),
                    b.text(detail.get("value", "")),
                ], "spaceBetween")
            )

        # Optional action button
        if item.get("actionLabel") and item.get("actionName"):
            ctx = {}
            if item.get("title"):
                ctx["itemTitle"] = item["title"]
            if item.get("id"):
                ctx["itemId"] = item["id"]
            children.append(b.button(item["actionLabel"], item["actionName"], ctx))

        card_ids.append(b.card(children))

    root = b.column([title] + card_ids)
    return b.build(root)
