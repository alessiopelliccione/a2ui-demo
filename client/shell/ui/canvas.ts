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

@customElement("a2ui-canvas")
export class Canvas extends LitElement {
  @property({ type: Boolean }) 
  accessor requesting = false;

  @property({ type: String }) 
  accessor loadingText = "Awaiting an answer...";

  @property({ type: Boolean }) 
  accessor hasSurfaces = false;

  static styles = css`
    :host {
      flex: 1;
      height: 100vh;
      overflow-y: auto;
      padding: 80px; /* Aumentato per dare respiro */
      background: #fdfdfd; /* Grigio quasi bianco per staccare dalla sidebar */
      display: flex;
      flex-direction: column;
      position: relative;
      box-sizing: border-box;

      /* FORZA IL TESTO SCURO NEL CANVAS (TEMA LIGHT) */
      --n-10: #111827;
      --n-20: #1f2937;
      --n-30: #374151;
      --n-40: #4b5563;
      --n-50: #6b7280;
      --n-80: #111827;
      --n-90: #000000;
      --n-100: #ffffff;
    }

    /* Contenitore interno per centrare senza tagliare */
    ::slotted(*) {
      width: 100%;
      max-width: 1000px;
      margin: 0 auto;
    }

    .pending {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 24px;
      position: absolute;
      top: 0;
      left: 0;
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(8px);
      z-index: 5;
    }

    .spinner {
      width: 32px;
      height: 32px;
      border: 2px solid #e5e7eb;
      border-top-color: #111827;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }

    .loading-text {
      color: #6b7280;
      font-size: 13px;
      font-weight: 400;
      font-family: 'Geist', sans-serif;
    }

    .idle-state {
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: rgba(0, 0, 0, 0.05);
      text-transform: uppercase;
      letter-spacing: 5px;
      font-size: 24px;
      font-family: 'Geist', sans-serif;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    ::slotted(#surfaces) {
      width: 100%;
      max-width: 1000px;
      display: flex;
      flex-direction: column;
      gap: 48px;
    }
  `;

  render() {
    if (this.requesting) {
      return html`
        <div class="pending">
          <div class="spinner"></div>
          <div class="loading-text">${this.loadingText}</div>
        </div>
      `;
    }

    if (!this.hasSurfaces) {
      return html`<div class="idle-state">Canvas Idle</div>`;
    }

    return html`<slot></slot>`;
  }
}
