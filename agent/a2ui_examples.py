# Finance & Insurance UI Builder Examples for A2UI
# Demo for Generative Frontend / Server-Driven UI session

UI_BUILDER_EXAMPLES = """
---BEGIN FINANCE_PORTFOLIO_DASHBOARD---
Description: Use this example when the user asks for a financial dashboard, portfolio overview, or investment performance.
[
  {{ "beginRendering": {{ "surfaceId": "default", "root": "dashboard-root", "styles": {{ "primaryColor": "#10B981", "font": "Geist" }} }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "default",
    "components": [
      {{ "id": "dashboard-root", "component": {{ "Column": {{ "children": {{ "explicitList": ["dashboard-header", "kpi-row"] }} }} }} }},
      {{ "id": "dashboard-header", "component": {{ "Column": {{ "children": {{ "explicitList": ["dashboard-title", "dashboard-subtitle"] }} }} }} }},
      {{ "id": "dashboard-title", "component": {{ "Text": {{ "usageHint": "h1", "text": {{ "path": "/dashboard/title" }} }} }} }},
      {{ "id": "dashboard-subtitle", "component": {{ "Text": {{ "usageHint": "body", "text": {{ "path": "/dashboard/subtitle" }} }} }} }},
      {{ "id": "kpi-row", "component": {{ "Row": {{ "distribution": "spaceEvenly", "children": {{ "explicitList": ["kpi-card-1", "kpi-card-2", "kpi-card-3"] }} }} }} }},
      {{ "id": "kpi-card-1", "weight": 1, "component": {{ "Card": {{ "child": "kpi-content-1" }} }} }},
      {{ "id": "kpi-content-1", "component": {{ "Column": {{ "alignment": "center", "children": {{ "explicitList": ["kpi-value-1", "kpi-label-1", "kpi-trend-1"] }} }} }} }},
      {{ "id": "kpi-value-1", "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "path": "/kpis/0/value" }} }} }} }},
      {{ "id": "kpi-label-1", "component": {{ "Text": {{ "usageHint": "caption", "text": {{ "path": "/kpis/0/label" }} }} }} }},
      {{ "id": "kpi-trend-1", "component": {{ "Text": {{ "usageHint": "h5", "text": {{ "path": "/kpis/0/trend" }} }} }} }},
      {{ "id": "kpi-card-2", "weight": 1, "component": {{ "Card": {{ "child": "kpi-content-2" }} }} }},
      {{ "id": "kpi-content-2", "component": {{ "Column": {{ "alignment": "center", "children": {{ "explicitList": ["kpi-value-2", "kpi-label-2", "kpi-trend-2"] }} }} }} }},
      {{ "id": "kpi-value-2", "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "path": "/kpis/1/value" }} }} }} }},
      {{ "id": "kpi-label-2", "component": {{ "Text": {{ "usageHint": "caption", "text": {{ "path": "/kpis/1/label" }} }} }} }},
      {{ "id": "kpi-trend-2", "component": {{ "Text": {{ "usageHint": "h5", "text": {{ "path": "/kpis/1/trend" }} }} }} }},
      {{ "id": "kpi-card-3", "weight": 1, "component": {{ "Card": {{ "child": "kpi-content-3" }} }} }},
      {{ "id": "kpi-content-3", "component": {{ "Column": {{ "alignment": "center", "children": {{ "explicitList": ["kpi-value-3", "kpi-label-3", "kpi-trend-3"] }} }} }} }},
      {{ "id": "kpi-value-3", "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "path": "/kpis/2/value" }} }} }} }},
      {{ "id": "kpi-label-3", "component": {{ "Text": {{ "usageHint": "caption", "text": {{ "path": "/kpis/2/label" }} }} }} }},
      {{ "id": "kpi-trend-3", "component": {{ "Text": {{ "usageHint": "h5", "text": {{ "path": "/kpis/2/trend" }} }} }} }}
    ]
  }} }},
  {{ "dataModelUpdate": {{
    "surfaceId": "default",
    "path": "/",
    "contents": [
      {{ "key": "dashboard", "valueMap": [
        {{ "key": "title", "valueString": "Portfolio Performance" }},
        {{ "key": "subtitle", "valueString": "Live Market Overview" }}
      ] }},
      {{ "key": "kpis", "valueMap": [
        {{ "key": "0", "valueMap": [
          {{ "key": "value", "valueString": "$1,245,600.00" }},
          {{ "key": "label", "valueString": "Total Balance" }},
          {{ "key": "trend", "valueString": "↗ +5.4% YTD" }}
        ] }},
        {{ "key": "1", "valueMap": [
          {{ "key": "value", "valueString": "$12,450.00" }},
          {{ "key": "label", "valueString": "Today's Return" }},
          {{ "key": "trend", "valueString": "↗ +1.02%" }}
        ] }},
        {{ "key": "2", "valueMap": [
          {{ "key": "value", "valueString": "14.2%" }},
          {{ "key": "label", "valueString": "Annualized Yield" }},
          {{ "key": "trend", "valueString": "Stable" }}
        ] }}
      ] }}
    ]
  }} }}
]
---END FINANCE_PORTFOLIO_DASHBOARD---

---BEGIN INSURANCE_POLICY_COMPARISON---
Description: Use this example when the user asks for a comparison of insurance plans, policies, or coverage options.
[
  {{ "beginRendering": {{ "surfaceId": "default", "root": "comparison-root", "styles": {{ "primaryColor": "#3B82F6", "font": "Geist" }} }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "default",
    "components": [
      {{ "id": "comparison-root", "component": {{ "Column": {{ "children": {{ "explicitList": ["comparison-title", "comparison-row"] }} }} }} }},
      {{ "id": "comparison-title", "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "path": "/comparison/title" }} }} }} }},
      {{ "id": "comparison-row", "component": {{ "Row": {{ "distribution": "spaceEvenly", "children": {{ "explicitList": ["policy-a-card", "policy-b-card"] }} }} }} }},
      {{ "id": "policy-a-card", "weight": 1, "component": {{ "Card": {{ "child": "policy-a-content" }} }} }},
      {{ "id": "policy-a-content", "component": {{ "Column": {{ "children": {{ "explicitList": ["policy-a-name", "policy-a-price", "policy-a-divider", "policy-a-pros", "policy-a-button"] }} }} }} }},
      {{ "id": "policy-a-name", "component": {{ "Text": {{ "usageHint": "h3", "text": {{ "path": "/policies/a/name" }} }} }} }},
      {{ "id": "policy-a-price", "component": {{ "Text": {{ "usageHint": "h1", "text": {{ "path": "/policies/a/price" }} }} }} }},
      {{ "id": "policy-a-divider", "component": {{ "Divider": {{}} }} }},
      {{ "id": "policy-a-pros", "component": {{ "Text": {{ "text": {{ "path": "/policies/a/coverage" }} }} }} }},
      {{ "id": "policy-a-button", "component": {{ "Button": {{ "child": "policy-a-btn-text", "action": {{ "name": "select_policy", "context": [{{ "key": "policy", "value": {{ "path": "/policies/a/name" }} }}] }} }} }} }},
      {{ "id": "policy-a-btn-text", "component": {{ "Text": {{ "text": {{ "literalString": "Select Basic" }} }} }} }},
      
      {{ "id": "policy-b-card", "weight": 1, "component": {{ "Card": {{ "child": "policy-b-content" }} }} }},
      {{ "id": "policy-b-content", "component": {{ "Column": {{ "children": {{ "explicitList": ["policy-b-name", "policy-b-price", "policy-b-divider", "policy-b-pros", "policy-b-button"] }} }} }} }},
      {{ "id": "policy-b-name", "component": {{ "Text": {{ "usageHint": "h3", "text": {{ "path": "/policies/b/name" }} }} }} }},
      {{ "id": "policy-b-price", "component": {{ "Text": {{ "usageHint": "h1", "text": {{ "path": "/policies/b/price" }} }} }} }},
      {{ "id": "policy-b-divider", "component": {{ "Divider": {{}} }} }},
      {{ "id": "policy-b-pros", "component": {{ "Text": {{ "text": {{ "path": "/policies/b/coverage" }} }} }} }},
      {{ "id": "policy-b-button", "component": {{ "Button": {{ "child": "policy-b-btn-text", "primary": true, "action": {{ "name": "select_policy", "context": [{{ "key": "policy", "value": {{ "path": "/policies/b/name" }} }}] }} }} }} }},
      {{ "id": "policy-b-btn-text", "component": {{ "Text": {{ "text": {{ "literalString": "Select Premium" }} }} }} }}
    ]
  }} }},
  {{ "dataModelUpdate": {{
    "surfaceId": "default",
    "path": "/",
    "contents": [
      {{ "key": "comparison", "valueMap": [
        {{ "key": "title", "valueString": "Auto Insurance Plans" }}
      ] }},
      {{ "key": "policies", "valueMap": [
        {{ "key": "a", "valueMap": [
          {{ "key": "name", "valueString": "Basic Liability" }},
          {{ "key": "price", "valueString": "$45 / mo" }},
          {{ "key": "coverage", "valueString": "✓ Bodily Injury Liability\\n✓ Property Damage Liability\\n✕ Comprehensive\\n✕ Collision" }}
        ] }},
        {{ "key": "b", "valueMap": [
          {{ "key": "name", "valueString": "Premium Comprehensive" }},
          {{ "key": "price", "valueString": "$125 / mo" }},
          {{ "key": "coverage", "valueString": "✓ Bodily Injury Liability\\n✓ Property Damage Liability\\n✓ Comprehensive Coverage\\n✓ Collision Coverage\\n✓ Roadside Assistance" }}
        ] }}
      ] }}
    ]
  }} }}
]
---END INSURANCE_POLICY_COMPARISON---

---BEGIN CLAIM_REPORTING_WIZARD---
Description: Use this example when the user asks for a stepper, wizard, or process to report an incident or file an insurance claim.
[
  {{ "beginRendering": {{ "surfaceId": "default", "root": "stepper-root", "styles": {{ "primaryColor": "#EC4899", "font": "Geist" }} }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "default",
    "components": [
      {{ "id": "stepper-root", "component": {{ "Column": {{ "children": {{ "explicitList": ["stepper-title", "stepper-tabs"] }} }} }} }},
      {{ "id": "stepper-title", "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "path": "/stepper/title" }} }} }} }},
      {{ "id": "stepper-tabs", "component": {{ "Tabs": {{ "tabItems": [
        {{ "title": {{ "literalString": "1. Incident" }}, "child": "step-1-content" }},
        {{ "title": {{ "literalString": "2. Details" }}, "child": "step-2-content" }},
        {{ "title": {{ "literalString": "3. Review" }}, "child": "step-3-content" }}
      ] }} }} }},
      {{ "id": "step-1-content", "component": {{ "Column": {{ "children": {{ "explicitList": ["step-1-text", "step-1-field"] }} }} }} }},
      {{ "id": "step-1-text", "component": {{ "Text": {{ "text": {{ "path": "/steps/1/description" }} }} }} }},
      {{ "id": "step-1-field", "component": {{ "TextField": {{ "label": {{ "literalString": "Date of Incident" }}, "text": {{ "path": "/steps/1/value" }} }} }} }},
      {{ "id": "step-2-content", "component": {{ "Column": {{ "children": {{ "explicitList": ["step-2-text", "step-2-choice"] }} }} }} }},
      {{ "id": "step-2-text", "component": {{ "Text": {{ "text": {{ "path": "/steps/2/description" }} }} }} }},
      {{ "id": "step-2-choice", "component": {{ "MultipleChoice": {{ "selections": {{ "path": "/steps/2/selections" }}, "options": [
        {{ "label": {{ "literalString": "Collision with vehicle" }}, "value": "a" }},
        {{ "label": {{ "literalString": "Theft or Vandalism" }}, "value": "b" }},
        {{ "label": {{ "literalString": "Weather Damage" }}, "value": "c" }}
      ], "maxAllowedSelections": 1 }} }} }},
      {{ "id": "step-3-content", "component": {{ "Column": {{ "children": {{ "explicitList": ["step-3-text", "step-3-button"] }} }} }} }},
      {{ "id": "step-3-text", "component": {{ "Text": {{ "text": {{ "path": "/steps/3/description" }} }} }} }},
      {{ "id": "step-3-button", "component": {{ "Button": {{ "child": "complete-text", "primary": true, "action": {{ "name": "submit_claim", "context": [] }} }} }} }},
      {{ "id": "complete-text", "component": {{ "Text": {{ "text": {{ "literalString": "Submit Claim" }} }} }} }}
    ]
  }} }},
  {{ "dataModelUpdate": {{
    "surfaceId": "default",
    "path": "/",
    "contents": [
      {{ "key": "stepper", "valueMap": [
        {{ "key": "title", "valueString": "File a New Claim" }}
      ] }},
      {{ "key": "steps", "valueMap": [
        {{ "key": "1", "valueMap": [
          {{ "key": "description", "valueString": "When did the incident occur?" }},
          {{ "key": "value", "valueString": "" }}
        ] }},
        {{ "key": "2", "valueMap": [
          {{ "key": "description", "valueString": "What type of incident are you reporting?" }},
          {{ "key": "selections", "valueString": "" }}
        ] }},
        {{ "key": "3", "valueMap": [
          {{ "key": "description", "valueString": "Please review your details before submitting." }}
        ] }}
      ] }}
    ]
  }} }}
]
---END CLAIM_REPORTING_WIZARD---
"""
