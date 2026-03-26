import streamlit as st
import random
import time

# 1. Page Configuration
st.set_page_config(page_title="MSc Periodic Master", page_icon="🧪", layout="wide")

# 2. Advanced Curriculum Data
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

# 3. Custom CSS for Visual Design and Dynamic Rotation
st.markdown("""
    <style>
    .wheel-container { display: flex; justify-content: center; align-items: center; height: 350px; position: relative; }
    .wheel {
        width: 250px; height: 250px; border-radius: 50%; border: 8px solid #FFD700;
        position: relative; overflow: hidden;
        background: conic-gradient(#FF4136 0% 20%, #0074D9 20% 40%, #2ECC40 40% 60%, #FFDC00 60% 80%, #B10DC9 80% 100%);
        transition: transform 3s cubic-bezier(0.1, 0, 0, 1);
        z-index: 1;
    }
    .wheel-pointer {
        position: absolute; top: 25px; width: 0; height: 0; 
        border-left: 15px solid transparent; border-right: 15px solid transparent;
        border-top: 30px solid #333; z-index: 10;
    }
    .wheel-num { position: absolute; font-weight: bold; color: white; font-size: 24px; pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)

# 4. Global Session State Initialization
if 'level' not in st.session_state: st.session_state.level = 1
if 'score' not in st.session_state: st.session_state.score = 0
if 'mode' not in st.session_state: st.session_state.mode = "spin"
if 'answered_ids' not in st.session_state: st.session_state.answered_ids = []
if 'current_q_data' not in st.session_state: st.session_state.current_q_data = None
if 'rotation' not in st.session_state: st.session_state.rotation = 0

# --- Helper Function to Render the Wheel ---
def render_wheel(rotation_angle):
    wheel_html = f"""
        <div class="wheel-container">
            <div class="wheel-pointer"></div>
            <div class="wheel" style="transform: rotate({rotation_angle}deg);">
                <div class="wheel-num" style="top:10%; left:45%;">1</div>
                <div class="wheel-num" style="top:40%; left:75%;">2</div>
                <div class="wheel-num" style="top:75%; left:45%;">3</div>
                <div class="wheel-num" style="top:40%; left:15%;">4</div>
                <div class="wheel-num" style="top:10%; left:15%;">5</div>
            </div>
        </div>
    """
    return wheel_html

# --- SCREEN 1: THE SPIN WHEEL ---
if st.session_state.mode == "spin":
    st.header(f"Level {st.session_state.level}: {st.session_state.levels_data[st.session_state.level]['name']}")
    st.write(f"Questions completed: **{len(st.session_state.answered_ids)}/5**")
    
    wheel_placeholder = st.empty()
    wheel_placeholder.markdown(render_wheel(st.session_state.rotation), unsafe_allow_html=True)
    
    if st.button("🚀 SPIN THE CHEMICAL WHEEL", use_container_width=True):
        # 1. Pick a random unanswered question
        available = [q for q in st.session_state.levels_data[st.session_state.level]["data"] 
                     if q["id"] not in st.session_state.answered_ids]
        
        target_q = random.choice(available)
        st.session_state.current_q_data = target_q
        
        # 2. Logic: Calculate Rotation Angle
        # Each segment is 72 degrees. We add 1440 (4 full spins) for effect.
        # We subtract the degrees because the pointer is at the TOP.
        offsets = {1: 0, 2: -72, 3: -144, 4: -216, 5: -288}
        st.session_state.rotation += 1440 + offsets[target_q['id']]
        
        # 3. Show Animation
        wheel_placeholder.markdown(render_wheel(st.session_state.rotation), unsafe_allow_html=True)
        
        with st.status("Spinning for Atomic Data...") as status:
            time.sleep(3.2)
            status.update(label=f"🎯 Success! Landed on Question {target_q['id']}", state="complete")
        
        st.session_state.mode = "quiz"
        st.rerun()

# --- SCREEN 2: THE SCIENTIFIC QUIZ ---
elif st.session_state.mode == "quiz":
    q = st.session_state.current_q_data
    st.subheader(f"📍 Question {q['id']}")
    
    st.info(f"**CHALLENGE:** {q['q']}")
    
    ans = st.radio("Select the correct scientific option:", q["options"], index=None)

    if st.button("SUBMIT RESEARCH DATA", use_container_width=True):
        if ans == q["ans"]:
            st.success("✅ Excellent! Correct answer.")
            st.session_state.score += 20
        else:
            st.error(f"❌ Incorrect. The correct answer was {q['ans']}")
        
        st.session_state.answered_ids.append(q["id"])
        time.sleep(2)
        
        # Check if level is finished
        if len(st.session_state.answered_ids) < 5:
            st.session_state.mode = "spin"
        else:
            st.session_state.mode = "review"
        st.rerun()

# --- SCREEN 3: LEVEL REVIEW (Curriculum Feedback) ---
elif st.session_state.mode == "review":
    st.balloons()
    st.header(f"🏁 Level {st.session_state.level} Complete!")
    st.write("### Scientific Review Session")
    st.write("Review these facts to improve your chemistry proficiency:")
    
    review_list = st.session_state.levels_data[st.session_state.level]["data"]
    for item in review_list:
        with st.expander(f"Question {item['id']} Analysis"):
            st.markdown(f"**The Question:** {item['q']}")
            st.success(f"**The Correct Fact:** {item['ans']}")

    st.write("---")
    st.subheader(f"Current Total Score: {st.session_state.score}")
    
    next_btn_text = "Unlock Next Level Gate" if st.session_state.level < 2 else "Final Evaluation"
    if st.button(next_btn_text, use_container_width=True):
        if st.session_state.level < 2:
            st.session_state.level += 1
            st.session_state.answered_ids = []
            st.session_state.mode = "spin"
        else:
            st.session_state.mode = "end"
        st.rerun()

# --- SCREEN 4: FINAL CERTIFICATION ---
elif st.session_state.mode == "end":
    st.header("🏆 MASTER CHEMIST CERTIFIED")
    st.write("You have successfully completed the MSc Periodic Table Quest.")
    st.metric("Final Proficiency Score", f"{st.session_state.score} / 200")
    
    if st.button("Restart New Research Project", use_container_width=True):
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.answered_ids = []
        st.session_state.mode = "spin"
        st.session_state.rotation = 0
        st.rerun()
                     
