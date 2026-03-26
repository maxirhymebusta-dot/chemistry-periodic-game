import streamlit as st
import random

# Page Configuration
st.set_page_config(page_title="Periodic Table Master", layout="centered")

# Chemistry Data (Sample set for Secondary Schools)
elements = [
    {"name": "Hydrogen", "symbol": "H", "number": 1, "group": "Non-metals", "clue": "I am the lightest element in the universe."},
    {"name": "Helium", "symbol": "He", "number": 2, "group": "Noble Gases", "clue": "I am used to make balloons float and I never react with others."},
    {"name": "Lithium", "symbol": "Li", "number": 3, "group": "Alkali Metals", "clue": "I am a light metal used in phone batteries."},
    {"name": "Oxygen", "symbol": "O", "number": 8, "group": "Non-metals", "clue": "You need me to breathe and for fire to burn."},
    {"name": "Sodium", "symbol": "Na", "number": 11, "group": "Alkali Metals", "clue": "I react violently with water. I am half of common table salt."},
    {"name": "Chlorine", "symbol": "Cl", "number": 17, "group": "Halogens", "clue": "I am a yellow-green gas used to keep swimming pools clean."},
    {"name": "Iron", "symbol": "Fe", "number": 26, "group": "Transition Metals", "clue": "I am used to make steel and I am found in your blood."},
]

st.title("🧪 The Element Hunter")
st.subheader("MSc Project: Secondary Chemistry Edition")

# Initialize Game Session
if 'current_q' not in st.session_state:
    st.session_state.current_q = random.choice(elements)
    st.session_state.score = 0

# Game Interface
st.info(f"**YOUR CLUE:** {st.session_state.current_q['clue']}")

# Student Input
answer = st.text_input("Which element am I? (Enter Name or Symbol)").strip()

if st.button("Submit Answer"):
    target = st.session_state.current_q
    if answer.lower() == target['name'].lower() or answer.upper() == target['symbol']:
        st.success(f"Correct! That was {target['name']} ({target['symbol']}). It belongs to the {target['group']} group.")
        st.session_state.score += 10
        # Pick a new element for the next round
        st.session_state.current_q = random.choice(elements)
        st.rerun()
    else:
        st.error("Not quite! Look at the clue again.")

# Progress
st.sidebar.metric("Your Score", st.session_state.score)
st.sidebar.write("---")
st.sidebar.write("Developed for Postgraduate Curriculum Study")
