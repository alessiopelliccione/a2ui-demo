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
import { LitElement, html, css, nothing } from "lit";
import { customElement, state, query } from "lit/decorators.js";
import { theme as uiTheme, DesignSystemConfig } from "./theme/default-theme.js";
import { A2UIClient } from "./client.js";
import { repeat } from "lit/directives/repeat.js";
import { v0_8 } from "@a2ui/lit";
import * as UI from "@a2ui/lit/ui";

import { AppConfig } from "./configs/types.js";
import { config as techConfig } from "./configs/tech.js";

const configs: Record<string, AppConfig> = { tech: techConfig };

interface ChatEntry {
  id: string;
  role: 'user' | 'assistant';
  text: string;
}

@customElement("a2ui-shell")
export class A2UIShell extends SignalWatcher(LitElement) {
  @provide({ context: UI.Context.themeContext })
  accessor theme: v0_8.Types.Theme = uiTheme;

  @state() accessor #requesting = false;
  @state() accessor #chatHistory: ChatEntry[] = [];
  @state() accessor #canvasVisible = false;
  @state() accessor #loadingTextIndex = 0;
  @state() accessor config: AppConfig = configs.tech;

  #turnCounter = 0;
  #loadingInterval: number | undefined;
  #processor = v0_8.Data.createSignalA2uiMessageProcessor();
  #a2uiClient = new A2UIClient();

  @query('#chat-messages') accessor #chatMessagesEl!: HTMLElement;

