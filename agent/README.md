# UI Builder Agent - A2UI Demo

A generic UI Builder agent that creates rich, interactive interfaces from natural language using Google's A2UI framework.

## Demo for Generative Frontend / Server-Driven UI Session

This agent demonstrates the power of AI-driven UI generation where:
- User describes what they want in natural language
- LLM generates A2UI JSON schema
- Client renders the UI dynamically

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Gemini API key

### Setup

1. **Set your API key:**
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key"
   ```

2. **Run the agent:**
   ```bash
   cd agent
   uv run .
   ```

3. **Start the web client** (in another terminal):
   ```bash
   cd ../A2UI/samples/client/lit/shell
   npm install && npm run dev
   ```

4. **Open browser:** http://localhost:5173

## Demo Commands to Try

| Command | What it creates |
|---------|----------------|
| "Create a headline for an insurance company" | Hero section with title, subtitle, CTA |
| "Build a KPI dashboard with user metrics" | 3-column metrics dashboard |
| "Compare Product A and Product B with pros/cons" | Side-by-side comparison cards |
| "Generate a contact form" | Form with name, email, message fields |
| "Add a stepper for user onboarding" | Tabbed wizard with 3 steps |
| "Make it more compact" | Modifies existing UI to be smaller |
| "Change the color to red" | Updates primary color |

## Architecture

```
User prompt
    ↓
UI Builder Agent (Python)
    ↓
Gemini LLM generates A2UI JSON
    ↓
A2A Protocol transport
    ↓
Lit Web Components render UI
    ↓
Interactive UI displayed
```

## Files

- `agent.py` - Main agent logic with LLM integration
- `agent_executor.py` - A2A protocol handler
- `prompt_builder.py` - System prompt with A2UI schema
- `a2ui_examples.py` - UI pattern examples for the LLM
- `__main__.py` - Server entry point

## Customization

### Adding New UI Patterns

Edit `a2ui_examples.py` to add new patterns. Follow the existing format:

```
---BEGIN YOUR_PATTERN_EXAMPLE---
Description: When to use this pattern
[
  { "beginRendering": {...} },
  { "surfaceUpdate": {...} },
  { "dataModelUpdate": {...} }
]
---END YOUR_PATTERN_EXAMPLE---
```

### Changing LLM Model

Set the `LITELLM_MODEL` environment variable:
```bash
export LITELLM_MODEL="gemini/gemini-2.5-pro"
```

## Port Configuration

Default port is `10003`. Change with:
```bash
uv run . --port 10004
```
