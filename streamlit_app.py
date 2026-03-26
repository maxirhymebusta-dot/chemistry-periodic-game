import streamlit as st
import random
import time

# 1. Page Configuration
st.set_page_config(page_title="MSc Periodic Master", page_icon="🧪", layout="wide")

# 2. Complete 8-Level Curriculum Data
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
        ]},
        3: {"name": "The Halogens (Group 17)", "data": [
            {"id": 1, "q": "Which Halogen is a liquid at room temperature?", "options": ["A) Fluorine", "B) Chlorine", "C) Bromine", "D) Iodine"], "ans": "C) Bromine"},
            {"id": 2, "q": "What is the **Atomic Number of Fluorine (F)**?", "options": ["A) 7", "B) 8", "C) 9", "D) 10"], "ans": "C) 9"},
            {"id": 3, "q": "Which element is the most electronegative?", "options": ["A) Oxygen", "B) Fluorine", "C) Chlorine", "D) Nitrogen"], "ans": "B) Fluorine"},
            {"id": 4, "q": "What is the common oxidation state of Halogens?", "options": ["A) +1", "B) -1", "C) +7", "D) -2"], "ans": "B) -1"},
            {"id": 5, "q": "Which Halogen is used as a purple antiseptic?", "options": ["A) Chlorine", "B) Bromine", "C) Iodine", "D) Astatine"], "ans": "C) Iodine"}
        ]},
        4: {"name": "The Noble Gases (Group 18)", "data": [
            {"id": 1, "q": "Which Noble Gas is used in orange neon signs?", "options": ["A) Helium", "B) Neon", "C) Argon", "D) Xenon"], "ans": "B) Neon"},
            {"id": 2, "q": "What is the **Atomic Number of Argon (Ar)**?", "options": ["A) 10", "B) 18", "C) 36", "D) 54"], "ans": "B) 18"},
            {"id": 3, "q": "Why are Noble Gases unreactive?", "options": ["A) Low Density", "B) High Mass", "C) Full Outer Shells", "D) They are rare"], "ans": "C) Full Outer Shells"},
            {"id": 4, "q": "Which Noble Gas is radioactive?", "options": ["A) Krypton", "B) Xenon", "C) Radon", "D) Helium"], "ans": "C) Radon"},
            {"id": 5, "q": "Which is the most abundant Noble Gas in air?", "options": ["A) Helium", "B) Neon", "C) Argon", "D) Radon"], "ans": "C) Argon"}
        ]},
        5: {"name": "Common Transition Metals", "data": [
            {"id": 1, "q": "Which metal has the symbol **Fe**?", "options": ["A) Fluorine", "B) Iron", "C) Francium", "D) Fermium"], "ans": "B) Iron"},
            {"id": 2, "q": "What is the **Atomic Number of Copper (Cu)**?", "options": ["A) 25", "B) 27", "C) 29", "D) 31"], "ans": "C) 29"},
            {"id": 3, "q": "Which metal is used to galvanize steel?", "options": ["A) Nickel", "B) Zinc", "C) Chrome", "D) Tin"], "ans": "B) Zinc"},
            {"id": 4, "q": "What is the symbol for Silver?", "options": ["A) Si", "B) Ag", "C) Au", "D) Sl"], "ans": "B) Ag"},
            {"id": 5, "q": "Which metal is liquid at room temperature?", "options": ["A) Mercury", "B) Gallium", "C) Bromine", "D) Cesium"], "ans": "A) Mercury"}
        ]},
        6: {"name": "Metalloids & Post-Transition", "data": [
            {"id": 1, "q": "Which element is a semiconductor used in chips?", "options": ["A) Carbon", "B) Silicon", "C) Germanium", "D) Boron"], "ans": "B) Silicon"},
            {"id": 2, "q": "What is the symbol for Lead?", "options": ["A) Ld", "B) Le", "C) Pb", "D) Pl"], "ans": "C) Pb"},
            {"id": 3, "q": "Which element has Atomic Number 13?", "options": ["A) Magnesium", "B) Aluminum", "C) Silicon", "D) Phosphorus"], "ans": "B) Aluminum"},
            {"id": 4, "q": "Symbol Sn belongs to which element?", "options": ["A) Antimony", "B) Tin", "C) Selenium", "D) Strontium"], "ans": "B) Tin"},
            {"id": 5, "q": "What is the symbol for Arsenic?", "options": ["A) Ar", "B) As", "C) An", "D) Ae"], "ans": "B) As"}
        ]},
        7: {"name": "The Precious Metals", "data": [
            {"id": 1, "q": "What is the symbol for Gold?", "options": ["A) Gd", "B) Go", "C) Au", "D) Ag"], "ans": "C) Au"},
            {"id": 2, "q": "Which metal is the best conductor of electricity?", "options": ["A) Gold", "B) Silver", "C) Copper", "D) Aluminum"], "ans": "B) Silver"},
            {"id": 3, "q": "Symbol Pt belongs to which metal?", "options": ["A) Plutonium", "B) Platinum", "C) Palladium", "D) Protactinium"], "ans": "B) Platinum"},
            {"id": 4, "q": "What is the Atomic Number of Gold (Au)?", "options": ["A) 47", "B) 79", "C) 80", "D) 92"], "ans": "B) 79"},
            {"id": 5, "q": "Which metal is used in high-end jewelry and catalysts?", "options": ["A) Iron", "B) Nickel", "C) Platinum", "D) Copper"], "ans": "C) Platinum"}
        ]},
        8: {"name": "Radioactive & Heavy Elements", "data": [
            {"id": 1, "q": "Which element is used as fuel in nuclear reactors?", "options": ["A) Thorium", "B) Radium", "C) Uranium", "D) Polonium"], "ans": "C) Uranium"},
            {"id": 2, "q": "What is the symbol for Plutonium?", "options": ["A) Pl", "B) Pt", "C) Pu", "D) Po"], "ans": "C) Pu"},
            {"id": 3, "q": "Which radioactive element was discovered by Marie Curie?", "options": ["A) Uranium", "B) Radium", "C) Radon", "D) Curium"], "ans": "B) Radium"},
            {"id": 4, "q": "What is the Atomic Number of Uranium?", "options": ["A) 88", "B) 90", "C) 92", "D) 94"], "ans": "C) 92"},
            {"id": 5, "q": "Which is the last element on the Periodic Table?", "options": ["A) Radon", "B) Oganesson", "C) Tennessine", "D) Livermorium"], "ans": "B) Oganesson"}
        ]}
    }

