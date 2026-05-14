import streamlit as st
import streamlit.components.v1 as components
import uuid
import base64
from db import get_sample_stimuli, save_response

st.set_page_config(page_title="Caption Rating", layout="centered", initial_sidebar_state="collapsed")

# --- Custom CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@300;400;700&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Frank Ruhl Libre', serif;
            direction: rtl;
            background-color: #eae6df !important;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #eae6df !important;
        }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {
            color: #2c2c2c !important;
        }

        .stSlider label, .stSlider p {
            color: #2c2c2c !important;
        }

        .block-container {
            padding-top: 3rem;
            padding-bottom: 2rem;
            max-width: 860px;
        }

        h1 {
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a2e !important;
            margin-bottom: 1.5rem;
        }

        .intro-text {
            font-size: 1.3rem;
            line-height: 2;
            color: #2c2c2c;
            text-align: right;
            background: #ffffff;
            border: 2px solid #1a1a2e;
            padding: 1.5rem 1.5rem 1.5rem 1rem;
            border-radius: 0px;
            margin-bottom: 2rem;
        }

        .intro-text ul {
            padding-right: 1.5rem;
            padding-left: 0;
            margin: 0.5rem 0;
        }

        .thank-you {
            text-align: center;
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a2e;
            margin-top: 4rem;
            line-height: 2;
        }

        div.stButton > button {
            display: block;
            margin: 0 auto;
            background-color: #1a1a2e !important;
            color: #ffffff !important;
            font-family: 'Frank Ruhl Libre', serif;
            font-size: 1.1rem;
            padding: 0.6rem 2.5rem;
            border-radius: 4px;
            border: none !important;
            cursor: pointer;
        }

        div.stButton > button:hover {
            background-color: #2e2e5e !important;
            color: #ffffff !important;
        }

        div.stButton > button p {
            color: #ffffff !important;
        }

        [data-testid="stImage"] {
            display: flex !important;
            justify-content: center !important;
        }

        [data-testid="stImage"] img {
            max-height: 350px !important;
            width: auto !important;
            max-width: 100% !important;
            object-fit: contain !important;
            border-radius: 0px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        .caption-label {
            font-size: 1.05rem;
            font-weight: 700;
            color: #1a1a2e;
            text-align: right;
            margin-bottom: 0.25rem;
        }

        [data-testid="stSlider"] {
            direction: ltr !important;
        }

        [data-testid="stSlider"] label {
            direction: rtl !important;
            text-align: right !important;
        }

        .counter {
            text-align: center;
            color: #1a1a2e !important;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Initialize session state ---
if "stage" not in st.session_state:
    st.session_state.stage = "landing"

if "participant_id" not in st.session_state:
    st.session_state.participant_id = str(uuid.uuid4())

if "stimuli" not in st.session_state:
    st.session_state.stimuli = get_sample_stimuli()

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "ratings" not in st.session_state:
    st.session_state.ratings = []

# ─────────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────────
if st.session_state.stage == "landing":

    def img_to_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    logo1 = img_to_base64("logo1.png")
    logo2 = img_to_base64("logo2.png")

    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; gap: 20px; margin-bottom: 1.5rem;">
            <div style="flex: 1; background: #ffffff; border: 2px solid #1a1a2e; padding: 12px; display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{logo1}" style="max-height: 90px; object-fit: contain;">
            </div>
            <div style="flex: 1; background: #ffffff; border: 2px solid #1a1a2e; padding: 12px; display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{logo2}" style="max-height: 90px; object-fit: contain;">
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1>השתתפות במחקר בנושא בינה מלאכותית</h1>", unsafe_allow_html=True)

    st.markdown("""
        <div class="intro-text">
            שלום רב,<br><br>
            אנו מודים לך על הסכמתך להשתתף במחקר שלנו. במהלך הניסוי יוצגו בפניך כ-20 תמונות, כשמתחת לכל אחת מהן
            מופיע תיאור מילולי שהופק על ידי מודל בינה מלאכותית. נבקשך לדרג את מידת שביעות הרצון שלך מהתיאור
            על גבי סקלה שבין 1 (לא מרוצה בכלל) ל-100 (מרוצה מאוד).<br><br>
            <strong>מידע חשוב:</strong>
            <ul>
                <li>הניסוי מיועד לדוברי עברית כשפת אם שיודעים/ות אנגלית ברמת בינונית ומעלה.</li>
                <li>הסקר אנונימי לחלוטין והנתונים שיאספו ישמשו למטרות מחקר בלבד.</li>
            </ul>
            <br>תודה על השתתפותך!
        </div>
    """, unsafe_allow_html=True)

    if st.button("להתחלה"):
        st.session_state.stage = "experiment"
        st.rerun()

# ─────────────────────────────────────────
# EXPERIMENT
# ─────────────────────────────────────────
elif st.session_state.stage == "experiment":
    stimuli = st.session_state.stimuli
    idx = st.session_state.current_index
    total = len(stimuli)

    if total == 0:
        st.warning("No stimuli found in the database yet. Please seed the database first.")
        st.stop()

    st.progress(idx / total)
    st.markdown(f'<div class="counter">תמונה {idx + 1} מתוך {total}</div>', unsafe_allow_html=True)

    stimulus = stimuli[idx]

    st.markdown(f"""
        <div style="display:flex; justify-content:center; margin-bottom:1rem;">
            <img src="{stimulus['image_url']}" style="max-height:350px; max-width:100%; object-fit:contain; border-radius:0px;">
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="caption-label">תיאור:</div>', unsafe_allow_html=True)
    st.markdown(stimulus["caption"])

    # Track whether user has touched the slider
    touched_key = f"touched_{idx}"
    if touched_key not in st.session_state:
        st.session_state[touched_key] = False

    # Track whether user tried to submit without rating
    tried_key = f"tried_{idx}"
    if tried_key not in st.session_state:
        st.session_state[tried_key] = False

    st.markdown("""
        <div style="display:flex; justify-content:space-between; font-size:0.9rem;
                    font-weight:600; color:#1a1a2e; margin-bottom:0.2rem; direction:ltr;">
            <span>1</span><span>100</span>
        </div>
    """, unsafe_allow_html=True)

    rating = st.slider(
        "כמה את/ה מרוצה מהתיאור?",
        min_value=0, max_value=100,
        value=0,
        key=f"slider_{idx}",
        label_visibility="visible"
    )

    if not st.session_state[touched_key] and rating != 0:
        st.session_state[touched_key] = True
        st.rerun()

    has_rated = st.session_state[touched_key]

    if not has_rated:
        st.markdown("""
            <style>
                div.stButton > button {
                    background-color: #b0aaa0 !important;
                    color: #e0ddd8 !important;
                    cursor: default !important;
                }
                div.stButton > button:hover {
                    background-color: #b0aaa0 !important;
                    color: #e0ddd8 !important;
                }
                div.stButton > button p {
                    color: #e0ddd8 !important;
                }
            </style>
        """, unsafe_allow_html=True)

    col_btn, col_msg = st.columns([2, 3])

    with col_btn:
        clicked = st.button("הבא ←" if idx < total - 1 else "סיום", key=f"next_{idx}")

    with col_msg:
        if st.session_state[tried_key] and not has_rated:
            st.markdown(
                '<p style="color:#c0392b; font-size:1rem; margin-top:0.6rem;">אנא דרג/י את התיאור</p>',
                unsafe_allow_html=True
            )

    if clicked:
        if not has_rated:
            st.session_state[tried_key] = True
            st.rerun()
        else:
            st.session_state.ratings.append({
                "stimulus_id": str(stimulus["_id"]),
                "error_type": stimulus.get("error_type"),
                "rating": rating
            })
            if idx < total - 1:
                st.session_state.current_index += 1
                st.rerun()
            else:
                save_response(
                    st.session_state.participant_id,
                    st.session_state.ratings
                )
                st.session_state.stage = "done"
                st.rerun()

# ─────────────────────────────────────────
# DONE
# ─────────────────────────────────────────
elif st.session_state.stage == "done":
    st.markdown("""
        <div class="thank-you">
            תגובתך נרשמה.<br>תודה על השתתפותך במחקר!
        </div>
    """, unsafe_allow_html=True)