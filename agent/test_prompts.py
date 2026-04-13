# Test prompts to exercise all A2UI atomic components
# Usage: copy-paste any prompt into the chat to verify rendering

TEST_PROMPTS = [
    # ── Buttons ──
    "Create a simple page with two buttons: 'Confirm' and 'Cancel'.",

    # ── Typography ──
    "Show a text hierarchy: a main title, subtitle, body paragraph, and a caption at the bottom.",

    # ── Cards + KPI dashboard ──
    "Build a financial KPI dashboard with 3 cards showing Total Revenue, Active Users, and Conversion Rate.",

    # ── TextField + Form ──
    "Create a contact form with fields for Name, Email, Phone Number, and a long text area for Message.",

    # ── CheckBox ──
    "Show a terms-and-conditions checkbox followed by a Submit button.",

    # ── DateTimeInput ──
    "Create a booking form with a date/time picker for appointment scheduling.",

    # ── Slider ──
    "Build a loan calculator with a slider for the amount (0 to 100000) and another for the duration in months (12 to 360).",

    # ── MultipleChoice ──
    "Create a survey with a multiple-choice question: 'Which features do you use most?' with options: Dashboard, Reports, Notifications, Settings.",

    # ── Icons ──
    "Show a row of feature highlights, each with an icon and a short label: Security (shield), Speed (bolt), Support (headset_mic).",

    # ── Images ──
    "Create a team page with 3 avatar images and names underneath each one.",

    # ── Tabs ──
    "Build a product page with 3 tabs: Overview, Specifications, and Reviews.",

    # ── Lists ──
    "Show a vertical list of 5 recent transactions, each with date, description, and amount.",

    # ── Modal ──
    "Create a page with a 'Delete Account' button that opens a confirmation modal.",

    # ── Divider ──
    "Build a pricing card with plan name, price, a divider, and a bullet list of features.",

    # ── Video + Audio ──
    "Create a media gallery with a video player and an audio player below it.",

    # ── Complex: multiple components ──
    "Build an insurance policy comparison with two cards side by side. Each card has a plan name, price, divider, feature list, and a selection button.",

    # ── Complex: wizard ──
    "Create a 3-step claim wizard using tabs: Step 1 asks for incident date (date picker), Step 2 asks for incident type (multiple choice), Step 3 shows a summary and a Submit button.",
]

if __name__ == "__main__":
    print(f"Available test prompts: {len(TEST_PROMPTS)}\n")
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"  [{i:2d}] {prompt}")