  static styles = css`
    :host {
      display: flex;
      flex-direction: column;
      width: 100vw;
      height: 100vh;
      background: #f4f5f7;
      font-family: 'Geist', sans-serif;
      overflow: hidden;
    }

    /* ── Header ── */
    #chat-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 14px 24px;
      border-bottom: 1px solid #e5e7eb;
      background: white;
      flex-shrink: 0;
    }
    #chat-header .logo {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: #10B981;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 14px;
      flex-shrink: 0;
    }
    #chat-header h1 {
      margin: 0;
      font-size: 17px;
      font-weight: 600;
      color: #111827;
      flex: 1;
    }
    .header-link {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 8px;
      border: 1px solid #e5e7eb;
      background: #f9fafb;
      color: #374151;
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      font-family: 'Geist', sans-serif;
      transition: background 0.15s;
      flex-shrink: 0;
    }
    .header-link:hover { background: #f3f4f6; }
    .header-link .material-symbols-outlined { font-size: 18px; }

    /* ── Main content (split layout) ── */
    #main-content {
      flex: 1;
      display: flex;
      overflow: hidden;
    }

    /* ── Chat panel (left) ── */
    #chat-panel {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-width: 0;
    }
    #chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .empty-state {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      color: #9ca3af;
      font-size: 16px;
      text-align: center;
    }
    .empty-state .agent-icon {
      width: 56px;
      height: 56px;
      border-radius: 16px;
      background: #10B981;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
    }

    /* ── Message bubbles ── */
    .message {
      display: flex;
      flex-direction: column;
      max-width: 85%;
    }
    .message.user-message {
      align-self: flex-end;
    }
    .message.assistant-message {
      align-self: flex-start;
    }
    .bubble {
      padding: 12px 16px;
      border-radius: 16px;
      font-size: 15px;
      line-height: 1.5;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .user-message .bubble {
      background: #10B981;
      color: white;
      border-bottom-right-radius: 4px;
    }
    .assistant-message .bubble {
      background: white;
      color: #1f2937;
      border: 1px solid #e5e7eb;
      border-bottom-left-radius: 4px;
    }

    /* ── Typing indicator ── */
    .typing-indicator {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 12px 16px;
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      border-bottom-left-radius: 4px;
      color: #6b7280;
      font-size: 14px;
    }
    .spinner {
      width: 18px;
      height: 18px;
      border: 2px solid #e5e7eb;
      border-top-color: #10B981;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* ── Input bar ── */
    #chat-input-bar {
      padding: 14px 24px;
      border-top: 1px solid #e5e7eb;
      background: white;
      flex-shrink: 0;
    }
    .input-wrapper {
      display: flex;
      align-items: center;
      gap: 10px;
      max-width: 900px;
      margin: 0 auto;
    }
    .input-wrapper textarea {
      flex: 1;
      resize: none;
      border: 1px solid #d1d5db;
      border-radius: 12px;
      padding: 10px 16px;
      font-size: 15px;
      font-family: 'Geist', sans-serif;
      line-height: 1.4;
      outline: none;
      height: 44px;
      max-height: 120px;
      transition: border-color 0.2s;
    }
    .input-wrapper textarea:focus {
      border-color: #10B981;
    }
    .input-wrapper textarea:disabled {
      opacity: 0.6;
    }
    .send-btn {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      border: none;
      background: #10B981;
      color: white;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: opacity 0.2s;
    }
    .send-btn:hover { opacity: 0.85; }
    .send-btn:disabled { opacity: 0.4; cursor: not-allowed; }

    /* ── Canvas panel (right) ── */
    #canvas-panel {
      width: 55%;
      max-width: 55%;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      border-left: 1px solid #e5e7eb;
      background: #f9fafb;
    }
    .canvas-titlebar {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 10px 16px;
      background: #f3f4f6;
      border-bottom: 1px solid #e5e7eb;
      flex-shrink: 0;
    }
    .canvas-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #d1d5db;
    }
    .canvas-dot.red { background: #ef4444; }
    .canvas-dot.yellow { background: #f59e0b; }
    .canvas-dot.green { background: #10b981; }
    .canvas-title {
      margin-left: 8px;
      font-size: 13px;
      font-weight: 500;
      color: #6b7280;
    }
    .canvas-body {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      background: white;
    }
    .canvas-body a2ui-surface {
      max-width: 100%;
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
    // Get the active surface (single persistent surface, no rewriting)
    const surfaces = this.#processor.getSurfaces();
    let activeSurfaceId: string | null = null;
    let activeSurface: any = null;
    for (const [id, surface] of surfaces) {
      activeSurfaceId = id;
      activeSurface = surface;
      break;
    }

    return html`
      <div id="chat-header">
        <div class="logo">
          <span class="material-symbols-outlined" style="font-size:20px">shield</span>
        </div>
        <h1>${this.config.title}</h1>
        <a href="components.html" class="header-link">
          <span class="material-symbols-outlined">palette</span>
          Components
        </a>
      </div>

      <div id="main-content">
        <div id="chat-panel">
          <div id="chat-messages">
            ${this.#chatHistory.length === 0 && !this.#requesting ? html`
              <div class="empty-state">
                <div class="agent-icon">
                  <span class="material-symbols-outlined">shield</span>
                </div>
                <div>${this.config.placeholder}</div>
              </div>
            ` : nothing}

            ${repeat(this.#chatHistory, (e) => e.id, (entry) => {
              if (entry.role === 'user') {
                return html`
                  <div class="message user-message">
                    <div class="bubble">${entry.text}</div>
                  </div>`;
              }
              return html`
                <div class="message assistant-message">
                  <div class="bubble">${entry.text}</div>
                </div>`;
            })}

            ${this.#requesting ? html`
              <div class="message assistant-message">
                <div class="typing-indicator">
                  <div class="spinner"></div>
                  <span>${this.#getLoadingText()}</span>
                </div>
              </div>
            ` : nothing}
          </div>

          <div id="chat-input-bar">
            <div class="input-wrapper">
              <textarea
                id="body"
                placeholder=${this.config.placeholder}
                ?disabled=${this.#requesting}
                @keydown=${this.#handleKeyDown}
                rows="1"
              ></textarea>
              <button
                class="send-btn"
                ?disabled=${this.#requesting}
                @click=${this.#handleSend}
              >
                <span class="material-symbols-outlined">send</span>
              </button>
            </div>
          </div>
        </div>

        ${this.#canvasVisible && activeSurface ? html`
          <div id="canvas-panel">
            <div class="canvas-titlebar">
              <div class="canvas-dot red"></div>
              <div class="canvas-dot yellow"></div>
              <div class="canvas-dot green"></div>
              <span class="canvas-title">Interactive View</span>
            </div>
            <div class="canvas-body">
              <a2ui-surface
                .surfaceId=${activeSurfaceId}
                .surface=${activeSurface}
                .processor=${this.#processor}
                @a2uiaction=${(evt: v0_8.Events.StateEvent<"a2ui.action">) => this.#handleAction(evt, activeSurfaceId!)}
              ></a2ui-surface>
            </div>
          </div>
        ` : nothing}
      </div>
    `;
  }

  #getLoadingText() {
    if (Array.isArray(this.config.loadingText)) {
      return this.config.loadingText[this.#loadingTextIndex];
    }
    return this.config.loadingText || "Thinking...";
  }

  #handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      this.#handleSend();
    }
  }

  #handleSend() {
    const textarea = this.renderRoot.querySelector('#body') as HTMLTextAreaElement;
    if (!textarea) return;
    const text = textarea.value.trim();
    if (!text) return;
    textarea.value = '';

    const message = text as unknown as v0_8.Types.A2UIClientEventMessage;
    this.#sendAndProcessMessage(message, text);
  }

