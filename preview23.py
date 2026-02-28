import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import altair as alt
from datetime import datetime, time
import time as time_lib
import google.generativeai as genai

# ==========================================
# 1. SETUP & SESSION STATE
# ==========================================
st.set_page_config(page_title="Rhythm Anchor", page_icon="🧠", layout="wide")

# Initialize Session State
if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "history_log" not in st.session_state:
    st.session_state["history_log"] = []
if "entry_counter" not in st.session_state:
    st.session_state["entry_counter"] = 1
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "text": "Hi! I'm your privacy-first wellness companion."}
    ]
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# STATE FOR LOGIN/SIGNUP SWITCHING
if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "Sign In"

# FLOATING WINDOW STATES
if "show_chat_window" not in st.session_state:
    st.session_state["show_chat_window"] = False
if "show_account_window" not in st.session_state:
    st.session_state["show_account_window"] = False

if "user_db" not in st.session_state:
    st.session_state["user_db"] = {
        "admin": {
            "password": "1234",
            "full_name": "System Administrator",
            "age": 30,
            "email": "admin@rhythmanchor.com",
            "medical_history": "None",
        }
    }

# ==========================================
# 2. GEMINI API SETUP
# ==========================================
GEMINI_API_KEY = "AIzaSyDoaboDLjgzCdJZMkyWL1ZUAGbDtanjrZM"  # <--- Ensure key is correct

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Using flash-lite as it has higher rate limits for free tier
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


# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def calculate_hybrid_stability(ai_score, lifestyle_factors, symptoms, age):
    base_stability = int(max(0, min(100, (ai_score + 0.5) * 100)))
    penalties = 0
    reasons = []
    if "Smoking" in lifestyle_factors:
        penalties += 5
        reasons.append("Lifestyle (Smoking)")
    if "High Stress Work" in lifestyle_factors:
        penalties += 5
        reasons.append("High Stress Environment")
    if "Regular Alcohol" in lifestyle_factors:
        penalties += 5
        reasons.append("Alcohol Consumption")
    if age > 60:
        penalties += 2
    symptom_weights = {
        "Fatigue": 10,
        "Insomnia": 15,
        "Anxiety": 15,
        "Palpitations": 20,
        "Headache": 5,
    }
    for sym in symptoms:
        penalties += symptom_weights.get(sym, 5)
        reasons.append(f"Symptom ({sym})")
    return max(0, base_stability - penalties), base_stability, reasons


def generate_baseline(days=30):
    np.random.seed(42)
    return pd.DataFrame(
        {
            "snooze_delta": np.random.normal(0.5, 0.2, days),
            "daily_steps": np.random.normal(7000, 800, days),
            "app_switch_rate": np.random.normal(40, 5, days),
            "pickup_count": np.random.normal(80, 10, days),
        }
    )


def train_isolation_forest(baseline_df):
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(baseline_df)
    return model


def generate_scroll_pattern(intensity, erraticness, duration_seconds=60):
    np.random.seed(42)
    time_points = range(duration_seconds)
    if intensity < 300:
        velocities = [
            0 if np.random.random() > 0.3 else np.random.randint(50, 400)
            for _ in time_points
        ]
    else:
        base = np.full(duration_seconds, intensity)
        noise = np.random.normal(0, erraticness * 5, duration_seconds)
        velocities = np.abs(base + noise)
    return pd.DataFrame({"Seconds": time_points, "Velocity (px/s)": velocities})


def detect_doomscrolling(df, current_time_obj):
    avg_speed = df["Velocity (px/s)"].mean()
    zero_crossings = (df["Velocity (px/s)"] == 0).sum()
    is_late_night = current_time_obj.hour >= 22 or current_time_obj.hour <= 4
    risk_score = 0
    reasons = []
    if avg_speed > 600:
        risk_score += 40
        reasons.append("High Velocity")
    if zero_crossings < 5:
        risk_score += 40
        reasons.append("Zero Dwell Time")
    if is_late_night and risk_score > 0:
        risk_score += 20
        reasons.append("Late Night Context")
    return min(100, risk_score), reasons


def get_ai_response(user_input, chat_history):
    if "ai_available" not in globals() or not ai_available:
        return "⚠️ Gemini API Key is missing. Check setup."
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


baseline_df = generate_baseline()
model = train_isolation_forest(baseline_df)


