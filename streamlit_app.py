import streamlit as st
import random
import time

# 1. Visual Styling
st.set_page_config(page_title="Element Reactor", layout="centered")
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .reactor-core {
        text-align: center; padding: 20px;
        background: #1e1e1e; border: 4px solid #82c91e;
        border-radius: 50%; width: 200px; height: 200px;
        margin: 0 auto; display: flex; align-items: center;
        justify-content: center; color: #82c91e;
        box-shadow: 0 0 20px #82c91e; font-size: 24px; font-weight: 800;
    }
    .stButton>button {
        height: 80px !important; font-size: 22px !important;
        border-radius: 15px !important; background-color: #262730 !important;
        color: white !important; border: 2px solid #444 !important;
    }
    .stButton>button:hover { border-color: #82c91e !important; color: #82c91e !important; }
</style>
""", unsafe_allow_html=True)

# 2. Data: The First 20 Elements
ELEMENTS = [
    {"s": "H", "n": "Hydrogen"}, {"s": "He", "n": "Helium"}, {"s": "Li", "n": "Lithium"},
    {"s": "Be", "n": "Beryllium"}, {"s": "B", "n": "Boron"}, {"s": "C", "n": "Carbon"},
    {"s": "N", "n": "Nitrogen"}, {"s": "O", "n": "Oxygen"}, {"s": "F", "n": "Fluorine"},
    {"s": "Ne", "n": "Neon"}, {"s": "Na", "n": "Sodium"}, {"s": "Mg", "n": "Magnesium"},
    {"s": "Al", "n": "Aluminium"}, {"s": "Si", "n": "Silicon"}, {"s": "P", "n": "Phosphorus"},
    {"s": "S", "n": "Sulphur"}, {"s": "Cl", "n": "Chlorine"}, {"s": "Ar", "n": "Argon"},
    {"s": "K", "n": "Potassium"}, {"s": "Ca", "n": "Calcium"}
]

# 3. Game State
if 'score' not in st.session_state: st.session_state.score = 0
if 'target' not in st.session_state: st.session_state.target = random.choice(ELEMENTS)
if 'level' not in st.session_state: st.session_state.level = 1

# 4. Interface
st.markdown(f"<p style='text-align:right; color:#82c91e;'>Score: {st.session_state.score}</p>", unsafe_allow_html=True)

# The Reactor Core (Shows the target name)
st.markdown(f"<div class='reactor-core'>{st.session_state.target['n'].upper()}</div>", unsafe_allow_html=True)
st.write("---")

# The Blaster Options (Symbols)
# Pick 4 random symbols, ensuring the correct one is included
options = random.sample(ELEMENTS, 3)
if st.session_state.target not in options:
    options[0] = st.session_state.target
random.shuffle(options)

st.write("### ⚡ BLAST THE CORRECT SYMBOL!")
col1, col2 = st.columns(2)

for i, opt in enumerate(options):
    with col1 if i < 2 else col2:
        if st.button(opt['s'], key=f"btn_{opt['s']}", use_container_width=True):
            if opt['s'] == st.session_state.target['s']:
                st.session_state.score += 100
                st.toast("🎯 DIRECT HIT!", icon="🚀")
                st.session_state.target = random.choice(ELEMENTS)
                st.rerun()
            else:
                st.error("MISSED! -50 Energy")
                st.session_state.score -= 50
                st.rerun()

# 5. Footer
st.markdown("<br><p style='text-align: center; color: #555;'>MSc Project: Periodic Master | Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
