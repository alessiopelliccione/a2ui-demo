import { v0_8 } from "@a2ui/lit";
import { theme as uiTheme, DesignSystemConfig } from "./theme/default-theme";
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
      root: "kitchen-sink",
      styles: { ...DesignSystemConfig } as any
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
                  "section-inputs",
                  "inputs-card",
                  "section-icons",
                  "icons-card",
                  "section-images",
                  "images-card",
                  "section-media",
                  "media-card",
                  "section-layout",
                  "layout-card",
                  "section-tabs",
                  "tabs-card",
                  "section-lists",
                  "lists-card",
                  "section-modal",
                  "modal-card"
                ]
              }
            }
          }
        },

        // ━━━ BUTTONS ━━━
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
              action: { name: "demo", context: [] }
            }
          }
        },
        { id: "secondary-btn-text", component: { Text: { text: { literalString: "Secondary Button" } } } },


        // ━━━ TYPOGRAPHY ━━━
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
                explicitList: ["txt-h1", "txt-h2", "txt-h3", "txt-h4", "txt-h5", "txt-body", "txt-caption"]
              }
            }
          }
        },
        { id: "txt-h1", component: { Text: { usageHint: "h1", text: { literalString: "Heading 1 (h1)" } } } },
        { id: "txt-h2", component: { Text: { usageHint: "h2", text: { literalString: "Heading 2 (h2)" } } } },
        { id: "txt-h3", component: { Text: { usageHint: "h3", text: { literalString: "Heading 3 (h3)" } } } },
        { id: "txt-h4", component: { Text: { usageHint: "h4", text: { literalString: "Heading 4 (h4)" } } } },
        { id: "txt-h5", component: { Text: { usageHint: "h5", text: { literalString: "Heading 5 (h5)" } } } },
        { id: "txt-body", component: { Text: { usageHint: "body", text: { literalString: "Body Text. Used for descriptions and normal content." } } } },
        { id: "txt-caption", component: { Text: { usageHint: "caption", text: { literalString: "Caption. Small subtle text." } } } },


        // ━━━ INPUT COMPONENTS ━━━
        {
          id: "section-inputs",
          component: { Text: { usageHint: "h2", text: { literalString: "Input Components" } } }
        },
        {
          id: "inputs-card",
          component: { Card: { child: "inputs-column" } }
        },
        {
          id: "inputs-column",
          component: {
            Column: {
              children: {
                explicitList: [
                  "sg-input-tf-label", "sg-input-textfield",
                  "sg-input-ta-label", "sg-input-textarea",
                  "sg-input-cb-label", "sg-input-checkbox",
                  "sg-input-dt-label", "sg-input-datetime",
                  "sg-input-sl-label", "sg-input-slider",
                  "sg-input-mc-label", "sg-input-multiplechoice"
                ]
              }
            }
          }
        },
        { id: "sg-input-tf-label", component: { Text: { usageHint: "h5", text: { literalString: "TextField (shortText)" } } } },
        {
          id: "sg-input-textfield",
          component: {
            TextField: {
              label: { literalString: "Full Name" },
              text: { literalString: "John Doe" },
              type: "shortText"
            }
          }
        },
        { id: "sg-input-ta-label", component: { Text: { usageHint: "h5", text: { literalString: "TextField (longText)" } } } },
        {
          id: "sg-input-textarea",
          component: {
            TextField: {
              label: { literalString: "Description" },
              text: { literalString: "Enter a detailed description here..." },
              type: "longText"
            }
          }
        },
        { id: "sg-input-cb-label", component: { Text: { usageHint: "h5", text: { literalString: "CheckBox" } } } },
        {
          id: "sg-input-checkbox",
          component: {
            CheckBox: {
              label: { literalString: "I agree to the terms and conditions" },
              value: { literalBoolean: true }
            }
          }
        },
        { id: "sg-input-dt-label", component: { Text: { usageHint: "h5", text: { literalString: "DateTimeInput" } } } },
        {
          id: "sg-input-datetime",
          component: {
            DateTimeInput: {
              value: { literalString: "2026-04-13T10:00" },
              enableDate: true,
              enableTime: true
            }
          }
        },
        { id: "sg-input-sl-label", component: { Text: { usageHint: "h5", text: { literalString: "Slider" } } } },
        {
          id: "sg-input-slider",
          component: {
            Slider: {
              value: { literalNumber: 50 },
              minValue: 0,
              maxValue: 100
            }
          }
        },
        { id: "sg-input-mc-label", component: { Text: { usageHint: "h5", text: { literalString: "MultipleChoice" } } } },
        {
          id: "sg-input-multiplechoice",
          component: {
            MultipleChoice: {
              selections: { literalArray: ["option-a"] },
              options: [
                { label: { literalString: "Option A" }, value: "option-a" },
                { label: { literalString: "Option B" }, value: "option-b" },
                { label: { literalString: "Option C" }, value: "option-c" }
              ],
              maxAllowedSelections: 2
            }
          }
        },


        // ━━━ ICONS ━━━
        {
          id: "section-icons",
          component: { Text: { usageHint: "h2", text: { literalString: "Icons" } } }
        },
        {
          id: "icons-card",
          component: { Card: { child: "icons-row" } }
        },
        {
          id: "icons-row",
          component: {
            Row: {
              distribution: "spaceEvenly",
              children: {
                explicitList: [
                  "sg-icon-home", "sg-icon-search", "sg-icon-settings",
                  "sg-icon-favorite", "sg-icon-star"
                ]
              }
            }
          }
        },
        { id: "sg-icon-home", component: { Icon: { name: { literalString: "home" } } } },
        { id: "sg-icon-search", component: { Icon: { name: { literalString: "search" } } } },
        { id: "sg-icon-settings", component: { Icon: { name: { literalString: "settings" } } } },
        { id: "sg-icon-favorite", component: { Icon: { name: { literalString: "favorite" } } } },
        { id: "sg-icon-star", component: { Icon: { name: { literalString: "star" } } } },


        // ━━━ IMAGES ━━━
        {
          id: "section-images",
          component: { Text: { usageHint: "h2", text: { literalString: "Images" } } }
        },
        {
          id: "images-card",
          component: { Card: { child: "images-row" } }
        },
        {
          id: "images-row",
          component: {
            Row: {
              distribution: "spaceEvenly",
              alignment: "center",
              children: {
                explicitList: ["sg-img-avatar-col", "sg-img-feature-col"]
              }
            }
          }
        },
        {
          id: "sg-img-avatar-col",
          component: {
            Column: {
              alignment: "center",
              children: { explicitList: ["sg-img-avatar-label", "sg-img-avatar"] }
            }
          }
        },
        { id: "sg-img-avatar-label", component: { Text: { usageHint: "caption", text: { literalString: "Avatar" } } } },
        {
          id: "sg-img-avatar",
          component: {
            Image: {
              url: { literalString: "https://api.dicebear.com/7.x/initials/svg?seed=A2" },
              usageHint: "avatar"
            }
          }
        },
        {
          id: "sg-img-feature-col",
          component: {
            Column: {
              alignment: "center",
              children: { explicitList: ["sg-img-feature-label", "sg-img-feature"] }
            }
          }
        },
        { id: "sg-img-feature-label", component: { Text: { usageHint: "caption", text: { literalString: "Medium Feature" } } } },
        {
          id: "sg-img-feature",
          component: {
            Image: {
              url: { literalString: "https://picsum.photos/400/200" },
              usageHint: "mediumFeature",
              fit: "cover"
            }
          }
        },


        // ━━━ MEDIA ━━━
        {
          id: "section-media",
          component: { Text: { usageHint: "h2", text: { literalString: "Media" } } }
        },
        {
          id: "media-card",
          component: { Card: { child: "media-column" } }
        },
        {
          id: "media-column",
          component: {
            Column: {
              children: {
                explicitList: ["sg-media-video-label", "sg-media-video", "sg-media-audio-label", "sg-media-audio"]
              }
            }
          }
        },
        { id: "sg-media-video-label", component: { Text: { usageHint: "h5", text: { literalString: "Video" } } } },
        {
          id: "sg-media-video",
          component: {
            Video: {
              url: { literalString: "https://www.w3schools.com/html/mov_bbb.mp4" }
            }
          }
        },
        { id: "sg-media-audio-label", component: { Text: { usageHint: "h5", text: { literalString: "AudioPlayer" } } } },
        {
          id: "sg-media-audio",
          component: {
            AudioPlayer: {
              url: { literalString: "https://www.w3schools.com/html/horse.ogg" },
              description: { literalString: "Sample Audio Track" }
            }
          }
        },


        // ━━━ CARDS & DIVIDERS ━━━
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
        { id: "layout-text-1", component: { Text: { usageHint: "body", text: { literalString: "Content above the Divider inside a Card." } } } },
        { id: "layout-divider", component: { Divider: {} } },
        { id: "layout-text-2", component: { Text: { usageHint: "caption", text: { literalString: "Content below the Divider." } } } },


        // ━━━ TABS ━━━
        {
          id: "section-tabs",
          component: { Text: { usageHint: "h2", text: { literalString: "Tabs" } } }
        },
        {
          id: "tabs-card",
          component: { Card: { child: "sg-tabs" } }
        },
        {
          id: "sg-tabs",
          component: {
            Tabs: {
              tabItems: [
                { title: { literalString: "Overview" }, child: "sg-tab-content-1" },
                { title: { literalString: "Details" }, child: "sg-tab-content-2" },
                { title: { literalString: "Settings" }, child: "sg-tab-content-3" }
              ]
            }
          }
        },
        { id: "sg-tab-content-1", component: { Text: { usageHint: "body", text: { literalString: "This is the Overview tab content. Tabs allow users to switch between different views." } } } },
        { id: "sg-tab-content-2", component: { Text: { usageHint: "body", text: { literalString: "This is the Details tab content with more specific information." } } } },
        { id: "sg-tab-content-3", component: { Text: { usageHint: "body", text: { literalString: "This is the Settings tab where users can configure options." } } } },


        // ━━━ LISTS ━━━
        {
          id: "section-lists",
          component: { Text: { usageHint: "h2", text: { literalString: "Lists" } } }
        },
        {
          id: "lists-card",
          component: { Card: { child: "lists-column" } }
        },
        {
          id: "lists-column",
          component: {
            Column: {
              children: {
                explicitList: ["sg-list-v-label", "sg-list-vertical", "sg-list-h-label", "sg-list-horizontal"]
              }
            }
          }
        },
        { id: "sg-list-v-label", component: { Text: { usageHint: "h5", text: { literalString: "Vertical List" } } } },
        {
          id: "sg-list-vertical",
          component: {
            List: {
              direction: "vertical",
              children: {
                explicitList: ["sg-list-v-item-1", "sg-list-v-item-2", "sg-list-v-item-3"]
              }
            }
          }
        },
        { id: "sg-list-v-item-1", component: { Text: { usageHint: "body", text: { literalString: "List item 1" } } } },
        { id: "sg-list-v-item-2", component: { Text: { usageHint: "body", text: { literalString: "List item 2" } } } },
        { id: "sg-list-v-item-3", component: { Text: { usageHint: "body", text: { literalString: "List item 3" } } } },
        { id: "sg-list-h-label", component: { Text: { usageHint: "h5", text: { literalString: "Horizontal List" } } } },
        {
          id: "sg-list-horizontal",
          component: {
            List: {
              direction: "horizontal",
              children: {
                explicitList: ["sg-list-h-item-1", "sg-list-h-item-2", "sg-list-h-item-3"]
              }
            }
          }
        },
        { id: "sg-list-h-item-1", component: { Card: { child: "sg-list-h-text-1" } } },
        { id: "sg-list-h-text-1", component: { Text: { usageHint: "body", text: { literalString: "Card A" } } } },
        { id: "sg-list-h-item-2", component: { Card: { child: "sg-list-h-text-2" } } },
        { id: "sg-list-h-text-2", component: { Text: { usageHint: "body", text: { literalString: "Card B" } } } },
        { id: "sg-list-h-item-3", component: { Card: { child: "sg-list-h-text-3" } } },
        { id: "sg-list-h-text-3", component: { Text: { usageHint: "body", text: { literalString: "Card C" } } } },


        // ━━━ MODAL ━━━
        {
          id: "section-modal",
          component: { Text: { usageHint: "h2", text: { literalString: "Modal" } } }
        },
        {
          id: "modal-card",
          component: { Card: { child: "sg-modal" } }
        },
        {
          id: "sg-modal",
          component: {
            Modal: {
              entryPointChild: "sg-modal-trigger",
              contentChild: "sg-modal-content"
            }
          }
        },
        {
          id: "sg-modal-trigger",
          component: {
            Button: {
              child: "sg-modal-trigger-text",
              action: { name: "openModal", context: [] }
            }
          }
        },
        { id: "sg-modal-trigger-text", component: { Text: { text: { literalString: "Open Modal" } } } },
        {
          id: "sg-modal-content",
          component: {
            Column: {
              children: {
                explicitList: ["sg-modal-title", "sg-modal-body"]
              }
            }
          }
        },
        { id: "sg-modal-title", component: { Text: { usageHint: "h3", text: { literalString: "Modal Title" } } } },
        { id: "sg-modal-body", component: { Text: { usageHint: "body", text: { literalString: "This is the modal content. Click outside or press Escape to close." } } } },

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
