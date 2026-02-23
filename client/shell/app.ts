/*
 Copyright 2025 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 */

import { SignalWatcher } from "@lit-labs/signals";
import { provide } from "@lit/context";
import { LitElement, html, css, nothing, HTMLTemplateResult, unsafeCSS } from "lit";
import { customElement, state } from "lit/decorators.js";
import { theme as uiTheme } from "./theme/default-theme.js";
import { A2UIClient } from "./client.js";
import { SnackbarAction, SnackbarMessage, SnackbarUUID, SnackType } from "./types/types.js";
import { type Snackbar } from "./ui/snackbar.js";
import { repeat } from "lit/directives/repeat.js";
import { v0_8 } from "@a2ui/lit";
import * as UI from "@a2ui/lit/ui";

// Refactored UI Components
import "./ui/sidebar.js";
import "./ui/canvas.js";
import "./ui/ui.js";

import { AppConfig } from "./configs/types.js";
import { config as techConfig } from "./configs/tech.js";

const configs: Record<string, AppConfig> = { tech: techConfig };

@customElement("a2ui-shell")
export class A2UILayoutEditor extends SignalWatcher(LitElement) {
  @provide({ context: UI.Context.themeContext })
  accessor theme: v0_8.Types.Theme = uiTheme;

  @state() accessor #requesting = false;
  @state() accessor #error: string | null = null;
  @state() accessor #lastMessages: v0_8.Types.ServerToClientMessage[] = [];
  @state() accessor config: AppConfig = configs.tech;
  @state() accessor #loadingTextIndex = 0;
  
  #loadingInterval: number | undefined;
  #processor = v0_8.Data.createSignalA2uiMessageProcessor();
  #a2uiClient = new A2UIClient();
  #snackbar: Snackbar | undefined = undefined;
  #pendingSnackbarMessages: Array<{ message: SnackbarMessage; replaceAll: boolean; }> = [];

  static styles = css`
    :host {
      display: flex;
      flex-direction: row;
      width: 100vw;
      height: 100vh;
      background: #000;
      overflow: hidden;
      margin: 0;
      padding: 0;
    }

    #surfaces {
      width: 100%;
      max-width: 1000px;
      animation: fadeIn 0.4s ease-out;
      display: flex;
      flex-direction: column;
      gap: 48px;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  `;

  connectedCallback() {
    super.connectedCallback();
    const urlParams = new URLSearchParams(window.location.search);
    const appKey = urlParams.get("app") || "tech";
    this.config = configs[appKey] || configs.tech;
    if (this.config.theme) this.theme = this.config.theme;
    window.document.title = this.config.title;
    this.#a2uiClient = new A2UIClient(this.config.serverUrl);
  }

  render() {
    const surfaces = this.#processor.getSurfaces();
    
    return html`
      <a2ui-sidebar 
        .config=${this.config} 
        .requesting=${this.#requesting}
        .renderedCount=${surfaces.size}
        @submit-prompt=${this.#handlePrompt}
      ></a2ui-sidebar>

      <a2ui-canvas 
        .requesting=${this.#requesting}
        .loadingText=${this.#getLoadingText()}
        .hasSurfaces=${surfaces.size > 0}
      >
        <section id="surfaces">
          ${repeat(surfaces, ([id]) => id, ([id, surface]) => html`
            <a2ui-surface
              .surfaceId=${id}
              .surface=${surface}
              .processor=${this.#processor}
              @a2uiaction=${this.#handleAction}
            ></a2ui-surface>
          `)}
        </section>
      </a2ui-canvas>
    `;
  }

  #getLoadingText() {
    if (Array.isArray(this.config.loadingText)) {
      return this.config.loadingText[this.#loadingTextIndex];
    }
    return this.config.loadingText || "Awaiting an answer...";
  }

  async #handlePrompt(evt: CustomEvent<{ body: string }>) {
    const message = evt.detail.body as unknown as v0_8.Types.A2UIClientEventMessage;
    await this.#sendAndProcessMessage(message);
  }

  async #handleAction(evt: v0_8.Events.StateEvent<"a2ui.action">) {
    const [target] = evt.composedPath();
    if (!(target instanceof HTMLElement)) return;

    const context: v0_8.Types.A2UIClientEventMessage["userAction"]["context"] = {};
    if (evt.detail.action.context) {
      for (const item of evt.detail.action.context) {
        if (item.value.literalBoolean) context[item.key] = item.value.literalBoolean;
        else if (item.value.literalNumber) context[item.key] = item.value.literalNumber;
        else if (item.value.literalString) context[item.key] = item.value.literalString;
        else if (item.value.path) {
          const path = this.#processor.resolvePath(item.value.path, evt.detail.dataContextPath);
          context[item.key] = this.#processor.getData(evt.detail.sourceComponent, path, evt.detail.action.name);
        }
      }
    }

    const message: v0_8.Types.A2UIClientEventMessage = {
      userAction: {
        name: evt.detail.action.name,
        surfaceId: evt.detail.sourceComponentId,
        sourceComponentId: target.id,
        timestamp: new Date().toISOString(),
        context,
      },
    };

    await this.#sendAndProcessMessage(message);
  }

  async #sendAndProcessMessage(request) {
    try {
      this.#requesting = true;
      this.#startLoadingAnimation();
      const messages = await this.#a2uiClient.send(request);
      this.#requesting = false;
      this.#stopLoadingAnimation();
      this.#lastMessages = messages;
      this.#processor.clearSurfaces();
      this.#processor.processMessages(messages);
    } catch (err) {
      this.#requesting = false;
      this.#stopLoadingAnimation();
    }
  }

  #startLoadingAnimation() {
    if (Array.isArray(this.config.loadingText)) {
      this.#loadingTextIndex = 0;
      this.#loadingInterval = window.setInterval(() => {
        this.#loadingTextIndex = (this.#loadingTextIndex + 1) % (this.config.loadingText as string[]).length;
      }, 2000);
    }
  }

  #stopLoadingAnimation() {
    if (this.#loadingInterval) {
      clearInterval(this.#loadingInterval);
      this.#loadingInterval = undefined;
    }
  }

  snackbar(message: string | HTMLTemplateResult, type: SnackType, actions: SnackbarAction[] = [], persistent = false, id = globalThis.crypto.randomUUID(), replaceAll = false) {
    if (!this.#snackbar) {
      this.#pendingSnackbarMessages.push({ message: { id, message, type, persistent, actions }, replaceAll });
      return;
    }
    return this.#snackbar.show({ id, message, type, persistent, actions }, replaceAll);
  }

  unsnackbar(id?: SnackbarUUID) {
    if (this.#snackbar) this.#snackbar.hide(id);
  }
}
