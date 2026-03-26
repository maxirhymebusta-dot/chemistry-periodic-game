import streamlit as st
import random
import time

# 1. Page Configuration
st.set_page_config(page_title="MSc Periodic Master", page_icon="🧪", layout="wide")

# Custom CSS for Background and Glassmorphism
st.markdown("""
<style>
@keyframes backgroundAnimation {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stApp {
    background: linear-gradient(-45deg, #1a1a2e, #16213e, #1a1a2e);
    background-size: 400% 400%;
    animation: backgroundAnimation 20s ease infinite;
}
.main-title { text-align: center; color: #4facfe !important; font-size: 45px; font-weight: 800; text-shadow: 0 0 10px rgba(79, 172, 254, 0.5); }
.subtitle { text-align: center; color: #b8c1ec !important; font-size: 18px; margin-bottom: 30px; }
.wheel-container { display: flex; justify-content: center; align-items: center; height: 350px; position: relative; }
.wheel {
    width: 250px; height: 250px; border-radius: 50%; border: 8px solid #FFD700;
    position: relative; overflow: hidden;
    background: conic-gradient(#FF4136 0% 20%, #0074D9 20% 40%, #2ECC40 40% 60%, #FFDC00 60% 80%, #B10DC9 80% 100%);
    transition: transform 3s cubic-bezier(0.1, 0, 0, 1);
    z-index: 1;
}
.wheel-pointer { position: absolute; top: 15px; width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-top: 40px solid #FFD700; z-index: 10; }
.wheel-num { position: absolute; font-weight: bold; color: white; font-size: 26px; pointer-events: none; }
.footer { text-align: center; padding: 40px; color: #b8c1ec; font-style: italic; font-size: 14px; }
.stButton>button { background: linear-gradient(45deg, #4facfe, #00f2fe); color: white; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. Data Logic
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

# 3. Session State
if 'level' not in st.session_state: st.session_state.level = 1
if 'score' not in st.session_state: st.session_state.score = 0
if 'mode' not in st.session_state: st.session_state.mode = "spin"
if 'answered_ids' not in st.session_state: st.session_state.answered_ids = []
if 'current_q_data' not in st.session_state: st.session_state.current_q_data = None
if 'rotation' not in st.session_state: st.session_state.rotation = 0

def render_wheel(rotation_angle):
    return f"""
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

# --- UI CONTENT ---
st.markdown('<h1 class="main-title">🧪 Periodic Table: The Grand Quest</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Developed by Ukazim Chidinma Favour</p>', unsafe_allow_html=True)

# --- SCREEN 1: SPIN ---
if st.session_state.mode == "spin":
    st.write(f"### 📍 Level {st.session_state.level}: {st.session_state.levels_data[st.session_state.level]['name']}")
    wheel_placeholder = st.empty()
    wheel_placeholder.markdown(render_wheel(st.session_state.rotation), unsafe_allow_html=True)
    
    if st.button("🚀 SPIN THE WHEEL", use_container_width=True):
        available = [q for q in st.session_state.levels_data[st.session_state.level]["data"] if q["id"] not in st.session_state.answered_ids]
        target_q = random.choice(available)
        st.session_state.current_q_data = target_q
        target_stop = -( (target_q['id'] - 1) * 72 + 36 )
        st.session_state.rotation += 1440 + (target_stop - (st.session_state.rotation % 360))
        wheel_placeholder.markdown(render_wheel(st.session_state.rotation), unsafe_allow_html=True)
        with st.status("Analyzing...") : time.sleep(3)
        st.session_state.mode = "quiz"
        st.rerun()

# --- SCREEN 2: QUIZ ---
elif st.session_state.mode == "quiz":
    q = st.session_state.current_q_data
    st.subheader(f"🔍 Question {q['id']}")
    st.info(f"**CHALLENGE:** {q['q']}")
    ans = st.radio("Select an answer:", q["options"], index=None)
    
    if st.button("SUBMIT ANSWER", use_container_width=True):
        if ans == q["ans"]:
            st.success("✅ Correct!")
            st.session_state.score += 20
        else:
            st.error(f"❌ Incorrect. It was {q['ans']}")
        st.session_state.answered_ids.append(q["id"])
        time.sleep(2)
        if len(st.session_state.answered_ids) < 5: st.session_state.mode = "spin"
        else: st.session_state.mode = "review"
        st.rerun()

# --- SCREEN 3: REVIEW ---
elif st.session_state.mode == "review":
    st.balloons()
    st.header(f"🏁 Level {st.session_state.level} Complete!")
    for item in st.session_state.levels_data[st.session_state.level]["data"]:
        with st.expander(f"Review Question {item['id']}"):
            st.write(item['q'])
            st.success(f"Fact: {item['ans']}")
    if st.button("Next Level Gate" if st.session_state.level < 2 else "Final Results", use_container_width=True):
        if st.session_state.level < 2:
            st.session_state.level += 1
            st.session_state.answered_ids = []
            st.session_state.mode = "spin"
        else: st.session_state.mode = "end"
        st.rerun()

# --- SCREEN 4: END ---
elif st.session_state.mode == "end":
    st.header("🏆 MASTER CHEMIST CERTIFIED")
    st.metric("Final Score", f"{st.session_state.score} / 200")
    if st.button("Restart Journey"):
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.answered_ids = []
        st.session_state.mode = "spin"
        st.session_state.rotation = 0
        st.rerun()

st.markdown('<div class="footer">Game Developed by Ukazim Chidinma Favour</div>', unsafe_allow_html=True)
        
