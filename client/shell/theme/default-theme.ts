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

import { v0_8 } from "@a2ui/lit";

export const theme: v0_8.Types.Theme = {
  additionalStyles: {
    Button: {
      background: "#111827",
      color: "#ffffff",
      border: "none",
      padding: "14px 28px",
      fontSize: "15px",
      fontWeight: "600",
      borderRadius: "12px",
      cursor: "pointer",
      boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
      transition: "all 0.2s ease",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      gap: "8px",
      /* FORZA IL BIANCO PER TUTTI I COMPONENTI FIGLI DEL BOTTONE */
      "--n-10": "#ffffff",
      "--n-20": "#ffffff",
      "--n-30": "#ffffff",
      "--n-40": "#ffffff",
      "--n-50": "#ffffff",
      "--n-60": "#ffffff",
      "--n-70": "#ffffff",
      "--n-80": "#ffffff",
      "--n-90": "#ffffff",
    },
    Text: {
      h1: {
        color: "#111827",
        fontWeight: "700",
        letterSpacing: "-0.04em",
        fontSize: "48px",
        lineHeight: "1.1",
        marginBottom: "16px",
      },
      h2: {
        color: "#111827",
        fontWeight: "600",
        letterSpacing: "-0.03em",
        fontSize: "32px",
        marginBottom: "12px",
      },
      h3: {
        color: "#111827",
        fontWeight: "600",
        fontSize: "24px",
      },
      body: {
        color: "#4b5563",
        lineHeight: "1.6",
        fontSize: "16px",
      },
      h4: { color: "#111827" },
      h5: { color: "#4b5563" },
      caption: { color: "#9ca3af" },
    },
    Card: {
      background: "#ffffff",
      border: "1px solid #e5e7eb",
      borderRadius: "20px",
      padding: "32px",
      boxShadow: "0 10px 25px rgba(0, 0, 0, 0.03)",
    },
  },
  components: {
    AudioPlayer: {},
    Button: {
      "layout-pt-3": true,
      "layout-pb-3": true,
      "layout-pl-6": true,
      "layout-pr-6": true,
      "border-br-3": true,
      "color-bgc-n90": true,
      "color-c-n0": true, 
    },
    Card: { "border-br-5": true, "layout-p-8": true, "color-bgc-n0": true },
    CheckBox: { element: {}, label: {}, container: {} },
    Column: { "layout-g-6": true },
    DateTimeInput: { element: {}, label: {}, container: {} },
    Divider: { "color-bgc-n20": true, "layout-h-px": true, "layout-mt-4": true, "layout-mb-4": true },
    Icon: {},
    Image: { 
      all: { "border-br-3": true, "layout-el-cv": true },
      avatar: { "is-avatar": true, "border-br-50pc": true },
      icon: {},
      smallFeature: {},
      mediumFeature: {},
      largeFeature: {},
      header: {},
    },
    List: { "layout-g-6": true },
    Modal: { element: {}, backdrop: {} },
    MultipleChoice: { element: {}, label: {}, container: {} },
    Row: { "layout-g-4": true, "layout-al-c": true },
    Slider: { element: {}, label: {}, container: {} },
    Tabs: { element: {}, controls: { all: {}, selected: {} }, container: {} },
    Text: {
      all: { "layout-w-100": true },
      h1: { "typography-sz-hs": true, "typography-w-700": true, "color-c-n90": true },
      h2: { "typography-sz-tl": true, "typography-w-600": true, "color-c-n90": true },
      h3: { "typography-sz-tm": true, "typography-w-600": true, "color-c-n90": true },
      h4: { "typography-sz-bl": true, "typography-w-600": true, "color-c-n90": true },
      h5: { "typography-sz-bm": true, "typography-w-600": true, "color-c-n90": true },
      body: { "typography-sz-bl": true, "color-c-n60": true },
      caption: { "typography-sz-bs": true, "color-c-n50": true },
    },
    TextField: { element: {}, label: {}, container: {} },
    Video: {},
  },
  elements: {
    a: { "color-c-p60": true },
    audio: {},
    body: { "color-c-n80": true, "typography-f-s": true },
    button: { "border-br-3": true, "color-c-n0": true },
    h1: { "color-c-n90": true },
    h2: { "color-c-n90": true },
    h3: { "color-c-n90": true },
    h4: { "color-c-n90": true },
    h5: { "color-c-n90": true },
    iframe: {},
    input: { "border-br-2": true, "border-bw-1": true, "border-bs-s": true, "color-bc-n30": true, "layout-p-2": true },
    p: { "color-c-n70": true },
    pre: {},
    textarea: {},
    video: {},
  },
  markdown: {
    p: ["color-c-n70", "typography-f-s"],
    h1: ["color-c-n90", "typography-w-700"],
    h2: [], h3: [], h4: [], h5: [], ul: [], ol: [], li: [], a: [], strong: [], em: [],
  }
};
