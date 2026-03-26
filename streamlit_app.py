import streamlit as st
import random
import time

# 1. Page Configuration
st.set_page_config(page_title="MSc Periodic Master", page_icon="🧪", layout="wide")

# 2. Scientific Curriculum Data
levels_data = {
    1: {"name": "Period 1 & 2 Essentials", "data": [
        {"id": 1, "q": "Which element has an **Atomic Number of 6** and forms the basis of organic chemistry?", "options": ["A) Nitrogen", "B) Carbon", "C) Oxygen", "D) Boron"], "ans": "B) Carbon"},
        {"id": 2, "q": "What is the **Molar Mass** of Oxygen (O) to the nearest whole number?", "options": ["A) 8 g/mol", "B) 12 g/mol", "C) 16 g/mol", "D) 32 g/mol"], "ans": "C) 16 g/mol"},
        {"id": 3, "q": "Identify the element with the electron configuration **1s² 2s¹**.", "options": ["A) Helium", "B) Lithium", "C) Beryllium", "D) Sodium"], "ans": "B) Lithium"},
        {"id": 4, "q": "Which element is a Noble Gas found in Period 1?", "options": ["A) Neon", "B) Argon", "C) Hydrogen", "D) Helium"], "ans": "D) Helium"},
        {"id": 5, "q": "Atomic Number 7 belongs to which element?", "options": ["A) Nitrogen", "B) Fluorine", "C) Neon", "D) Carbon"], "ans": "A) Nitrogen"}
    ]},
    2: {"name": "Group 1 & 2 (Reactive Metals)", "data": [
        {"id": 1, "q": "Which Alkali Metal has a **Molar Mass of approx. 23 g/mol**?", "options": ["A) Lithium", "B) Potassium", "C) Sodium", "D) Magnesium"], "ans": "C) Sodium"},
        {"id": 2, "q": "What is the **Atomic Number of Calcium (Ca)**?", "options": ["A) 12", "B) 20", "C) 19", "D) 30"], "ans": "B) 20"},
        {"id": 3, "q": "Which Group 2 element burns with a bright white flame?", "options": ["A) Beryllium", "B) Calcium", "C) Magnesium", "D) Barium"], "ans": "C) Magnesium"},
        {"id": 4, "q": "Identify the element located in Group 1, Period 4.", "options": ["A) Sodium", "B) Potassium", "C) Rubidium", "D) Cesium"], "ans": "B) Potassium"},
        {"id": 5, "q": "What is the common valency of elements in Group 2?", "options": ["A) +1", "B) +2", "C) -2", "D) 0"], "ans": "B) +2"}
    ]}
}

# 3. Custom CSS for the Spinning Wheel and UI
st.markdown("""
    <style>
    .wheel-container { display: flex; justify-content: center; align-items: center; height: 320px; position: relative; margin-bottom: 20px; }
    .wheel {
        width: 250px; height: 250px; border-radius: 50%; border: 8px solid #FFD700;
        position: relative; overflow: hidden;
        background: conic-gradient(#FF4136 0% 20%, #0074D9 20% 40%, #2ECC40 40% 60%, #FFDC00 60% 80%, #B10DC9 80% 100%);
    }
    .wheel-pointer {
        position: absolute; top: 15px; width: 0; height: 0; 
        border-left: 15px solid transparent; border-right: 15px solid transparent;
        border-top: 30px solid #333; z-index: 10;
    }
    .spinning { animation: rotate-wheel 3s cubic-bezier(0.1, 0, 0, 1) forwards; }
    @keyframes rotate-wheel { from { transform: rotate(0deg); } to { transform: rotate(1440deg); } }
    .wheel-num { position: absolute; font-weight: bold; color: white; font-size: 22px; }
    </style>
    """, unsafe_allow_html=True)

# 4. Session State Management
if 'level' not in st.session_state: st.session_state.level = 1
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'mode' not in st.session_state: st.session_state.mode = "spin" # spin, quiz, review, end

