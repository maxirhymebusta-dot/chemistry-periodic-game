import streamlit as st
import random
import time

# 1. Page Config
st.set_page_config(page_title="MSc Periodic Master: Spin Edition", page_icon="🎡", layout="wide")

# 2. Advanced Curriculum Data
levels_data = {
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

# --- Session State ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'mode' not in st.session_state: st.session_state.mode = "spin" # spin, quiz, review, end

# --- UI Header ---
st.title("🎡 Periodic Master: Spin Quest")
st.sidebar.metric("Total Score", st.session_state.score)

# --- SCREEN 1: THE SPIN WHEEL ---
if st.session_state.mode == "spin":
    st.header(f"Level {st.session_state.level}: {levels_data[st.session_state.level]['name']}")
    st.write("Click below to spin for your next question!")
    
    # The "Visual Wheel" Container
    wheel_placeholder = st.empty()
    wheel_placeholder.markdown("<h1 style='text-align: center; font-size: 100px;'>🎡</h1>", unsafe_allow_html=True)
    
    if st.button("🚀 SPIN NOW"):
        # Simulated Spin Animation
        numbers = [1, 2, 3, 4, 5]
        for _ in range(15): # Cycle 15 times
            random_num = random.choice(numbers)
            wheel_placeholder.markdown(f"<h1 style='text-align: center; color: #007bff; font-size: 80px;'>{random_num}</h1>", unsafe_allow_html=True)
            time.sleep(0.1)
        
        # Land on the actual current question number
        landing_num = st.session_state.q_idx + 1
        wheel_placeholder.markdown(f"<h1 style='text-align: center; color: #28a745; font-size: 100px;'>{landing_num}</h1>", unsafe_allow_html=True)
        st.success(f"Landed on Question {landing_num}!")
        time.sleep(1)
        st.session_state.mode = "quiz"
        st.rerun()

# --- SCREEN 2: THE QUIZ ---
elif st.session_state.mode == "quiz":
    q_list = levels_data[st.session_state.level]["data"]
    q_data = q_list[st.session_state.q_idx]

    st.subheader(f"Question {st.session_state.q_idx + 1} of 5")
    st.info(q_data["q"])
    
    ans = st.radio("Select Answer:", q_data["options"], index=None)

    if st.button("Submit"):
        if ans == q_data["ans"]:
            st.toast("Correct!", icon="✅")
            st.session_state.score += 20
        else:
            st.toast("Incorrect", icon="❌")
        
        # Logic to move to next spin or review
        if st.session_state.q_idx < 4:
            st.session_state.q_idx += 1
            st.session_state.mode = "spin"
        else:
            st.session_state.mode = "review"
        st.rerun()

# --- SCREEN 3: LEVEL REVIEW (Correct Answers) ---
elif st.session_state.mode == "review":
    st.balloons()
    st.header(f"🏁 Level {st.session_state.level} Complete!")
    st.subheader("Scientific Review: Correct Answers")
    
    # Create a table of correct answers for the level
    review_data = levels_data[st.session_state.level]["data"]
    for item in review_data:
        st.write(f"**Q{item['id']}:** {item['q']}")
        st.success(f"Correct Answer: {item['ans']}")
        st.write("---")
    
    if st.button("Next Level Gate" if st.session_state.level < 2 else "Final Results"):
        if st.session_state.level < 2:
            st.session_state.level += 1
            st.session_state.q_idx = 0
            st.session_state.mode = "spin"
        else:
            st.session_state.mode = "end"
        st.rerun()

# --- SCREEN 4: END ---
elif st.session_state.mode == "end":
    st.header("🏆 Master Chemist Certified")
    st.metric("Final Score", f"{st.session_state.score} / 200")
    if st.button("Restart"):
        st.session_state.level = 1
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.mode = "spin"
        st.rerun()
        
