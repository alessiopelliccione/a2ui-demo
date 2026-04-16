# Test prompts for the Insurance Assistant agent
# Usage: copy-paste any prompt into the chat to verify rendering and interactions
# Prompts exercise both text-only responses and A2UI interactive components

TEST_PROMPTS = [
    # ── Text-only (no UI) ──
    "Hi, what can you do?",
    "What types of insurance do you offer?",

    # ── Policy browsing ──
    "I want to see the available auto insurance policies.",
    "Show me a comparison between home insurance policies: Base, Plus, and Premium.",
    "What are the life insurance options?",

    # ── KPI Dashboard ──
    "Show me a dashboard with the status of my active policies, premiums paid, and expiration dates.",
    "Create a summary of my insurance portfolio with 4 KPIs.",

    # ── Policy selection (button interaction) ──
    "I want to change my auto insurance. What policies are available?",
    "Compare health plans: Bronze, Silver, and Gold with prices and coverage.",

    # ── Claims ──
    "I want to file a claim for my auto insurance.",
    "Show me a wizard to file a claim: date, incident type, and description.",

    # ── Forms ──
    "I want to request a quote for home insurance. Show me a form.",
    "Create a form to update my contact details: name, email, phone, address.",

    # ── Complex interactions ──
    "Show me my active policies in a list with status, expiration, and a button for details.",
    "Create a comparative table of 3 auto insurance plans with premium, deductible, and maximum coverage.",

    # ── Cards + details ──
    "Show me the details of the Premium Auto policy with coverage, deductible, and monthly premium.",
    "Create a card with a claim summary: case number, status, date, and amount.",

    # ── Tabs ──
    "Create a page with 3 tabs: My Policies, Open Claims, Payments.",

    # ── Edge cases ──
    "What is the difference between comprehensive and third-party insurance?",
    "Tell me the tech conference not to miss this year.",
]

if __name__ == "__main__":
    print(f"Available test prompts: {len(TEST_PROMPTS)}\n")
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"  [{i:2d}] {prompt}")
