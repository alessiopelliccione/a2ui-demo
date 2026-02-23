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

import { AppConfig } from "./types.js";

export const config: AppConfig = {
  key: "tech",
  title: "AI UI Builder",
  heroImage: "", // Rimosso hero image del ristorante
  heroImageDark: "",
  background: `
    radial-gradient(
      at 0% 0%,
      rgba(0, 255, 127, 0.15) 0px,
      transparent 50%
    ),
    radial-gradient(
      at 100% 0%,
      rgba(0, 229, 255, 0.15) 0px,
      transparent 50%
    ),
    radial-gradient(
      at 100% 100%,
      rgba(123, 31, 162, 0.15) 0px,
      transparent 50%
    ),
    radial-gradient(
      at 0% 100%,
      rgba(255, 64, 129, 0.15) 0px,
      transparent 50%
    ),
    #0a0a0b
  `,
  placeholder: "Generate a futuristic KPI dashboard...",
  loadingText: [
    "Compiling UI components...",
    "Optimizing layout...",
    "Synthesizing visual assets...",
    "Finalizing render...",
  ],
  serverUrl: "http://localhost:10003",
};
