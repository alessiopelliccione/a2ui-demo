# A2UI Architecture (Agent-to-UI) - Presentation Overview

This diagram illustrates the macro logical flow of the A2UI system, focusing on the interaction between the User, Agent, and Artificial Intelligence.

```mermaid
graph LR
    subgraph UserGroup ["User"]
        UserNode((User))
    end

    subgraph FrontendGroup ["Frontend (Web/Mobile)"]
        UI[<b>A2UI Shell</b><br/>Chat Interface]
        Renderer[<b>Dynamic Renderer</b><br/>UI Components]
    end

    subgraph BackendGroup ["Backend (Python Agent)"]
        Agent[<b>A2UI Agent</b><br/>Orchestrator]
        Schema[<b>A2UI Schema</b><br/>Contract Validation]
    end

    subgraph AIGroup ["Artificial Intelligence"]
        LLM((<b>LLM</b><br/>Gemini / GPT / Claude))
    end

    %% Forward Flow (Prompt)
    UserNode -- "1. Natural Language Request" --> UI
    UI -- "2. API Call" --> Agent
    Agent -- "3. Prompt + Examples" --> LLM

    %% Return Flow (Rendering)
    LLM -- "4. JSON Generation" --> Agent
    Agent -- "5. Validation" --> Schema
    Schema -- "6. Validated JSON" --> Agent
    Agent -- "7. Stream UI Data" --> UI
    UI -- "8. Dynamic Rendering" --> Renderer
    Renderer -- "9. UI Interaction" --> UserNode

    %% Presentation styles
    style UI fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Agent fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style LLM fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style Schema fill:#fff3e0,stroke:#e65100,stroke-dasharray: 5 5
```

## Key System Highlights

1.  **Natural Language → Real UI:** The user interacts with AI to generate complex interfaces without writing code.
2.  **Server-Driven Architecture (SDUI):** UI logic and structure reside on the server (Agent), keeping the frontend lightweight and cross-platform.
3.  **The JSON Contract (A2UI Schema):** A structured format ensuring the AI generates only valid interfaces compatible with renderer components.
4.  **Real-Time Validation:** The Agent validates LLM output before it reaches the user, correcting any generation errors.
5.  **Streaming & Interactivity:** Native support for incremental updates and user actions (buttons, forms) that flow back to the Agent to close the feedback loop.
