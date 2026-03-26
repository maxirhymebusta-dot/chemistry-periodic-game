import streamlit as st
import random
import time
import json

# 1. Page Configuration & Custom CSS for the Dynamic Background
st.set_page_config(page_title="MSc Periodic Master", page_icon="🧪", layout="wide")

st.markdown("""
<style>
/* 1. Animated Chemistry Background */
@keyframes backgroundAnimation {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes particleRotate {
    from { transform: rotate(0deg) translate(20px) rotate(0deg); }
    to { transform: rotate(360deg) translate(20px) rotate(-360deg); }
}

.stApp {
    background: linear-gradient(-45deg, #1a1a2e, #16213e, #1a1a2e);
    background-size: 400% 400%;
    animation: backgroundAnimation 20s ease infinite;
    overflow: hidden;
}

/* Glassmorphism Containers */
[data-testid="stVerticalBlock"] > div:has(div.instruction-box),
[data-testid="stVerticalBlock"] > div:has(div.wheel-container),
.stExpander {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 20px;
    margin-bottom: 20px;
}

/* 2. Text Beautification */
h1, h2, h3, h4, .stMarkdown, p, li, label {
    color: #e0e0e0 !important;
    font-family: 'Poppins', sans-serif;
}

.main-title {
    text-align: center;
    color: #4facfe !important; /* Cool Blue */
    font-size: 50px;
    font-weight: 800;
    margin-bottom: 0px;
    text-shadow: 0 0 10px rgba(79, 172, 254, 0.5);
}

.subtitle {
    text-align: center;
    color: #b8c1ec !important; /* Soft Blue/Purple */
    font-size: 18px;
    margin-bottom: 40px;
}

/* 3. Instruction Box Update */
.instruction-box {
    color: #e0e0e0;
    border-left: 5px solid #4facfe;
    background-color: transparent !important;
}

/* 4. The Spinning Wheel Design */
.wheel-container { display: flex; justify-content: center; align-items: center; height: 350px; position: relative; }
.wheel {
    width: 250px; height: 250px; border-radius: 50%; border: 8px solid #FFD700;
    position: relative; overflow: hidden;
    /* We use brighter colors for the segments so they pop against the dark background */
    background: conic-gradient(#FF4136 0% 20%, #2ECC40 20% 40%, #0074D9 40% 60%, #FFDC00 60% 80%, #B10DC9 80% 100%);
    transition: transform 3s cubic-bezier(0.1, 0, 0, 1);
    z-index: 1;
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}
.wheel-pointer { position: absolute; top: 15px; width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-top: 40px solid #FFD700; z-index: 10; }
.wheel-num { position: absolute; font-weight: bold; color: white; font-size: 26px; pointer-events: none; text-shadow: 1px 1px 2px black; }

/* 5. Component Styling */
.stButton>button {
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    color: white; border: none; font-weight: bold; border-radius: 10px;
}
.stButton>button:hover { background: linear-gradient(45deg, #00f2fe, #4facfe); }
.stProgress > div > div > div > div { background-color: #4facfe; }

/* 6. Radio (ABCD) options text color */
[data-testid="stMarkdownContainer"] p {
    color: white;
}

/* 7. Footer */
.footer { text-align: center; padding: 40px; color: #b8c1ec; font-style: italic; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# 2. Add Animated Chemistry Background Icons (SVGs)
st.markdown("""
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; opacity: 0.15; pointer-events: none;">
    <svg width="60" height="60" viewBox="0 0 60 60" style="position: absolute; top: 10%; left: 5%; animation: particleRotate 10s linear infinite;">
        <path d="M48 40V12H36V8H24V12H12V40C12 46.6 17.4 52 24 52H36C42.6 52 48 46.6 48 40ZM28 12H32V40C32 42.2 30.2 44 28 44H20C17.8 44 16 42.2 16 40V12H20V20H24V12H28Z" fill="#b8c1ec"/>
    </svg>
    <svg width="80" height="80" viewBox="0 0 100 100" style="position: absolute; top: 15%; right: 10%; animation: particleRotate 15s linear infinite;">
        <circle cx="20" cy="50" r="15" stroke="#b8c1ec" stroke-width="3" fill="none"/>
        <circle cx="80" cy="50" r="15" stroke="#b8c1ec" stroke-width="3" fill="none"/>
        <line x1="35" y1="50" x2="65" y2="50" stroke="#b8c1ec" stroke-width="3"/>
        <line x1="35" y1="50" x2="65" y2="50" stroke="#b8c1ec" stroke-width="3"/>
    </svg>
    <svg width="100" height="100" viewBox="0 0 100 100" style="position: absolute; bottom: 15%; left: 10%; animation: particleRotate 20s linear infinite;">
        <circle cx="50" cy="50" r="10" fill="#b8c1ec"/>
        <ellipse cx="50" cy="50" rx="40" ry="15" stroke="#b8c1ec" stroke-width="3" fill="none" transform="rotate(45 50 50)"/>
        <ellipse cx="50" cy="50" rx="40" ry="15" stroke="#b8c1ec" stroke-width="3" fill="none" transform="rotate(-45 50 50)"/>
    </svg>
    <svg width="70" height="70" viewBox="0 0 60 60" style="position: absolute; bottom: 10%; right: 5%; animation: particleRotate 12s linear infinite;">
        <rect x="5" y="5" width="50" height="50" rx="5" stroke="#b8c1ec" stroke-width="3" fill="none"/>
        <text x="30" y="35" text-anchor="middle" font-size="20" fill="#b8c1ec">H</text>
    </svg>
</div>
""", unsafe_allow_html=True)

# 3. Advanced Curriculum Data
if 'levels_data' not in st.session_state:
    st.session_state.levels_data = {
        1: {"name": "Period 1 & 2 Essentials", "data": [
            {"id": 1, "q": "Which element has an **Atomic Number of 6**?", "options": ["A) Nitrogen", "B) Carbon", "C) Oxygen", "D) Boron"], "ans": "B) Carbon"},
            {"id": 2, "q": "What is the **Molar Mass** of Oxygen (O)?", "options": ["A) 8 g/mol", "B) 12 g/mol", "C) 16 g/mol", "D) 32 g/mol"], "ans": "C) 16 g/mol"},
            {"id": 3, "q": "Identify the element with configuration **1s² 2s¹**.", "options": ["A) Helium", "B) Lithium", "C) Beryllium", "D) Sodium"], "ans": "B) Lithium"},
            {"id": 4, "q": "Which element is a Noble Gas in Period 1?", "options": ["A) Neon", "B) Argon", "C) Hydrogen", "D) Helium"], "ans": "D) Helium"},
            {"id": 5, "q": "Atomic Number 7 belongs to which element?", "options": ["A) Nitrogen", "B) Fluorine", "C) Neon", "D) Carbon"], "ans": "A) Nitrogen"}
        ]},
        2: {"name": "Group 1 & 2 (Reactive Metals)", "data": [
            {"id": 1, "q": "Which Alkali Metal has a **Molar Mass of ~23 g/mol**?", "options": ["A) Lithium", "B) Potassium", "C) Sodium", "D) Magnesium"], "ans": "C) Sodium"},
            {"id": 2, "q": "What is the **Atomic Number of Calcium (Ca)**?", "options": ["A) 12", "B) 20", "C) 19", "D) 30"], "ans": "B) 20"},
            {"id": 3, "q": "Which Group 2 element burns with a white flame?", "options": ["A) Beryllium", "B) Calcium", "C) Magnesium", "D) Barium"], "ans": "C) Magnesium"},
            {"id": 4, "q": "Identify the element: Group 1, Period 4.", "options": ["A) Sodium", "B) Potassium", "C) Rubidium", "D) Cesium"], "ans": "B) Potassium"},
            {"id": 5, "q": "What is the valency of elements in Group 2?", "options": ["A) +1", "B) +2", "C) -2", "D) 0"], "ans": "B) +2"}
        ]}
    }

# 4. Global Session State Initialization
if 'level' not in st.session_state: st.session_state.level = 1
if 'score' not in st.session_state: st.session_state.score = 0
if 'mode' not in st.session_state: st.session_state.mode = "spin"
if 'answered_ids' not in st.session_state: st.session_state.answered_ids = []
if 'current_q_data' not in st.session_state: st.session_state.current_q_data = None
if 'rotation' not in st.session_state: st.session_state.rotation = 0

# --- Helper Function for the Wheel ---
def render_wheel(rotation_angle):
    # Centroid mapping: Labels are offset to be in the center of the slices
    wheel_html = f"""
        <div class="wheel-container">
            <div class="wheel-pointer"></div>
            <div class="wheel" style="transform: rotate({rotation_angle}deg);">
                <div class="wheel-num" style="top:12%; left:55%; transform: rotate(36deg);">1</div>
                <div class="wheel-num" style="top:48%; left:75%; transform: rotate(108deg);">2</div>
                <div class="wheel-num" style="top:78%; left:40%; transform: rotate(180deg);">3</div>
                <div class="wheel-num" style="top:48%; left:10%; transform: rotate(252deg);">4</div>
                <div class="wheel-num" style="top:12%; left:25%; transform: rotate(324deg);">5</div>
            </div>
        </div>
    """
    return wheel_html

# --- MAIN CONTENT ---
# Use a centered column for gameplay
game_col1, game_col2, game_col3 = st.columns([1, 4, 1])

with game_col2:
    # --- HEADER SECTION ---
    st.markdown('<h1 class="main-title">🧪 Periodic Table: The Grand Quest</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">An Interactive Educational Assessment Tool</p>', unsafe_allow_html=True)

    # --- INSTRUCTIONS ---
    with st.expander("📖 HOW TO PLAY"):
        st.markdown("""
        <div class="instruction-box">
        1. **Spin the Wheel:** Click the spin button to randomly select a challenge from the current Chemical Gate.
        2. **Answer the Question:** Analyze the prompt and select the correct option (A, B, C, or D).
        3. **Unlock gates:** Complete 5 correct analyses per level to progress.
        </div>
        """, unsafe_allow_html=True)

    # --- SCREEN 1: THE SPIN WHEEL ---
    if st.session_state.mode == "spin":
        st.write(f"### 📍 Current Gate: {st.session_state.levels_data[st.session_state.level]['name']}")
        
        # Calculate Progress
        correct_count = len(st.session_state.answered_ids)
        st.write(f"Progress: **{correct_count}/5** Questions Analysis Complete")
        st.progress(correct_count / 5)
        
        # The Wheel Graphic
        wheel_placeholder = st.empty()
        wheel_placeholder.markdown(render_wheel(st.session_state.rotation), unsafe_allow_html=True)
        
        if st.button("🚀 SPIN FOR A CHALLENGE", use_container_width=True):
            available = [q for q in st.session_state.levels_data[st.session_state.level]["data"] if q["id"] not in st.session_state.answered_ids]
            target_q = random.choice(available)
            st.session_state.current_q_data = target_q
            
            target_stop = -( (target_q['id'] - 1) * 72 + 36 )
            st.session_state.rotation += 1440 + (target_stop - (st.session_state.rotation % 360))
            
            wheel_placeholder.markdown(render_wheel(st.session_state.rotation), unsafe_allow_html=True)
            
            with st.status("Analyzing Atomic Structures...") as status:
                time.sleep(3)
                status.update(label=f"🎯 Landed on Question {target_q['id']}!", state="complete")
            
            st.session_state.mode = "quiz"
            st.rerun()

    # --- SCREEN 2: THE SCIENTIFIC QUIZ ---
    elif st.session_state.mode == "quiz":
        q = st.session_state.current_q_data
        st.subheader(f"🔍 Scientific Analysis: Question {q['id']}")
        
        st.info(f"**CHALLENGE:** {q['q']}")
        
        ans = st.radio("Select your scientific option:", q["options"], index=None)

    # --- FOOTER ---
    st.markdown('<div class="footer">Game Developed by Ukazim Chidinma Favour</div>', unsafe_allow_html=True)
    
