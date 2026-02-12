# Session Roadmap: Generative Frontend / Server-Driven UI / AI-Driven UI

A high-impact technical session demonstrating AI-driven UI generation with Angular.

---

## Session Structure

### 1. The Shift: From Deterministic to Intent-Based (5-7 min)

**Objective:** Challenge the audience's perception of UI interaction.

**The "Natural Language Takeover" Hook:**
- **Terminals** used to accept shell commands → now it’s Natural Language.
- **IDEs** used to accept code → now it’s Natural Language.
- **Search Engines** used to accept keywords → now it’s Natural Language.
- **Your sites & apps** accept clicks, drags, hovers → soon it’ll all be Natural Language.

**The Core Thesis:**
- We are moving beyond clicks and drags.
- Massive shift: **Deterministic Flows** (if click, then X) → **Intent-Based Systems**.
- As Guillermo Rauch (Vercel) pointed out: the shift to natural language is happening now.
- **The Question:** Are we really ready for this?

---

### 2. Introduction: What is a Generative Frontend (5 min)

**Objective:** Provide immediate, clear context on the implementation.

- UI that isn't static, but is generated/modified by AI at runtime
- The LLM controls:
  - Text
  - Layout
  - Components
  - Behaviors
- We're moving from "pre-compiled UI" → "UI negotiated with the model"

**Simple analogy:**

> It's as if the design system becomes a spoken language with the model.

---

### 3. Why This Matters (3–4 min)

- Adaptive UIs per person, context, device
- Runtime-generated microfrontends
- Advanced personalization (headlines, sections, copy)
- Dynamic UX for internal/enterprise apps
- No deployment needed to change parts of the interface

---

### 4. Architecture: Transforming LLM Output → UI (8–10 min)

#### Approach A → A2UI (Angular Adaptive UI)

**Pattern:**

```
User prompt ---> LLM ---> JSON Schema ---> Angular UI Renderer
```

**Example LLM output:**

```json
{
  "type": "section",
  "title": "Weather Today",
  "components": [
    { "type": "text", "value": "It's going to rain today." },
    { "type": "chart", "data": [1, 2, 3] }
  ]
}
```

**Angular renders dynamically via:**

- `*ngComponentOutlet`
- `ViewContainerRef.createComponent`
- Component → JSON type mapping
- Reactive signals/effects

#### Alternative Approaches

**Approach B → Classic Server-Driven UI + AI completion**

- LLM produces only parameters
- Layout remains static
- But content and "micro-components" are dynamic

**Approach C → Design System as DSL for AI**

- The AI speaks directly in your design system
- Example prompt: `"Use only components from @my/design-system. Output JSON only."`

---

### 5. High-Impact Demos (10–15 min)

#### Demo 1 — Headline Generator (simple, powerful)

**User input:**

> "Homepage for insurance customers interested in mobility products"

**LLM response:**

```json
{
  "title": "Move Smarter, Travel Safer",
  "subtitle": "Your mobility insurance, personalized",
  "cta": "Discover your coverage"
}
```

Angular updates the UI in real-time.

---

#### Demo 2 — Generate a Whole Section (medium complexity)

**Prompt:**

> "Add a section with KPIs about user's policy status"

**Output:**

```json
{
  "type": "grid",
  "columns": 3,
  "items": [
    { "type": "kpi", "label": "Active Policies", "value": 3 },
    { "type": "kpi", "label": "Pending Claims", "value": 1 },
    { "type": "kpi", "label": "Payments Due", "value": "None" }
  ]
}
```

Angular renders them dynamically with component mapping.

---

#### Demo 3 — LLM-Generated Component Layout (WOW demo)

**User input:**

> "Add a comparison table between products A and B, with pros/cons."

The LLM returns JSON that Angular transforms into a reactive table.

---

#### Demo 4 — "UI Correction" via AI

**Prompt:**

> "Make it more compact and mobile-first"

The LLM regenerates layout/columns/spacing.

---

### 6. Code: Minimal Angular UI Renderer

```typescript
const componentMap = {
  text: TextComponent,
  kpi: KpiComponent,
  section: SectionComponent,
  grid: GridComponent,
};

renderNode(node: SchemaNode, vc: ViewContainerRef) {
  const comp = componentMap[node.type];
  if (!comp) return;

  const cmpRef = vc.createComponent(comp);
  Object.assign(cmpRef.instance, node);

  if (node.children) {
    node.children.forEach(child =>
      this.renderNode(child, cmpRef.instance.childContainer)
    );
  }
}
```

Shows how simple it is to connect JSON → UI.

---

### 7. Takeaways (3 min)

- LLMs are transforming the concept of frontend
- UI becomes runtime and adaptive
- Angular is perfect for Server-Driven UI thanks to:
  - Component factories
  - Reactive signals
  - Strong typing
- The challenge: maintaining control over security, design system, performance
- The future: AI-driven DX editor → self-generating UIs

---

### WOW Finale: "UI Chat"

Open the demo with:

> "Modify my UI with a sentence."

And show:

> "Add a stepper to complete onboarding"

**Boom** — the UI changes live.

---

## Demo Checklist

- [ ] Headline generator working
- [ ] KPI section generation
- [ ] Comparison table generation
- [ ] UI correction/responsive transformation
- [ ] Live "UI Chat" finale

---

## Technical Requirements

- Angular 17+ (with signals)
- LLM API access (OpenAI, Claude, or local model)
- Component registry/mapping system
- JSON schema validation (optional but recommended)

---

## Resources

- [Angular Dynamic Component Loader](https://angular.io/guide/dynamic-component-loader)
- [Server-Driven UI Patterns](https://www.judo.app/blog/server-driven-ui/)
- [Design Systems as Code](https://bradfrost.com/blog/post/design-systems-as-code/)