# ==========================================
# 4. CSS STYLING
# ==========================================
def set_global_theme():
    st.markdown(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;600;700&display=swap');
        
        /* 1. BACKGROUND */
        .stApp {
            background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #243b55, #141E30);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: #ffffff;
            font-family: 'Quicksand', sans-serif;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* 2. HEADERS */
        h1 { font-size: 3rem !important; font-weight: 700; color: #e0f7fa !important; }
        h2 { font-size: 2.2rem !important; color: #b2ebf2 !important; }
        
        /* 3. INPUTS & SLIDERS */
        div[data-baseweb="base-input"], div[data-testid="stNumberInputContainer"] {
            background-color: transparent !important; border: none !important; box-shadow: none !important;
        }
        .stTextInput input, .stNumberInput input, .stTextArea textarea {
            font-size: 16px !important; padding: 15px !important; border-radius: 20px !important;
            color: #e0f7fa !important; background: rgba(255, 255, 255, 0.07) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        /* 4. BUTTONS (Blue Gradient) */
        .stButton > button {
            border-radius: 50px !important;
            background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3);
        }
        .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 114, 255, 0.5); }

        /* 5. METRIC CARDS */
        .metric-card {
            background: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05); text-align: center; height: 100%;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .metric-card:hover { transform: translateY(-8px); background: rgba(255, 255, 255, 0.08); }
        .metric-value { font-size: 2rem; font-weight: 700; color: #00e5ff !important; }
        .status-danger { color: #fca5a5; } .status-warning { color: #fcd34d; } .status-safe { color: #6ee7b7; }

        /* 6. FLOATING BUTTONS */
        .account-floater { position: fixed; top: 70px; right: 20px; z-index: 9999; }
        .chat-floater { position: fixed; bottom: 30px; right: 20px; z-index: 9999; }

        .account-floater button, .chat-floater button {
            border-radius: 50% !important;
            width: 60px !important; height: 60px !important;
            padding: 0 !important; font-size: 24px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        }
        .chat-floater button { background: linear-gradient(135deg, #00c6ff, #0072ff) !important; }
        .account-floater button { background: rgba(255,255,255,0.1) !important; border: 1px solid rgba(255,255,255,0.3) !important; }

        /* 7. SIDEBAR STYLING (To match screenshot) */
        [data-testid="stSidebar"] {
            background-color: #0f172a; /* Dark Blue/Black */
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        [data-testid="stSidebar"] h1 { color: #e0f7fa !important; }
        [data-testid="stSidebar"] p { color: #94a3b8 !important; }
        
        header {background: transparent !important;}
    </style>
    """,
        unsafe_allow_html=True,
    )


def apply_dark_theme(chart):
    return (
        chart.configure(background="transparent")
        .configure_axis(
            labelColor="#e0f7fa",
            titleColor="#00e5ff",
            gridColor="rgba(255,255,255,0.1)",
        )
        .configure_view(strokeWidth=0)
    )


set_global_theme()


# ==========================================
# 5. UI VIEWS
# ==========================================
def show_landing_page():
    st.markdown(
        """<div style="text-align:center; padding:50px;">
        <div style="font-size: 80px; margin-bottom: 10px;">🧠</div>
        <h1>Rhythm Anchor</h1>
        <p>AI-Powered Mental Well-Being Risk Indicator (Non-Clinical)</p>
    </div>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([0.2, 8, 0.2])
    with col2:
        st.markdown(
            """<style>div[data-testid="stButton"] > button { height: 80px !important; font-size: 28px !important; }</style>""",
            unsafe_allow_html=True,
        )
        if st.button("Get Started", type="primary", use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()


def show_login_page():
    col1, col2, col3 = st.columns([0.5, 8, 0.5])
    with col2:
        st.markdown(
            """<div style="text-align: center; margin-bottom: 30px;"><div style="font-size: 60px;">🧠</div><h2>Rhythm Anchor</h2></div>""",
            unsafe_allow_html=True,
        )
        mode = st.radio(
            "Auth Mode",
            ["Sign In", "New Account"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if mode == "Sign In":
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.button("Enter Sanctuary", type="primary", use_container_width=True):
                if (
                    user in st.session_state["user_db"]
                    and st.session_state["user_db"][user]["password"] == pw
                ):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = user
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        else:
            new_u = st.text_input("New Username")
            new_p = st.text_input("New Password", type="password")
            if st.button("Create Profile", type="primary", use_container_width=True):
                st.session_state["user_db"][new_u] = {
                    "password": new_p,
                    "full_name": new_u,
                    "age": 25,
                }
                st.success("Created! Please Sign In.")


def show_main_app():
    current_user = st.session_state["username"]
    user_data = st.session_state["user_db"].get(current_user, {})

    # ==========================
    # FLOATING BUTTONS
    # ==========================
    # 1. Account (Top Right)
    with st.container():
        st.markdown('<div class="account-floater">', unsafe_allow_html=True)
        if st.button("👤", key="btn_account_float", help="Account"):
            st.session_state.show_account_window = (
                not st.session_state.show_account_window
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Chat (Bottom Right)
    with st.container():
        st.markdown('<div class="chat-floater">', unsafe_allow_html=True)
        if st.button("💬", key="btn_chat_float", help="Chat"):
            # Toggle Logic: If chat opens, it reclaims sidebar. If closed, sidebar goes back to controls.
            st.session_state.show_chat_window = not st.session_state.show_chat_window
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================
    # SIDEBAR CONTENT SWAP LOGIC
    # ==========================
    with st.sidebar:
        # MODE A: CHAT INTERFACE (Triggered by Floating Button)
        if st.session_state.show_chat_window:
            st.markdown("### 💬 AI Coach")
            if st.button("🔙 Back to Controls", use_container_width=True):
                st.session_state.show_chat_window = False
                st.rerun()

            # Chat UI
            messages_container = st.container()
            with messages_container:
                for msg in st.session_state["chat_history"]:
                    with st.chat_message(msg["role"]):
                        st.write(msg["text"])

            user_input = st.chat_input("Ask advice...")
            if user_input:
                st.session_state["chat_history"].append(
                    {"role": "user", "text": user_input}
                )
                with st.chat_message("user"):
                    st.write(user_input)
                with st.spinner("Thinking..."):
                    response = get_ai_response(
                        user_input, st.session_state["chat_history"]
                    )
                st.session_state["chat_history"].append(
                    {"role": "assistant", "text": response}
                )
                st.rerun()

            # Define Defaults for Dashboard when Sidebar is in Chat Mode
            # (Dashboard needs these variables to run without error)
            steps = 7000
            snooze_delta = 1
            symptoms = []
            lifestyle = ["Stress"]
            sim_time = time(23, 30)
            scroll_intensity, scroll_variance = 800, 20

        # MODE B: CONTROLS INTERFACE (Default - Matches Screenshot)
        else:
            st.markdown("## 🎮 Controls")

            with st.expander("👤 1. User Profile"):
                st.markdown(f"**User:** {user_data.get('full_name', current_user)}")
                st.caption("Edit details in Account 👤")

            with st.expander("📝 2. Day Simulation", expanded=True):
                alarm = st.slider("⏰ Alarm Time", 4, 12, 7)
                unlock = st.slider("🔓 Actual Wake Up", 4, 14, 8)
                snooze_delta = max(0, unlock - alarm)
                steps = st.slider("👟 Daily Steps", 0, 15000, 7000)
                st.markdown("---")
                symptoms = st.multiselect(
                    "Symptoms Today",
                    ["Headache", "Fatigue", "Anxiety", "Insomnia"],
                    default=[],
                )
                lifestyle = st.multiselect(
                    "Risk Factors", ["High Stress", "Smoking"], default=["High Stress"]
                )

            with st.expander("📜 3. Thumb Physics", expanded=True):
                sim_time = st.time_input("Current Time", value=time(23, 30))
                scroll_intensity = st.slider("Scroll Speed (px/s)", 0, 2000, 800)
                scroll_variance = st.slider("Erraticness", 0, 100, 20)

            st.markdown("<br>", unsafe_allow_html=True)

            # THE BUTTONS FROM SCREENSHOT
            if st.button("💾 Save Daily Stats", use_container_width=True):
                # Calculate metric first
                log_data = pd.DataFrame(
                    [
                        {
                            "snooze_delta": snooze_delta,
                            "daily_steps": steps,
                            "app_switch_rate": 40,
                            "pickup_count": 80,
                        }
                    ]
                )
                ai_score = model.decision_function(log_data)[0]
                final_stability, _, _ = calculate_hybrid_stability(
                    ai_score, lifestyle, symptoms, 25
                )

                st.session_state["history_log"].append(
                    {
                        "day": f"Day {st.session_state['entry_counter']}",
                        "stability_index": final_stability,
                    }
                )
                st.session_state["entry_counter"] += 1
                st.toast("Saved!")

            if st.button("⬅️ Log Out", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["page"] = "landing"
                st.rerun()

    # ==========================
    # ACCOUNT OVERLAY
    # ==========================
    if st.session_state.show_account_window:
        with st.expander("👤 Account Profile", expanded=True):
            e_name = st.text_input("Name", user_data.get("full_name", ""))
            e_age = st.number_input("Age", 18, 100, int(user_data.get("age", 25)))
            if st.button("Update Profile"):
                st.session_state["user_db"][current_user]["full_name"] = e_name
                st.session_state["user_db"][current_user]["age"] = e_age
                st.success("Updated!")

    # ==========================
    # MAIN DASHBOARD
    # ==========================
    st.markdown(f"## 🧠 Rhythm Anchor")
    st.caption(f"Welcome back, {user_data.get('full_name', current_user)}")

    tab1, tab2 = st.tabs(["📊 Dashboard", "🛑 Doomscroll"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        # Recalculate Logic for Main View
        log_data = pd.DataFrame(
            [
                {
                    "snooze_delta": snooze_delta,
                    "daily_steps": steps,
                    "app_switch_rate": 40,
                    "pickup_count": 80,
                }
            ]
        )
        ai_score = model.decision_function(log_data)[0]
        final_stability, _, impact_reasons = calculate_hybrid_stability(
            ai_score, lifestyle, symptoms, 25
        )

        # Status Logic
        if final_stability < 50:
            status_class, status_text, main_icon = "status-danger", "Risk Detected", "⚠️"
        elif final_stability < 80:
            status_class, status_text, main_icon = (
                "status-warning",
                "Minor Deviation",
                "🛡️",
            )
        else:
            status_class, status_text, main_icon = "status-safe", "Stable Rhythm", "✅"

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f"""<div class="metric-card"><div class="metric-value">{main_icon} {final_stability}/100</div><div>Stability Index</div><div class="{status_class}">{status_text}</div></div>""",
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""<div class="metric-card"><div class="metric-value">🛌 {snooze_delta}h</div><div>Snooze Delta</div></div>""",
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f"""<div class="metric-card"><div class="metric-value">👟 {steps}</div><div>Steps Today</div></div>""",
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Trend Graph
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.subheader("📉 Risks")
            if impact_reasons:
                for r in impact_reasons:
                    st.markdown(f"🔴 {r}")
            else:
                st.markdown("🟢 No significant risks")

        with col_b:
            st.subheader("📈 Trend")
            if st.session_state["history_log"]:
                chart = (
                    alt.Chart(pd.DataFrame(st.session_state["history_log"]))
                    .mark_area(
                        line={"color": "#00e5ff"},
                        color=alt.Gradient(
                            gradient="linear",
                            stops=[
                                alt.GradientStop(color="#00e5ff", offset=0),
                                alt.GradientStop(color="transparent", offset=1),
                            ],
                            x1=1,
                            x2=1,
                            y1=1,
                            y2=0,
                        ),
                    )
                    .encode(x="day", y="stability_index")
                    .interactive()
                )
                st.altair_chart(apply_dark_theme(chart), use_container_width=True)
            else:
                st.info("Save daily stats to see trends!")

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        # Use controls from sidebar
        scroll_df = generate_scroll_pattern(scroll_intensity, scroll_variance)
        risk, _ = detect_doomscrolling(scroll_df, sim_time)

        c_a, c_b = st.columns([2, 1])
        with c_a:
            chart = (
                alt.Chart(scroll_df)
                .mark_bar(color="#ef4444" if risk > 50 else "#3b82f6")
                .encode(
                    x=alt.X("Seconds", axis=alt.Axis(labels=False)), y="Velocity (px/s)"
                )
                .properties(height=250)
            )
            st.altair_chart(apply_dark_theme(chart), use_container_width=True)
        with c_b:
            if risk > 60:
                st.markdown(
                    f"""<div class="metric-card" style="border: 1px solid #ef4444;"><div style="font-size:40px;">🛑</div><h3 style="color:#ef4444;">High Risk</h3></div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""<div class="metric-card" style="border: 1px solid #10b981;"><div style="font-size:40px;">✅</div><h3 style="color:#10b981;">Focused</h3></div>""",
                    unsafe_allow_html=True,
                )


# ==========================================
# 6. ROUTING
# ==========================================
if st.session_state["logged_in"]:
    show_main_app()
elif st.session_state["page"] == "landing":
    show_landing_page()
elif st.session_state["page"] == "login":
    show_login_page()
