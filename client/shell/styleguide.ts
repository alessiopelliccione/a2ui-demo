import { v0_8 } from "@a2ui/lit";
import { theme as uiTheme } from "./theme/default-theme";
import * as UI from "@a2ui/lit/ui";
import { LitElement, html, css } from "lit";
import { customElement } from "lit/decorators.js";
import { provide } from "@lit/context";
import { SignalWatcher } from "@lit-labs/signals";
import { repeat } from "lit/directives/repeat.js";

const STYLEGUIDE_UI: v0_8.Types.ServerToClientMessage[] = [
  {
    beginRendering: {
      surfaceId: "styleguide",
      root: "kitchen-sink"
    }
  },
  {
    surfaceUpdate: {
      surfaceId: "styleguide",
      components: [
        {
          id: "kitchen-sink",
          component: {
            Column: {
              children: {
                explicitList: [
                  "section-buttons",
                  "buttons-card",
                  "section-text",
                  "text-card",
                  "section-layout",
                  "layout-card"
                ]
              }
            }
          }
        },
        
        // --- BUTTONS SECTION ---
        {
          id: "section-buttons",
          component: { Text: { usageHint: "h2", text: { literalString: "Buttons" } } }
        },
        {
          id: "buttons-card",
          component: { Card: { child: "buttons-row" } }
        },
        {
          id: "buttons-row",
          component: {
            Row: {
              distribution: "spaceEvenly",
              children: {
                explicitList: ["primary-btn", "secondary-btn"]
              }
            }
          }
        },
        {
          id: "primary-btn",
          component: {
            Button: {
              child: "primary-btn-text",
              primary: true,
              action: { name: "demo", context: [] }
            }
          }
        },
        { id: "primary-btn-text", component: { Text: { text: { literalString: "Primary Button" } } } },
        
        {
          id: "secondary-btn",
          component: {
            Button: {
              child: "secondary-btn-text",
              primary: false,
              action: { name: "demo", context: [] }
            }
          }
        },
        { id: "secondary-btn-text", component: { Text: { text: { literalString: "Secondary Button" } } } },


        // --- TEXT SECTION ---
        {
          id: "section-text",
          component: { Text: { usageHint: "h2", text: { literalString: "Typography" } } }
        },
        {
          id: "text-card",
          component: { Card: { child: "text-column" } }
        },
        {
          id: "text-column",
          component: {
            Column: {
              children: {
                explicitList: ["txt-h1", "txt-h2", "txt-h3", "txt-body", "txt-caption"]
              }
            }
          }
        },
        { id: "txt-h1", component: { Text: { usageHint: "h1", text: { literalString: "Heading 1 (h1)" } } } },
        { id: "txt-h2", component: { Text: { usageHint: "h2", text: { literalString: "Heading 2 (h2)" } } } },
        { id: "txt-h3", component: { Text: { usageHint: "h3", text: { literalString: "Heading 3 (h3)" } } } },
        { id: "txt-body", component: { Text: { usageHint: "body", text: { literalString: "Body Text. Used for descriptions and normal content." } } } },
        { id: "txt-caption", component: { Text: { usageHint: "caption", text: { literalString: "Caption. Small subtle text." } } } },


        // --- LAYOUT E DIVIDERS SECTION ---
        {
          id: "section-layout",
          component: { Text: { usageHint: "h2", text: { literalString: "Cards & Dividers" } } }
        },
        {
          id: "layout-card",
          component: { Card: { child: "layout-column" } }
        },
        {
          id: "layout-column",
          component: {
            Column: {
              children: {
                explicitList: ["layout-text-1", "layout-divider", "layout-text-2"]
              }
            }
          }
        },
        { id: "layout-text-1", component: { Text: { usageHint: "body", text: { literalString: "Questo è il contenuto in alto dentro una Card." } } } },
        { id: "layout-divider", component: { Divider: {} } },
        { id: "layout-text-2", component: { Text: { usageHint: "caption", text: { literalString: "Questo contenuto è separato dal Divider in basso." } } } }

      ]
    }
  }
];

@customElement("a2ui-styleguide")
export class A2UIStyleguide extends SignalWatcher(LitElement) {
  @provide({ context: UI.Context.themeContext })
  accessor theme: v0_8.Types.Theme = uiTheme;

  #processor = v0_8.Data.createSignalA2uiMessageProcessor();

  static styles = css`
    :host {
      display: block;
      width: 100%;
    }
  `;

  connectedCallback() {
    super.connectedCallback();
    this.#processor.processMessages(STYLEGUIDE_UI);
  }

  render() {
    const surfaces = this.#processor.getSurfaces();
    return html`
      <div>
        ${repeat(surfaces, ([id]) => id, ([id, surface]) => html`
          <a2ui-surface
            .surfaceId=${id}
            .surface=${surface}
            .processor=${this.#processor}
          ></a2ui-surface>
        `)}
      </div>
    `;
  }
}
