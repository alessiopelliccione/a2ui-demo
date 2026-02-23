# Architettura A2UI (Agent-to-UI) - Panoramica per Presentazione

Questo diagramma illustra il flusso logico macro del sistema A2UI, focalizzandosi sull'interazione tra Utente, Agente e Intelligenza Artificiale.

```mermaid
graph LR
    subgraph "Utente"
        User((Utente))
    end

    subgraph "Frontend (Web/Mobile)"
        UI[<b>A2UI Shell</b><br/>Interfaccia di Chat]
        Renderer[<b>Dynamic Renderer</b><br/>Componenti UI]
    end

    subgraph "Backend (Python Agent)"
        Agent[<b>A2UI Agent</b><br/>Orchestratore]
        Schema[<b>A2UI Schema</b><br/>Validazione Contratto]
    end

    subgraph "Intelligenza Artificiale"
        LLM((<b>LLM</b><br/>Gemini / GPT / Claude))
    end

    %% Flusso di Andata (Prompt)
    User -- "1. Richiesta Naturale" --> UI
    UI -- "2. API Call" --> Agent
    Agent -- "3. Prompt + Esempi" --> LLM

    %% Flusso di Ritorno (Rendering)
    LLM -- "4. Generazione JSON" --> Agent
    Agent -- "5. Validazione" --> Schema
    Schema -- "6. JSON Validato" --> Agent
    Agent -- "7. Stream UI Data" --> UI
    UI -- "8. Rendering Dinamico" --> Renderer
    Renderer -- "9. Interazione UI" --> User

    %% Stili per la presentazione
    style UI fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Agent fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style LLM fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style Schema fill:#fff3e0,stroke:#e65100,stroke-dasharray: 5 5
```

## Punti Chiave del Sistema

1.  **Linguaggio Naturale → UI Reale:** L'utente interagisce con l'AI per generare interfacce complesse senza scrivere codice.
2.  **Architettura Server-Driven (SDUI):** La logica e la struttura della UI risiedono sul server (Agente), rendendo il frontend leggero e cross-platform.
3.  **Il Contratto JSON (A2UI Schema):** Un formato strutturato che garantisce che l'AI generi solo interfacce valide e compatibili con i componenti del renderer.
4.  **Validazione in Tempo Reale:** L'Agente convalida l'output dell'LLM prima che raggiunga l'utente, correggendo eventuali errori di generazione.
5.  **Streaming & Interattività:** Supporto nativo per aggiornamenti incrementali e azioni utente (bottoni, form) che tornano all'Agente per chiudere il ciclo di feedback.
