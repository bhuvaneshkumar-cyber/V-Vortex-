# V-Vortex-Hackathon
# Rhythm Anchor

AI-Powered Mental Well-Being Risk Indicator (Non-Clinical)

Rhythm Anchor is a privacy-first, interactive wellness companion built with Streamlit. It helps users track their daily habits, recognise doomscrolling patterns, and receive personalised advice through an integrated AI chatbot.

# Key Features

* Hybrid Stability Index: Calculates a daily wellness score combining an ML-based anomaly detection model (`IsolationForest`) with a deterministic penalty system for lifestyle factors (like stress and smoking) and physical symptoms.
* Doomscroll Detection: Analyses simulated "thumb physics" (scroll velocity and erraticness) combined with the time of day to warn you of high-risk late-night scrolling.
* AI Wellness Coach: A floating chat window powered by Gemini (using the `gemini-2.5-flash-lite` model) provides precise and actionable wellness advice.
* Interactive Dashboard: Visualises stability trends and scrolling velocity using dark-themed `Altair` charts.
* Custom UI: Features a custom CSS-driven dark gradient background, floating action buttons, and responsive metric cards.

# Tech Stack

* Frontend & Framework: Streamlit
* Data Manipulation: Pandas, NumPy
* Machine Learning: Scikit-learn (`IsolationForest`)
* Visualisations: Altair
* Generative AI: Google Generative AI SDK (`google-generativeai`)

# How to use
* Sign Up/Log In: Create a new profile or log in with credentials.

* Input Daily Stats: Open the controls in the sidebar to simulate your day—adjust your alarm time, wake-up time, daily steps, symptoms, and lifestyle factors.

* Simulate Scrolling: Adjust your thumb physics (scroll speed and erraticness) to see if the app detects a doomscrolling risk in the "🛑 Doomscroll" tab.

* Save & Track: Hit "💾 Save Daily Stats" to log your data and watch your stability trend line populate.

* Chat with the AI: Click the floating 💬 button in the bottom right corner to get actionable advice from your AI coach.

# Disclaimer
Rhythm Anchor is a non-clinical tool. The stability index and AI insights provided are for educational and self-reflection purposes only and should not be used as a substitute for professional medical or psychiatric advice.
