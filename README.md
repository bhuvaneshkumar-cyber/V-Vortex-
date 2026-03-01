# V-Vortex
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