  async #handleAction(evt: v0_8.Events.StateEvent<"a2ui.action">, surfaceId: string) {
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
          context[item.key] = this.#processor.getData(evt.detail.sourceComponent, path, surfaceId);
        }
      }
    }

    // External links: handle locally
    if (evt.detail.action.name === "open_url" && context.url) {
      window.open(context.url as string, "_blank", "noopener,noreferrer");
      return;
    }

    const message: v0_8.Types.A2UIClientEventMessage = {
      userAction: {
        name: evt.detail.action.name,
        surfaceId,
        sourceComponentId: target.id,
        timestamp: new Date().toISOString(),
        context,
      },
    };

    // Actions don't show as user messages in chat
    await this.#sendAndProcessMessage(message, null);
  }

  async #sendAndProcessMessage(request: v0_8.Types.A2UIClientEventMessage | string, userText: string | null) {
    try {
      this.#requesting = true;
      this.#startLoadingAnimation();
      this.#turnCounter++;

      // Add user message to chat (only for typed messages, not button actions)
      if (userText) {
        this.#chatHistory = [...this.#chatHistory, {
          id: `user-${this.#turnCounter}`,
          role: 'user',
          text: userText,
        }];
        this.#scrollToBottom();
      }

      const response = await this.#a2uiClient.send(request);

      // Process A2UI messages — no surfaceId rewriting, use original IDs
      if (response.messages.length > 0) {
        for (const msg of response.messages) {
          if (msg.beginRendering) {
            msg.beginRendering.styles = { ...DesignSystemConfig };
          }
        }
        this.#processor.processMessages(response.messages);
        this.#canvasVisible = true;
      }

      // Add assistant text to chat (if any)
      if (response.text) {
        this.#chatHistory = [...this.#chatHistory, {
          id: `assistant-${this.#turnCounter}`,
          role: 'assistant',
          text: response.text,
        }];
      }

      this.#requesting = false;
      this.#stopLoadingAnimation();
      this.#scrollToBottom();
    } catch (err) {
      console.error('A2UI request failed:', err);
      this.#requesting = false;
      this.#stopLoadingAnimation();
      this.#chatHistory = [...this.#chatHistory, {
        id: `error-${this.#turnCounter}`,
        role: 'assistant',
        text: 'Sorry, something went wrong. Please try again.',
      }];
    }
  }

  #scrollToBottom() {
    this.updateComplete.then(() => {
      const el = this.#chatMessagesEl;
      if (el) el.scrollTop = el.scrollHeight;
    });
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
}
