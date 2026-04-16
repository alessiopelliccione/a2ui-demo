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

// Single source of truth for colors enforced by the engine
export const DesignSystemConfig = {
  primaryColor: "#10B981", 
  font: "Geist"
};

export const theme: v0_8.Types.Theme = {
  additionalStyles: {
    Button: {
      fontSize: "15px",
      fontWeight: "600",
      cursor: "pointer",
      transition: "all 0.2s ease",
    },
    Text: {
      h1: { fontSize: "48px", lineHeight: "1.1", marginBottom: "16px" },
      h2: { fontSize: "32px", marginBottom: "12px" },
      h3: { fontSize: "24px" },
      body: { lineHeight: "1.6", fontSize: "16px" },
      h4: {},
      h5: {},
      caption: {}
    },
    Card: {
      borderRadius: "20px",
      padding: "32px",
      boxShadow: "0 8px 32px rgba(0, 0, 0, 0.05)",
      background: "#ffffff"
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
      "color-bgc-p50": true,
      "color-c-p100": true,
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
      h1: { "typography-sz-hs": true, "typography-w-700": true },
      h2: { "typography-sz-tl": true, "typography-w-600": true },
      h3: { "typography-sz-tm": true, "typography-w-600": true },
      h4: { "typography-sz-bl": true, "typography-w-600": true },
      h5: { "typography-sz-bm": true, "typography-w-600": true },
      body: { "typography-sz-bl": true },
      caption: { "typography-sz-bs": true },
    },
    TextField: { element: {}, label: {}, container: {} },
    Video: {},
  },
  elements: {
    a: { "color-c-p60": true },
    audio: {},
    body: { "typography-f-s": true },
    button: { "border-br-3": true },
    h1: {},
    h2: {},
    h3: {},
    h4: {},
    h5: {},
    iframe: {},
    input: { "border-br-2": true, "border-bw-1": true, "border-bs-s": true, "color-bc-n30": true, "layout-p-2": true },
    p: {},
    pre: {},
    textarea: {},
    video: {},
  },
  markdown: {
    p: ["typography-f-s"],
    h1: ["typography-w-700"],
    h2: [], h3: [], h4: [], h5: [], ul: [], ol: [], li: [], a: [], strong: [], em: [],
  }
};
