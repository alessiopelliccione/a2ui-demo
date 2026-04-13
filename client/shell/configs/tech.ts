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
  title: "Insurance Assistant",
  heroImage: "",
  heroImageDark: "",
  background: "",
  placeholder: "How can I help you today? Ask about policies, claims, coverage...",
  loadingText: [
    "Analyzing your request...",
    "Checking available options...",
    "Preparing your answer...",
  ],
  serverUrl: "http://localhost:10003",
};
