import streamlit as st
import random
import time

# 1. Game Setup & Styling
st.set_page_config(page_title="Atomic Collector", layout="centered")

st.markdown("""
<style>
    .game-container {
        height: 400px; width: 100%; border: 3px solid #82c91e;
        position: relative; background-color: #111; overflow: hidden;
        border-radius: 15px; margin-bottom: 20px;
    }
    .element-bubble {
        position: absolute; width: 50px; height: 50px;
        background-color: #82c91e; color: white;
        border-radius: 50%; display: flex; align-items: center;
        justify-content: center; font-weight: bold; font-size: 20px;
        cursor: pointer; box-shadow: 0 0 10px #82c91e;
    }
    .target-box {
        text-align: center; padding: 20px; background: #f1f3f5;
        border-radius: 10px; font-size: 24px; font-weight: bold;
        color: #2b8a3e; border: 2px dashed #82c91e;
    }
</style>
""", unsafe_allow_html=True)

# 2. Data: First 20 Elements
ELEMENTS = [
    {"s": "H", "n": "Hydrogen"}, {"s": "He", "n": "Helium"}, {"s": "Li", "n": "Lithium"},
    {"s": "Be", "n": "Beryllium"}, {"s": "B", "n": "Boron"}, {"s": "C", "n": "Carbon"},
    {"s": "N", "n": "Nitrogen"}, {"s": "O", "n": "Oxygen"}, {"s": "F", "n": "Fluorine"},
    {"s": "Ne", "n": "Neon"}, {"s": "Na", "n": "Sodium"}, {"s": "Mg", "n": "Magnesium"}
]

# 3. Session State for Game Logic
if 'score' not in st.session_state: st.session_state.score = 0
if 'target' not in st.session_state: st.session_state.target = random.choice(ELEMENTS)
if 'lives' not in st.session_state: st.session_state.lives = 3

# 4. UI Header
st.title("🚀 Atomic Collector")
c1, c2 = st.columns(2)
with c1: st.subheader(f"🏆 Score: {st.session_state.score}")
with c2: st.subheader(f"❤️ Lives: {st.session_state.lives}")

# 5. THE TARGET AREA
st.markdown(f"<div class='target-box'>TARGET: CATCH {st.session_state.target['n'].upper()}</div>", unsafe_allow_html=True)
st.write(" ")

# 6. THE GAME GRID (Action Area)
# We show 4 random options. The student must click the correct symbol.
options = random.sample(ELEMENTS, 3)
if st.session_state.target not in options:
    options.append(st.session_state.target)
random.shuffle(options)

# Displaying as "Floating Bubbles" using columns
cols = st.columns(4)
for i, opt in enumerate(options):
    with cols[i]:
        if st.button(opt['s'], key=f"opt_{i}_{opt['s']}", use_container_width=True):
            if opt['s'] == st.session_state.target['s']:
                st.session_state.score += 50
                st.balloons()
                st.toast(f"Great Catch! {opt['s']} is {opt['n']}", icon="🧪")
                st.session_state.target = random.choice(ELEMENTS)
                st.rerun()
            else:
                st.session_state.lives -= 1
                st.error("Wrong Element!")
                if st.session_state.lives <= 0:
                    st.warning("REACTOR OVERLOAD! Game Over.")
                    time.sleep(2)
                    st.session_state.score = 0
                    st.session_state.lives = 3
                    st.rerun()

# 7. Progress through the shells
st.write("---")
st.markdown("<p style='text-align: center; color: grey;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
