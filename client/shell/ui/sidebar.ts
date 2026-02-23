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

import { LitElement, html, css, nothing } from "lit";
import { customElement, property } from "lit/decorators.js";
import { styleMap } from "lit/directives/style-map.js";
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
      width: 400px;
      min-width: 400px;
      height: 100vh;
      border-right: 1px solid #262626;
      display: flex;
      flex-direction: column;
      padding: 40px;
      background: #000;
      gap: 40px;
      box-sizing: border-box;
    }

    header {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    header h1 {
      color: #fff;
      font-weight: 600;
      font-size: 1.1rem;
      margin: 0;
      letter-spacing: -0.02em;
      font-family: 'Geist', sans-serif;
    }

    .logo {
      width: 40px;
      height: 40px;
      background: #171717;
      border: 1px solid #262626;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: bold;
    }

    form {
      display: flex;
      flex-direction: column;
      gap: 24px;
      width: 100%;
    }

    .input-container {
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
      border: 1px solid #262626;
      background: #0a0a0a;
      padding: 16px;
      border-radius: 12px;
      transition: border-color 0.2s ease;
    }

    .input-container:focus-within {
      border-color: #404040;
    }

    .label {
      color: #737373;
      font-size: 11px;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    input {
      display: block;
      width: 100%;
      border: none;
      background: transparent;
      font-size: 15px;
      color: #fff;
      font-family: 'Geist', sans-serif;
      outline: none;
    }

    input::placeholder {
      color: #404040;
    }

    button {
      align-self: flex-end;
      background: #fff;
      color: #000;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: 'Geist', sans-serif;
    }

    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    button:hover:not([disabled]) {
      background: #e5e5e5;
    }

    .status-panel {
      margin-top: auto;
      font-size: 10px;
      color: #404040;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      border-top: 1px solid #171717;
      padding-top: 20px;
    }
  `;

  render() {
    return html`
      <header>
        <div class="logo">A2</div>
        <h1>${this.config?.title || "Studio"}</h1>
      </header>

      <form @submit=${this._handleSubmit}>
        <div class="input-container">
          <span class="label">Prompt AI</span>
          <input
            required
            placeholder="${this.config?.placeholder || "Describe your UI..."}"
            autocomplete="off"
            id="body"
            name="body"
            type="text"
            ?disabled=${this.requesting}
          />
          <button type="submit" ?disabled=${this.requesting}>
            ${this.requesting ? 'Executing...' : 'Run Command'}
          </button>
        </div>
      </form>

      <div class="status-panel">
        Status: ${this.requesting ? 'Processing' : 'Idle'} | 
        Rendered: ${this.renderedCount} Units
      </div>
    `;
  }

  private _handleSubmit(evt: Event) {
    evt.preventDefault();
    const form = evt.target as HTMLFormElement;
    const data = new FormData(form);
    const body = data.get("body") ?? "";
    
    this.dispatchEvent(new CustomEvent("submit-prompt", {
      detail: { body },
      bubbles: true,
      composed: true
    }));

    const input = form.querySelector('input');
    if (input) input.value = '';
  }
}
