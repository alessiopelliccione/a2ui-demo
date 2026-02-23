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

import { LitElement, html, css } from "lit";
import { customElement, property } from "lit/decorators.js";
import { AppConfig } from "../configs/types.js";

@customElement("a2ui-sidebar")
export class Sidebar extends LitElement {
  @property({ type: Object }) 
  accessor config!: AppConfig;

  @property({ type: Boolean }) 
  accessor requesting = false;

  @property({ type: Number })
  accessor renderedCount = 0;

  static styles = css`
    :host {
      display: block;
      width: 400px;
      min-width: 400px;
      height: 100vh;
      background: #f9fafb;
      border-right: 1px solid #e5e7eb;
      box-sizing: border-box;
    }

    .sidebar-container {
      padding: 48px 32px;
      height: 100%;
      display: flex;
      flex-direction: column;
      gap: 48px;
      box-sizing: border-box;
    }

    header {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    header h1 {
      color: #111827;
      font-weight: 600;
      font-size: 1.25rem;
      margin: 0;
      letter-spacing: -0.02em;
      font-family: 'Geist', sans-serif;
    }

    .logo {
      width: 44px;
      height: 44px;
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #111827;
      font-weight: 700;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
      font-size: 18px;
    }

    .prompt-section {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .prompt-section h3 {
      font-size: 11px;
      font-weight: 600;
      color: #6b7280;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin: 0 4px;
    }

    .input-card {
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 20px;
      padding: 24px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
      display: flex;
      flex-direction: column;
      gap: 20px;
      transition: all 0.3s ease;
    }

    .input-card:focus-within {
      border-color: #4f46e5;
      box-shadow: 0 10px 30px rgba(79, 70, 229, 0.08);
      transform: translateY(-2px);
    }

    textarea {
      width: 100%;
      border: none;
      background: transparent;
      font-size: 16px;
      color: #111827;
      font-family: 'Geist', sans-serif;
      outline: none;
      resize: none;
      line-height: 1.6;
      min-height: 80px;
    }

    textarea::placeholder {
      color: #9ca3af;
    }

    .actions {
      display: flex;
      justify-content: flex-end;
      align-items: center;
    }

    button {
      background: #111827;
      color: #ffffff;
      border: none;
      padding: 12px 24px;
      border-radius: 12px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: 'Geist', sans-serif;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    button:disabled {
      background: #9ca3af;
      cursor: not-allowed;
      box-shadow: none;
    }

    button:hover:not([disabled]) {
      background: #000000;
      transform: scale(1.02);
    }

    .status-panel {
      margin-top: auto;
      font-size: 11px;
      color: #9ca3af;
      display: flex;
      justify-content: space-between;
      border-top: 1px solid #e5e7eb;
      padding-top: 24px;
    }

    .status-dot {
      display: inline-block;
      width: 8px;
      height: 8px;
      background: #10b981;
      border-radius: 50%;
      margin-right: 6px;
    }

    .status-dot.working {
      background: #f59e0b;
      animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
      0% { opacity: 1; }
      50% { opacity: 0.4; }
      100% { opacity: 1; }
    }
  `;

  render() {
    return html`
      <div class="sidebar-container">
        <header>
          <div class="logo">A2</div>
          <h1>${this.config?.title || "Studio"}</h1>
        </header>

        <div class="prompt-section">
          <h3>Prompt AI</h3>
          <form @submit=${this._handleSubmit}>
            <div class="input-card">
              <textarea
                required
                placeholder="${this.config?.placeholder || "Describe the UI you want to build..."}"
                autocomplete="off"
                id="body"
                name="body"
                ?disabled=${this.requesting}
                @keydown=${this._handleKeyDown}
              ></textarea>
              
              <div class="actions">
                <button type="submit" ?disabled=${this.requesting}>
                  ${this.requesting ? 'Executing...' : 'Run Command'}
                </button>
              </div>
            </div>
          </form>
        </div>

        <div class="status-panel">
          <span>
            <span class="status-dot ${this.requesting ? 'working' : ''}"></span>
            ${this.requesting ? 'Processing...' : 'System Ready'}
          </span>
          <span>${this.renderedCount} Units</span>
        </div>
      </div>
    `;
  }

  private _handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      this._handleSubmit(e);
    }
  }

  private _handleSubmit(evt: Event) {
    evt.preventDefault();
    const form = this.shadowRoot?.querySelector('form');
    if (!form) return;

    const textarea = form.querySelector('textarea');
    const body = textarea?.value || "";
    if (!body.trim()) return;
    
    this.dispatchEvent(new CustomEvent("submit-prompt", {
      detail: { body },
      bubbles: true,
      composed: true
    }));

    if (textarea) textarea.value = '';
  }
}
