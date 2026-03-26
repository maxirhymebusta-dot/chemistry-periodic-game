import streamlit as st
import random
import time

# 1. Page Config
st.set_page_config(page_title="MSc Periodic Quest: Spin Edition", page_icon="🎡", layout="wide")

# 2. Advanced Curriculum Data (Scientific Properties)
levels_data = {
    1: {"name": "Period 1 & 2 Essentials", "data": [
        {"q": "Which element has an **Atomic Number of 6**?", "options": ["A) Nitrogen", "B) Carbon", "C) Oxygen", "D) Boron"], "ans": "B) Carbon"},
        {"q": "What is the **Molar Mass** of Oxygen (O)?", "options": ["A) 8 g/mol", "B) 12 g/mol", "C) 16 g/mol", "D) 32 g/mol"], "ans": "C) 16 g/mol"},
        {"q": "Identify the element with configuration **1s² 2s¹**.", "options": ["A) Helium", "B) Lithium", "C) Beryllium", "D) Sodium"], "ans": "B) Lithium"},
        {"q": "Which element is a Noble Gas in Period 1?", "options": ["A) Neon", "B) Argon", "C) Hydrogen", "D) Helium"], "ans": "D) Helium"},
        {"q": "Atomic Number 7 belongs to which element?", "options": ["A) Nitrogen", "B) Fluorine", "C) Neon", "D) Carbon"], "ans": "A) Nitrogen"}
    ]},
    2: {"name": "Group 1 & 2 (Reactive Metals)", "data": [
        {"q": "Which Alkali Metal has a **Molar Mass of ~23 g/mol**?", "options": ["A) Lithium", "B) Potassium", "C) Sodium", "D) Magnesium"], "ans": "C) Sodium"},
        {"q": "What is the **Atomic Number of Calcium (Ca)**?", "options": ["A) 12", "B) 20", "C) 19", "D) 30"], "ans": "B) 20"},
        {"q": "Which Group 2 element burns with a white flame?", "options": ["A) Beryllium", "B) Calcium", "C) Magnesium", "D) Barium"], "ans": "C) Magnesium"},
        {"q": "Identify the element: Group 1, Period 4.", "options": ["A) Sodium", "B) Potassium", "C) Rubidium", "D) Cesium"], "ans": "B) Potassium"},
        {"q": "What is the valency of elements in Group 2?", "options": ["A) +1", "B) +2", "C) -2", "D) 0"], "ans": "B) +2"}
    ]},
    # ... Levels 3 and 4 follow the same pattern
}

# --- Session State Management ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'mode' not in st.session_state: st.session_state.mode = "spin" # Modes: spin, quiz, level_up, end

# --- UI Header ---
st.title("🎡 Periodic Table: Spin & Win")
st.progress(min((st.session_state.level - 1) / 4, 1.0))

# --- SCREEN 1: THE SPIN WHEEL ---
if st.session_state.mode == "spin":
    st.header(f"Ready for Level {st.session_state.level}?")
    st.write(f"Click the button below to spin the chemical wheel and generate your questions!")
    
    if st.button("🔄 SPIN THE WHEEL"):
        with st.spinner('Spinning for Elements...'):
            time.sleep(2) # Simulates the spin time
        st.success(f"Successfully loaded 5 questions for {levels_data[st.session_state.level]['name']}!")
        st.session_state.mode = "quiz"
        st.rerun()

# --- SCREEN 2: THE QUIZ ---
elif st.session_state.mode == "quiz":
    curr_level_info = levels_data[st.session_state.level]
    q_data = curr_level_info["data"][st.session_state.q_idx]

    st.subheader(f"📍 {curr_level_info['name']}")
    st.markdown(f"**Question {st.session_state.q_idx + 1} of 5**")
    
    # Beautified Clue Box
    st.info(q_data["q"])
    
    user_choice = st.radio("Select your answer:", q_data["options"], index=None)

    if st.button("Submit Answer"):
        if user_choice == q_data["ans"]:
            st.toast("✅ Correct!", icon="🎉")
            st.session_state.score += 20
        else:
            st.toast(f"❌ Wrong! Correct: {q_data['ans']}", icon="⚠️")
        
        if st.session_state.q_idx < 4:
            st.session_state.q_idx += 1
            st.rerun()
        else:
            if st.session_state.level < 4:
                st.session_state.mode = "level_up"
            else:
                st.session_state.mode = "end"
            st.rerun()

# --- SCREEN 3: LEVEL CONGRATULATIONS ---
elif st.session_state.mode == "level_up":
    st.balloons()
    st.header(f"🌟 Level {st.session_state.level} Mastered!")
    st.write(f"Current Score: **{st.session_state.score}**")
    
    if st.button("Go to next Level Gate"):
        st.session_state.level += 1
        st.session_state.q_idx = 0
        st.session_state.mode = "spin" # Goes back to spin for the new level
        st.rerun()

# --- SCREEN 4: FINAL RESULTS ---
elif st.session_state.mode == "end":
    st.header("🏆 MASTER CHEMIST CERTIFIED!")
    st.metric("Final Score", f"{st.session_state.score} / 400")
    if st.button("Start New Experiment"):
        st.session_state.level = 1
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.mode = "spin"
        st.rerun()
        
