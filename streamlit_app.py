import streamlit as st
import random

# 1. Page Config
st.set_page_config(page_title="MSc Chemistry Master", page_icon="🧪", layout="wide")

# 2. Advanced Curriculum Data (Scientific Properties)
# We use A, B, C, D options for every question
levels_data = {
    1: {"name": "Period 1 & 2 Essentials", "data": [
        {"q": "Which element has an **Atomic Number of 6** and is the basis of organic chemistry?", "options": ["A) Nitrogen", "B) Carbon", "C) Oxygen", "D) Boron"], "ans": "B) Carbon"},
        {"q": "What is the **Molar Mass** of Oxygen (O) to the nearest whole number?", "options": ["A) 8 g/mol", "B) 12 g/mol", "C) 16 g/mol", "D) 32 g/mol"], "ans": "C) 16 g/mol"},
        {"q": "Identify the element with the electron configuration **1s² 2s¹**.", "options": ["A) Helium", "B) Lithium", "C) Beryllium", "D) Sodium"], "ans": "B) Lithium"},
        {"q": "Which element is a Noble Gas found in Period 1?", "options": ["A) Neon", "B) Argon", "C) Hydrogen", "D) Helium"], "ans": "D) Helium"},
        {"q": "Atomic Number 7 belongs to which element?", "options": ["A) Nitrogen", "B) Fluorine", "C) Neon", "D) Carbon"], "ans": "A) Nitrogen"}
    ]},
    2: {"name": "Group 1 & 2 (Reactive Metals)", "data": [
        {"q": "Which Alkali Metal has a **Molar Mass of approx. 23 g/mol**?", "options": ["A) Lithium", "B) Potassium", "C) Sodium", "D) Magnesium"], "ans": "C) Sodium"},
        {"q": "What is the **Atomic Number of Calcium (Ca)**?", "options": ["A) 12", "B) 20", "C) 19", "D) 30"], "ans": "B) 20"},
        {"q": "Which element in Group 2 is known for burning with a bright white flame?", "options": ["A) Beryllium", "B) Calcium", "C) Magnesium", "D) Barium"], "ans": "C) Magnesium"},
        {"q": "Identify the element: Group 1, Period 4.", "options": ["A) Sodium", "B) Potassium", "C) Rubidium", "D) Cesium"], "ans": "B) Potassium"},
        {"q": "What is the valency of elements in Group 2?", "options": ["A) +1", "B) +2", "C) -2", "D) 0"], "ans": "B) +2"}
    ]}
    # You can add Level 3, 4, etc. following this same format
}

# --- Session State Management ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'completed' not in st.session_state: st.session_state.completed = False

# --- UI Header ---
st.title("🛡️ Periodic Table: The Scientific Quest")
st.progress(min(st.session_state.level / len(levels_data), 1.0))

# --- Game Logic ---
if not st.session_state.completed:
    curr_level_info = levels_data[st.session_state.level]
    questions = curr_level_info["data"]
    
    st.subheader(f"📍 {curr_level_info['name']} (Level {st.session_state.level})")
    
    # Display the specific question
    q_data = questions[st.session_state.q_idx]
    st.markdown(f"**Question {st.session_state.q_idx + 1} of 5:**")
    st.info(q_data["q"])
    
    # Multiple Choice Input
    user_choice = st.radio("Select the correct option:", q_data["options"], index=None)

    if st.button("Submit Answer"):
        if user_choice == q_data["ans"]:
            st.success("✅ Correct!")
            st.session_state.score += 20
        else:
            st.error(f"❌ Wrong! The correct answer was {q_data['ans']}")
        
        # Progression Logic
        if st.session_state.q_idx < 4:
            st.session_state.q_idx += 1
            st.rerun()
        else:
            # Finished a level
            if st.session_state.level < len(levels_data):
                st.balloons()
                st.write(f"## 🎉 Congratulations! Level {st.session_state.level} Complete.")
                if st.button("Start Next Level"):
                    st.session_state.level += 1
                    st.session_state.q_idx = 0
                    st.rerun()
            else:
                st.session_state.completed = True
                st.rerun()

else:
    st.header("🏆 MASTER CHEMIST CERTIFIED!")
    st.metric("Final Scientific Score", f"{st.session_state.score} Points")
    if st.button("Reset Experiment"):
        st.session_state.level = 1
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.completed = False
        st.rerun()
    
