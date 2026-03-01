import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDoaboDLjgzCdJZMkyWL1ZUAGbDtanjrZM"

try:
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel("gemini-2.5-flash-lite")
    ai_available = True
except Exception as e:
    ai_available = False
    print(f"AI Setup Error: {e}")

SYSTEM_CONTEXT = """
You are Rhythm Anchor, a smart, encouraging, and action-oriented wellness coach. 🧠✨ 
Your goal is to help users improve sleep, reduce screen time, and lower stress with precise, science-backed advice.
- Be Precise & Actionable.
- Use Bold Text and Bullet Points.
- Use motivational emojis (🌿, 💪, 🌊, 🚀).
- Keep it short.
"""

def get_ai_response(user_input, chat_history):
    if not ai_available:
        return "⚠️ Gemini API Key is missing or invalid. Check setup."
    try:
        history_for_gemini = []
        history_for_gemini.append({"role": "user", "parts": [SYSTEM_CONTEXT]})
        history_for_gemini.append(
            {"role": "model", "parts": ["Understood. I am Rhythm Anchor."]}
        )
        for msg in chat_history[-10:]:
            role = "user" if msg["role"] == "user" else "model"
            history_for_gemini.append({"role": role, "parts": [msg["text"]]})

        chat = ai_model.start_chat(history=history_for_gemini)
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"
