import streamlit as st

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

        /* 7. SIDEBAR STYLING */
        [data-testid="stSidebar"] {
            background-color: #0f172a;
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
