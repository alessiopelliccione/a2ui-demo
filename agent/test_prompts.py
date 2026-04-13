# Test prompts for the Insurance Assistant agent
# Usage: copy-paste any prompt into the chat to verify rendering and interactions
# Prompts exercise both text-only responses and A2UI interactive components

TEST_PROMPTS = [
    # ── Text-only (no UI) ──
    "Ciao, cosa sai fare?",
    "Quali tipi di assicurazione offrite?",

    # ── Policy browsing ──
    "Voglio vedere le polizze auto disponibili.",
    "Mostrami un confronto tra le polizze casa: Base, Plus e Premium.",
    "Quali sono le opzioni di assicurazione vita?",

    # ── KPI Dashboard ──
    "Mostrami una dashboard con lo stato delle mie polizze attive, i premi pagati e le scadenze.",
    "Crea un riepilogo del mio portfolio assicurativo con 4 KPI.",

    # ── Policy selection (button interaction) ──
    "Voglio cambiare la mia assicurazione auto. Che polizze ci sono?",
    "Confronta i piani salute: Bronze, Silver e Gold con prezzi e coperture.",

    # ── Claims ──
    "Voglio aprire un sinistro per la mia auto.",
    "Mostrami un wizard per la denuncia di un sinistro: data, tipo di incidente e descrizione.",

    # ── Forms ──
    "Voglio richiedere un preventivo per un'assicurazione casa. Fammi un form.",
    "Crea un modulo per aggiornare i miei dati di contatto: nome, email, telefono, indirizzo.",

    # ── Complex interactions ──
    "Mostrami le mie polizze attive in una lista con stato, scadenza e un bottone per i dettagli.",
    "Crea una tabella comparativa di 3 piani assicurativi auto con premio, franchigia e massimale.",

    # ── Cards + details ──
    "Mostrami i dettagli della polizza Premium Auto con coperture, franchigia e premio mensile.",
    "Crea una card con il riepilogo di un sinistro: numero pratica, stato, data e importo.",

    # ── Tabs ──
    "Crea una pagina con 3 tab: Le Mie Polizze, Sinistri Aperti, Pagamenti.",

    # ── Edge cases ──
    "What is the difference between comprehensive and third-party insurance?",
    "Dimmi la conferenza tech da non perdere quest'anno.",
]

if __name__ == "__main__":
    print(f"Available test prompts: {len(TEST_PROMPTS)}\n")
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"  [{i:2d}] {prompt}")
