import streamlit as st
import random

# 1. Page Config
st.set_page_config(page_title="MSc Chemistry Master", page_icon="🧪", layout="wide")

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
    3: {"name": "The Halogens (Group 17)", "data": [
        {"q": "Which Halogen is a liquid at room temperature?", "options": ["A) Fluorine", "B) Chlorine", "C) Bromine", "D) Iodine"], "ans": "C) Bromine"},
        {"q": "What is the **Atomic Number of Fluorine (F)**?", "options": ["A) 7", "B) 8", "C) 9", "D) 10"], "ans": "C) 9"},
        {"q": "Which element is the most electronegative?", "options": ["A) Oxygen", "B) Fluorine", "C) Chlorine", "D) Nitrogen"], "ans": "B) Fluorine"},
        {"q": "What is the common oxidation state of Halogens?", "options": ["A) +1", "B) -1", "C) +7", "D) -2"], "ans": "B) -1"},
        {"q": "Which Halogen is used as a purple antiseptic?", "options": ["A) Chlorine", "B) Bromine", "C) Iodine", "D) Astatine"], "ans": "C) Iodine"}
    ]},
    4: {"name": "The Noble Gases (Group 18)", "data": [
        {"q": "Which Noble Gas is used in orange neon signs?", "options": ["A) Helium", "B) Neon", "C) Argon", "D) Xenon"], "ans": "B) Neon"},
        {"q": "What is the **Atomic Number of Argon (Ar)**?", "options": ["A) 10", "B) 18", "C) 36", "D) 54"], "ans": "B) 18"},
        {"q": "Why are Noble Gases unreactive?", "options": ["A) They are gases", "B) They have 8 protons", "C) They have full outer shells", ") They are rare"], "ans": "C) They have full outer shells"},
        {"q": "Which Noble Gas is radioactive?", "options": ["A) Krypton", "B) Xenon", "C) Radon", "D) Helium"], "ans": "C) Radon"},
        {"q": "Which is the most abundant Noble Gas in air?", "options": ["A) Helium", "B) Neon", "C) Argon", "D) Radon"], "ans": "C) Argon"}
    ]}
}

# --- Session State Management ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'mode' not in st.session_state: st.session_state.mode = "quiz" # modes: quiz, level_up, end

# --- UI Header ---
st.title("🛡️ Periodic Table: The Scientific Quest")
st.progress(min((st.session_state.level - 1) / len(levels_data), 1.0))

# --- SCREEN 1: THE QUIZ ---
if st.session_state.mode == "quiz":
    curr_level_info = levels_data[st.session_state.level]
    questions = curr_level_info["data"]
    q_data = questions[st.session_state.q_idx]

    st.subheader(f"📍 {curr_level_info['name']} (Level {st.session_state.level})")
    st.markdown(f"**Question {st.session_state.q_idx + 1} of 5:**")
    st.info(q_data["q"])
    
    user_choice = st.radio("Select your answer:", q_data["options"], index=None)

    if st.button("Submit Answer"):
        if user_choice == q_data["ans"]:
            st.success("✅ Correct!")
            st.session_state.score += 20
        else:
            st.error(f"❌ Wrong! The correct answer was {q_data['ans']}")
        
        # Advance logic
        if st.session_state.q_idx < 4:
            st.session_state.q_idx += 1
            st.rerun()
        else:
            # Check if there are more levels
            if st.session_state.level < len(levels_data):
                st.session_state.mode = "level_up"
            else:
                st.session_state.mode = "end"
            st.rerun()

# --- SCREEN 2: LEVEL CONGRATULATIONS ---
elif st.session_state.mode == "level_up":
    st.balloons()
    st.header(f"🎉 Level {st.session_state.level} Complete!")
    st.write(f"Excellent work! You have mastered the **{levels_data[st.session_state.level]['name']}**.")
    st.write(f"Current Score: **{st.session_state.score}**")
    
    if st.button("🚀 Start Level " + str(st.session_state.level + 1)):
        st.session_state.level += 1
        st.session_state.q_idx = 0
        st.session_state.mode = "quiz"
        st.rerun()

# --- SCREEN 3: FINAL RESULTS ---
elif st.session_state.mode == "end":
    st.header("🏆 MASTER CHEMIST CERTIFIED!")
    st.metric("Final Scientific Score", f"{st.session_state.score} / 400")
    if st.button("Reset Experiment"):
        st.session_state.level = 1
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.mode = "quiz"
        st.rerun()
        