# 3. Custom CSS for Dynamic Background & Design
st.markdown("""
<style>
@keyframes backgroundAnimation { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
.stApp {
    background: linear-gradient(-45deg, #1a1a2e, #16213e, #1a1a2e);
    background-size: 400% 400%;
    animation: backgroundAnimation 20s ease infinite;
}
.stExpander, .instruction-box, .wheel-container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 20px;
}
h1, h2, h3, h4, p, li, label, .stMarkdown { color: #e0e0e0 !important; }
.main-title { text-align: center; color: #4facfe !important; font-size: 45px; font-weight: 800; }
.subtitle { text-align: center; color: #b8c1ec !important; font-size: 18px; margin-bottom: 30px; }
.wheel-container { display: flex; justify-content: center; align-items: center; height: 350px; position: relative; }
.wheel {
    width: 250px; height: 250px; border-radius: 50%; border: 8px solid #FFD700;
    position: relative; overflow: hidden;
    background: conic-gradient(#FF4136 0% 20%, #0074D9 20% 40%, #2ECC40 40% 60%, #FFDC00 60% 80%, #B10DC9 80% 100%);
    transition: transform 3s cubic-bezier(0.1, 0, 0, 1);
}
.wheel-pointer { position: absolute; top: 15px; width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-top: 40px solid #FFD700; z-index: 10; }
.wheel-num { position: absolute; font-weight: bold; color: white; font-size: 26px; }
.stButton>button { background: linear-gradient(45deg, #4facfe, #00f2fe); color: white; border-radius: 10px; font-weight: bold; width: 100%; }
.footer { text-align: center; padding: 40px; color: #b8c1ec; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# 4. Session State Management
if 'level' not in st.session_state: st.session_state.level = 1
if 'total_score' not in st.session_state: st.session_state.total_score = 0
if 'level_scores' not in st.session_state: st.session_state.level_scores = {}
if 'mode' not in st.session_state: st.session_state.mode = "spin"
if 'answered_ids' not in st.session_state: st.session_state.answered_ids = []
if 'current_q_data' not in st.session_state: st.session_state.current_q_data = None
if 'rotation' not in st.session_state: st.session_state.rotation = 0
if 'level_temp_score' not in st.session_state: st.session_state.level_temp_score = 0

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

# --- MAIN UI ---
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown('<h1 class="main-title">🛡️ Periodic Table: The Grand Quest</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">MSc Chemistry Educational Assessment</p>', unsafe_allow_html=True)

    with st.expander("📖 HOW TO PLAY"):
        st.markdown("Spin the wheel, select A-D, and master all 8 levels to finish!")

    if st.session_state.mode == "spin":
        st.write(f"### 📍 Level {st.session_state.level}: {st.session_state.levels_data[st.session_state.level]['name']}")
        st.write(f"Questions answered: **{len(st.session_state.answered_ids)}/5**")
        wheel_placeholder = st.empty()
        wheel_placeholder.markdown(render_wheel(st.session_state.rotation), unsafe_allow_html=True)
        
        if st.button("🚀 SPIN FOR A CHALLENGE"):
            available = [q for q in st.session_state.levels_data[st.session_state.level]["data"] if q["id"] not in st.session_state.answered_ids]
            target_q = random.choice(available)
            st.session_state.current_q_data = target_q
            target_stop = -( (target_q['id'] - 1) * 72 + 36 )
            st.session_state.rotation += 1440 + (target_stop - (st.session_state.rotation % 360))
            wheel_placeholder.markdown(render_wheel(st.session_state.rotation), unsafe_allow_html=True)
            with st.status("Analyzing Data...") as status:
                time.sleep(3)
                status.update(label=f"🎯 Question {target_q['id']}!", state="complete")
            st.session_state.mode = "quiz"
            st.rerun()

    elif st.session_state.mode == "quiz":
        q = st.session_state.current_q_data
        st.subheader(f"🔍 Challenge {q['id']}")
        st.info(q["q"])
        ans = st.radio("Choose Answer:", q["options"], index=None)
        if st.button("SUBMIT"):
            if ans == q["ans"]:
                st.success("Correct!")
                st.session_state.level_temp_score += 20
                st.session_state.total_score += 20
            else:
                st.error(f"Incorrect. It was {q['ans']}")
            st.session_state.answered_ids.append(q["id"])
            time.sleep(2)
            if len(st.session_state.answered_ids) < 5: st.session_state.mode = "spin"
            else: 
                st.session_state.level_scores[st.session_state.level] = st.session_state.level_temp_score
                st.session_state.mode = "review"
            st.rerun()

    elif st.session_state.mode == "review":
        st.header(f"🏁 Level {st.session_state.level} Results: {st.session_state.level_temp_score}/100")
        for item in st.session_state.levels_data[st.session_state.level]["data"]:
            with st.expander(f"Question {item['id']}"):
                st.write(item['q'])
                st.success(f"Fact: {item['ans']}")
        
        if st.button("Next Level Gate" if st.session_state.level < 8 else "View Final Certificate"):
            if st.session_state.level < 8:
                st.session_state.level += 1
                st.session_state.answered_ids = []
                st.session_state.level_temp_score = 0 # RESET SCORE FOR NEXT LEVEL
                st.session_state.mode = "spin"
                st.rerun()
            else:
                st.session_state.mode = "end"
                st.rerun()

    elif st.session_state.mode == "end":
        st.header("🏆 MASTER CHEMIST CERTIFIED")
        st.metric("Total Final Score", f"{st.session_state.total_score} / 800")
        for lvl, s in st.session_state.level_scores.items():
            st.write(f"Level {lvl}: {s}/100")
        if st.button("Restart Journey"):
            st.session_state.level = 1
            st.session_state.total_score = 0
            st.session_state.level_scores = {}
            st.session_state.answered_ids = []
            st.session_state.mode = "spin"
            st.rerun()

    st.markdown('<div class="footer">Game Developed by Ukazim Chidinma Favour</div>', unsafe_allow_html=True)
             
