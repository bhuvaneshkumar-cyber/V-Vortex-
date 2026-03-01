import streamlit as st
import views
from styles import set_global_theme

st.set_page_config(page_title="Rhythm Anchor", page_icon="🧠", layout="wide")

if "page" not in st.session_state: st.session_state["page"] = "landing"
if "history_log" not in st.session_state: st.session_state["history_log"] = []
if "entry_counter" not in st.session_state: st.session_state["entry_counter"] = 1
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "text": "Hi! I'm your privacy-first wellness companion."}]
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "username" not in st.session_state: st.session_state["username"] = ""
if "auth_mode" not in st.session_state: st.session_state["auth_mode"] = "Sign In"
if "show_chat_window" not in st.session_state: st.session_state["show_chat_window"] = False
if "show_account_window" not in st.session_state: st.session_state["show_account_window"] = False

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

set_global_theme()

if st.session_state["logged_in"]:
    views.show_main_app()
elif st.session_state["page"] == "landing":
    views.show_landing_page()
elif st.session_state["page"] == "login":
    views.show_login_page()
