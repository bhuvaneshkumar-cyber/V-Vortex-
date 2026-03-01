import streamlit as st
import pandas as pd
import altair as alt
from datetime import time
from analytics import calculate_hybrid_stability, generate_scroll_pattern, detect_doomscrolling, model
from ai_service import get_ai_response
from styles import apply_dark_theme

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

    with st.container():
        st.markdown('<div class="account-floater">', unsafe_allow_html=True)
        if st.button("👤", key="btn_account_float", help="Account"):
            st.session_state.show_account_window = not st.session_state.show_account_window
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="chat-floater">', unsafe_allow_html=True)
        if st.button("💬", key="btn_chat_float", help="Chat"):
            st.session_state.show_chat_window = not st.session_state.show_chat_window
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with st.sidebar:
        if st.session_state.show_chat_window:
            st.markdown("### 💬 AI Coach")
            if st.button("🔙 Back to Controls", use_container_width=True):
                st.session_state.show_chat_window = False
                st.rerun()

            messages_container = st.container()
            with messages_container:
                for msg in st.session_state["chat_history"]:
                    with st.chat_message(msg["role"]):
                        st.write(msg["text"])

            user_input = st.chat_input("Ask advice...")
            if user_input:
                st.session_state["chat_history"].append({"role": "user", "text": user_input})
                with st.chat_message("user"):
                    st.write(user_input)
                with st.spinner("Thinking..."):
                    response = get_ai_response(user_input, st.session_state["chat_history"])
                st.session_state["chat_history"].append({"role": "assistant", "text": response})
                st.rerun()

            steps = 7000
            snooze_delta = 1
            symptoms = []
            lifestyle = ["Stress"]
            sim_time = time(23, 30)
            scroll_intensity, scroll_variance = 800, 20

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
                symptoms = st.multiselect("Symptoms Today", ["Headache", "Fatigue", "Anxiety", "Insomnia"], default=[])
                lifestyle = st.multiselect("Risk Factors", ["High Stress", "Smoking"], default=["High Stress"])

            with st.expander("📜 3. Thumb Physics", expanded=True):
                sim_time = st.time_input("Current Time", value=time(23, 30))
                scroll_intensity = st.slider("Scroll Speed (px/s)", 0, 2000, 800)
                scroll_variance = st.slider("Erraticness", 0, 100, 20)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("💾 Save Daily Stats", use_container_width=True):
                log_data = pd.DataFrame([{"snooze_delta": snooze_delta, "daily_steps": steps, "app_switch_rate": 40, "pickup_count": 80}])
                ai_score = model.decision_function(log_data)[0]
                final_stability, _, _ = calculate_hybrid_stability(ai_score, lifestyle, symptoms, 25)

                st.session_state["history_log"].append({"day": f"Day {st.session_state['entry_counter']}", "stability_index": final_stability})
                st.session_state["entry_counter"] += 1
                st.toast("Saved!")

            if st.button("⬅️ Log Out", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["page"] = "landing"
                st.rerun()

    if st.session_state.show_account_window:
        with st.expander("👤 Account Profile", expanded=True):
            e_name = st.text_input("Name", user_data.get("full_name", ""))
            e_age = st.number_input("Age", 18, 100, int(user_data.get("age", 25)))
            if st.button("Update Profile"):
                st.session_state["user_db"][current_user]["full_name"] = e_name
                st.session_state["user_db"][current_user]["age"] = e_age
                st.success("Updated!")

    st.markdown(f"## 🧠 Rhythm Anchor")
    st.caption(f"Welcome back, {user_data.get('full_name', current_user)}")
    tab1, tab2 = st.tabs(["📊 Dashboard", "🛑 Doomscroll"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        log_data = pd.DataFrame([{"snooze_delta": snooze_delta, "daily_steps": steps, "app_switch_rate": 40, "pickup_count": 80}])
        ai_score = model.decision_function(log_data)[0]
        final_stability, _, impact_reasons = calculate_hybrid_stability(ai_score, lifestyle, symptoms, 25)

        if final_stability < 50:
            status_class, status_text, main_icon = "status-danger", "Risk Detected", "⚠️"
        elif final_stability < 80:
            status_class, status_text, main_icon = "status-warning", "Minor Deviation", "🛡️"
        else:
            status_class, status_text, main_icon = "status-safe", "Stable Rhythm", "✅"

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"""<div class="metric-card"><div class="metric-value">{main_icon} {final_stability}/100</div><div>Stability Index</div><div class="{status_class}">{status_text}</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<div class="metric-card"><div class="metric-value">🛌 {snooze_delta}h</div><div>Snooze Delta</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown(f"""<div class="metric-card"><div class="metric-value">👟 {steps}</div><div>Steps Today</div></div>""", unsafe_allow_html=True)

        st.markdown("---")

        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.subheader("📉 Risks")
            if impact_reasons:
                for r in impact_reasons: st.markdown(f"🔴 {r}")
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
                            stops=[alt.GradientStop(color="#00e5ff", offset=0), alt.GradientStop(color="transparent", offset=1)],
                            x1=1, x2=1, y1=1, y2=0,
                        ),
                    ).encode(x="day", y="stability_index").interactive()
                )
                st.altair_chart(apply_dark_theme(chart), use_container_width=True)
            else:
                st.info("Save daily stats to see trends!")

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        scroll_df = generate_scroll_pattern(scroll_intensity, scroll_variance)
        risk, _ = detect_doomscrolling(scroll_df, sim_time)

        c_a, c_b = st.columns([2, 1])
        with c_a:
            chart = (
                alt.Chart(scroll_df)
                .mark_bar(color="#ef4444" if risk > 50 else "#3b82f6")
                .encode(x=alt.X("Seconds", axis=alt.Axis(labels=False)), y="Velocity (px/s)")
                .properties(height=250)
            )
            st.altair_chart(apply_dark_theme(chart), use_container_width=True)
        with c_b:
            if risk > 60: st.markdown(f"""<div class="metric-card" style="border: 1px solid #ef4444;"><div style="font-size:40px;">🛑</div><h3 style="color:#ef4444;">High Risk</h3></div>""", unsafe_allow_html=True)
            else: st.markdown(f"""<div class="metric-card" style="border: 1px solid #10b981;"><div style="font-size:40px;">✅</div><h3 style="color:#10b981;">Focused</h3></div>""", unsafe_allow_html=True)
