# A2UI Demo - Generative Frontend Session

**Standalone** demo repository for the **Generative Frontend / Server-Driven UI / AI-Driven UI** session.

Built with [Google A2UI](https://github.com/google/A2UI) (Agent-to-User Interface).

## What's Inside

```
a2ui-demo/
├── agent/                  # Python agent (UI Builder)
│   ├── agent.py            # Main agent logic
│   ├── agent_executor.py   # A2A protocol handler
│   ├── prompt_builder.py   # LLM prompts with A2UI schema
│   ├── a2ui_examples.py    # UI pattern examples
│   ├── lib/                # Local A2UI extension library
│   └── __main__.py         # Server entry point
├── renderers/              # A2UI Web Renderers
│   ├── web_core/           # Core TypeScript library
│   └── lit/                # Lit Web Components
├── client/
│   └── shell/              # Web client (chat interface)
├── slides.pptx             # Presentation slides (13 slides)
├── ROADMAP.md              # Detailed session structure
└── README.md               # This file
```

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- API key for your preferred LLM provider

### 1. Choose Your LLM Provider

The agent supports multiple LLM providers via [LiteLLM](https://docs.litellm.ai/docs/providers).

**Option A: Google Gemini (default)**
```bash
export GEMINI_API_KEY="your_gemini_api_key"
# Optional: specify model (default: gemini/gemini-2.5-flash)
export LITELLM_MODEL="gemini/gemini-2.5-pro"
```

**Option B: OpenAI**
```bash
export OPENAI_API_KEY="your_openai_api_key"
export LITELLM_MODEL="gpt-4o"  # or gpt-4o-mini, gpt-4-turbo
```

**Option C: Anthropic Claude**
```bash
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export LITELLM_MODEL="claude-3-5-sonnet-20241022"
```

**Option D: Azure OpenAI**
```bash
export AZURE_API_KEY="your_azure_api_key"
export AZURE_API_BASE="https://your-resource.openai.azure.com"
export LITELLM_MODEL="azure/gpt-4o"
```

### 2. Build Renderers (first time only)

```bash
# Build web_core
cd renderers/web_core
npm install && npm run build

# Build lit renderer
cd ../lit
npm install && npm run build
```

### 3. Start the UI Builder Agent

```bash
cd agent
uv run .
```

Agent runs on `http://localhost:10003`

### 4. Start the Web Client

```bash
cd client/shell
npm install && npm run dev
```

Client runs on `http://localhost:5173`

### 5. Open Browser and Demo!

Navigate to `http://localhost:5173` and try these commands:

| Demo | Command |
|------|---------|
| Headline | "Create a headline for an insurance company" |
| KPI Dashboard | "Build a KPI dashboard with user metrics" |
| Comparison | "Compare Product A and Product B with pros/cons" |
| Form | "Generate a contact form" |
| Stepper | "Add a stepper for user onboarding" |
| Modification | "Make it more compact" |

## One-Liner Setup

```bash
# Terminal 1: Build and run agent (with Gemini)
export GEMINI_API_KEY="your_key" && cd renderers/web_core && npm install && npm run build && cd ../lit && npm install && npm run build && cd ../../agent && uv run .

# Or with OpenAI
export OPENAI_API_KEY="your_key" && export LITELLM_MODEL="gpt-4o" && cd agent && uv run .

# Terminal 2: Run client
cd client/shell && npm install && npm run dev
```

## Session Structure (30-45 min)

1. **Intro** (5 min) - What is a Generative Frontend?
2. **Why It Matters** (3-4 min) - Use cases and benefits
3. **Architecture** (8-10 min) - A2UI and LLM integration
4. **Demos** (10-15 min) - 4 live demos
5. **Code** (5 min) - Minimal UI renderer
6. **Takeaways** (3 min) - Key insights

See `ROADMAP.md` for detailed structure.

## Architecture

```
User Prompt
    ↓
UI Builder Agent (Python + Gemini)
    ↓
A2UI JSON Messages (beginRendering, surfaceUpdate, dataModelUpdate)
    ↓
A2A Protocol Transport
    ↓
Lit Web Components Renderer
    ↓
Interactive UI
```

## Available UI Patterns

The agent can generate these UI patterns:

- **Headline/Hero** - Title, subtitle, CTA button
- **KPI Dashboard** - 3-column metrics cards
- **Comparison Table** - Side-by-side product cards with pros/cons
- **Contact Form** - Name, email, message fields
- **Stepper/Wizard** - Tabbed multi-step flow
- **Image List** - Cards with images and details

## Troubleshooting

### "API_KEY not set" error
Set the appropriate API key for your chosen model:
```bash
# For Gemini (default)
export GEMINI_API_KEY="your_key_here"

# For OpenAI
export OPENAI_API_KEY="your_key_here"
export LITELLM_MODEL="gpt-4o"

# For Anthropic
export ANTHROPIC_API_KEY="your_key_here"
export LITELLM_MODEL="claude-3-5-sonnet-20241022"
```

### Build errors in renderers
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Agent connection issues
Make sure agent is running on port 10003 before starting client.

## Resources

- [Google A2UI](https://github.com/google/A2UI)
- [A2A Protocol](https://github.com/google/A2A)
- [Gemini API](https://ai.google.dev/)

## License

Apache 2.0