# --- SCREEN 1: THE SPIN WHEEL ---
if st.session_state.mode == "spin":
    st.header(f"Level {st.session_state.level}: {levels_data[st.session_state.level]['name']}")
    st.write("Click below to spin the chemical wheel for your next question!")
    
    wheel_placeholder = st.empty()
    
    # HTML for the Wheel
    wheel_html = """
        <div class="wheel-container">
            <div class="wheel-pointer"></div>
            <div class="wheel {CLASS}">
                <div class="wheel-num" style="top:15%; left:45%;">1</div>
                <div class="wheel-num" style="top:40%; left:75%;">2</div>
                <div class="wheel-num" style="top:75%; left:45%;">3</div>
                <div class="wheel-num" style="top:40%; left:15%;">4</div>
                <div class="wheel-num" style="top:15%; left:15%;">5</div>
            </div>
        </div>
    """
    
    wheel_placeholder.markdown(wheel_html.format(CLASS=""), unsafe_allow_html=True)
    
    if st.button("🚀 SPIN THE WHEEL", use_container_width=True):
        wheel_placeholder.markdown(wheel_html.format(CLASS="spinning"), unsafe_allow_html=True)
        with st.status("Analyzing Atomic Data...") as status:
            time.sleep(3.2)
            status.update(label=f"Landed on Question {st.session_state.q_idx + 1}!", state="complete")
        st.session_state.mode = "quiz"
        st.rerun()

# --- SCREEN 2: THE QUIZ ---
elif st.session_state.mode == "quiz":
    q_list = levels_data[st.session_state.level]["data"]
    q_data = q_list[st.session_state.q_idx]

    st.subheader(f"Level {st.session_state.level} | Question {st.session_state.q_idx + 1} of 5")
    st.info(f"🔍 **CHALLENGE:** {q_data['q']}")
    
    ans = st.radio("Select the correct scientific option:", q_data["options"], index=None)

    if st.button("Submit Answer", use_container_width=True):
        if ans == q_data["ans"]:
            st.success("✅ Correct! Excellent understanding.")
            st.session_state.score += 20
        else:
            st.error(f"❌ Incorrect. The correct answer was {q_data['ans']}")
        
        time.sleep(1.5)
        if st.session_state.q_idx < 4:
            st.session_state.q_idx += 1
            st.session_state.mode = "spin"
        else:
            st.session_state.mode = "review"
        st.rerun()

# --- SCREEN 3: LEVEL REVIEW ---
elif st.session_state.mode == "review":
    st.balloons()
    st.header(f"🏁 Level {st.session_state.level} Summary")
    st.subheader("Scientific Review Session")
    st.write("Examine the correct answers below to reinforce your chemical knowledge:")
    
    review_data = levels_data[st.session_state.level]["data"]
    for item in review_data:
        with st.expander(f"Question {item['id']} Analysis"):
            st.write(f"**Question:** {item['q']}")
            st.success(f"**Correct Scientific Answer:** {item['ans']}")
    
    st.write(f"### Current Total Score: {st.session_state.score}")
    
    btn_text = "Proceed to Next Level Gate" if st.session_state.level < 2 else "View Final Certification"
    if st.button(btn_text, use_container_width=True):
        if st.session_state.level < 2:
            st.session_state.level += 1
            st.session_state.q_idx = 0
            st.session_state.mode = "spin"
        else:
            st.session_state.mode = "end"
        st.rerun()

# --- SCREEN 4: FINAL RESULTS ---
elif st.session_state.mode == "end":
    st.header("🏆 MASTER CHEMIST CERTIFIED")
    st.write("Congratulations! You have completed the Periodic Table Scientific Quest.")
    st.metric("Final Proficiency Score", f"{st.session_state.score} / 200")
    
    if st.button("Restart New Research Session", use_container_width=True):
        st.session_state.level = 1
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.mode = "spin"
        st.rerun()
    
