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
      background: "#ffffff",
      color: "#000000",
      border: "none",
      padding: "20px 40px",
      fontSize: "18px",
      fontWeight: "700",
      borderRadius: "12px",
      cursor: "pointer",
      boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      textTransform: "none",
    },
    Text: {
      h1: {
        color: "#ffffff",
        fontFamily: "var(--font-family)",
        fontWeight: "800",
        letterSpacing: "-0.05em",
        lineHeight: "1",
        fontSize: "64px",
        marginBottom: "24px",
        textAlign: "center",
        display: "block",
      },
      h2: {
        color: "#ffffff",
        fontFamily: "var(--font-family)",
        fontWeight: "700",
        letterSpacing: "-0.03em",
        fontSize: "48px",
        marginBottom: "20px",
      },
      h3: {
        color: "#ffffff",
        fontWeight: "600",
        fontSize: "32px",
      },
      h4: { color: "#ffffff" },
      h5: { color: "#ffffff" },
      body: {
        fontFamily: "var(--font-family)",
        color: "#e5e5e5",
        lineHeight: "1.6",
        fontSize: "18px",
        textAlign: "center",
        maxWidth: "800px",
        margin: "0 auto",
      },
      caption: { color: "#a3a3a3" },
    },
    Card: {
      background: "#171717",
      border: "1px solid #262626",
      borderRadius: "24px",
      padding: "40px",
    },
  },
  components: {
    AudioPlayer: {},
    Button: {
      "layout-pt-4": true,
      "layout-pb-4": true,
      "layout-pl-8": true,
      "layout-pr-8": true,
      "border-br-3": true,
      "color-bgc-n100": true,
      "color-c-n0": true,
    },
    Card: { "border-br-5": true, "layout-p-10": true },
    CheckBox: { element: {}, label: {}, container: {} },
    Column: { "layout-g-8": true, "layout-al-c": true },
    DateTimeInput: { element: {}, label: {}, container: {} },
    Divider: {},
    Icon: {},
    Image: { all: {}, avatar: {}, header: {}, icon: {}, largeFeature: {}, mediumFeature: {}, smallFeature: {} },
    List: {},
    Modal: { element: {}, backdrop: {} },
    MultipleChoice: { element: {}, label: {}, container: {} },
    Row: { "layout-g-8": true, "layout-al-c": true },
    Slider: { element: {}, label: {}, container: {} },
    Tabs: { element: {}, controls: { all: {}, selected: {} }, container: {} },
    Text: {
      all: { "layout-w-100": true, "color-c-n100": true },
      h1: { "typography-sz-hs": true, "typography-w-700": true, "color-c-n100": true, "layout-as-c": true },
      h2: { "typography-sz-tl": true, "typography-w-700": true, "color-c-n100": true },
      h3: { "typography-sz-tl": true, "typography-w-600": true, "color-c-n90": true },
      h4: { "typography-sz-bl": true, "typography-w-600": true, "color-c-n90": true },
      h5: { "typography-sz-bm": true, "typography-w-600": true, "color-c-n90": true },
      body: { "typography-sz-bl": true, "color-c-n90": true, "layout-as-c": true },
      caption: { "typography-sz-bs": true, "color-c-n80": true },
    },
    TextField: { element: {}, label: {}, container: {} },
    Video: {},
  },
  elements: {
    a: {},
    audio: {},
    body: { "color-c-n90": true, "typography-f-s": true },
    button: { "border-br-3": true, "layout-p-4": true },
    h1: {},
    h2: {},
    h3: {},
    h4: {},
    h5: {},
    iframe: {},
    input: {},
    p: {},
    pre: {},
    textarea: {},
    video: {},
  },
  markdown: {
    p: ["color-c-n80", "typography-f-s"],
    h1: ["color-c-n100", "typography-w-700"],
    h2: [],
    h3: [],
    h4: [],
    h5: [],
    ul: [],
    ol: [],
    li: [],
    a: [],
    strong: [],
    em: [],
  }
};
