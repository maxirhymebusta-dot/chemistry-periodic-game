import streamlit as st
import random
import time

# 1. Page Config & Lab Theme
st.set_page_config(page_title="Periodic Master", layout="centered")

st.markdown("""
<style>
    .stButton>button {
        height: 55px; border-radius: 15px !important;
        border: 2px solid #82c91e !important; font-weight: bold !important;
        transition: 0.3s; background-color: #ffffff;
    }
    .stButton>button:active { background-color: #a5d8ff !important; }
    .lvl-text { text-align: center; color: #2b8a3e; font-family: sans-serif; }
    .score-card { background: #f1f3f5; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. Level Data (5 Elements per Level)
LEVELS = {
    1: {"name": "K-Shell", "data": [("H", 1), ("He", 2), ("Li", 3), ("Be", 4), ("B", 5)]},
    2: {"name": "L-Shell", "data": [("C", 6), ("N", 7), ("O", 8), ("F", 9), ("Ne", 10)]},
    3: {"name": "M-Shell", "data": [("Na", 11), ("Mg", 12), ("Al", 13), ("Si", 14), ("P", 15)]},
    4: {"name": "Valence Gate", "data": [("S", 16), ("Cl", 17), ("Ar", 18), ("K", 19), ("Ca", 20)]}
}

# 3. State Management
if 'lvl' not in st.session_state: st.session_state.lvl = 1
if 'found' not in st.session_state: st.session_state.found = []
if 'sel_sym' not in st.session_state: st.session_state.sel_sym = None
if 'score' not in st.session_state: st.session_state.score = 0

# 4. Header UI
st.markdown(f"<h1 class='lvl-text'>🔬 Level {st.session_state.lvl}: {LEVELS[st.session_state.lvl]['name']}</h1>", unsafe_allow_html=True)
st.progress(len(st.session_state.found) / 5)

# 5. The Grid (Symbols vs Atomic Numbers)
current_lvl = LEVELS[st.session_state.lvl]
col1, col2 = st.columns(2)

with col1:
    st.subheader("Symbols")
    for sym, num in current_lvl['data']:
        done = sym in st.session_state.found
        if st.button(f"✨ {sym}" if done else sym, key=f"s{sym}", disabled=done, use_container_width=True):
            st.session_state.sel_sym = sym

with col2:
    st.subheader("Atomic #")
    # Shuffle the numbers for the challenge
    nums_only = sorted(current_lvl['data'], key=lambda x: random.random())
    for sym, num in nums_only:
        done = sym in st.session_state.found
        if st.button(f"✅ {num}" if done else str(num), key=f"n{num}", disabled=done, use_container_width=True):
            if st.session_state.sel_sym == sym:
                st.session_state.found.append(sym)
                st.session_state.score += 20
                st.session_state.sel_sym = None
                st.success("Stable!")
                time.sleep(0.3)
                st.rerun()
            else:
                st.error("Unstable!")

# 6. Level Up Logic
if len(st.session_state.found) == 5:
    st.balloons()
    if st.session_state.lvl < 4:
        if st.button("🔓 UNLOCK NEXT SHELL", use_container_width=True):
            st.session_state.lvl += 1
            st.session_state.found = []
            st.rerun()
    else:
        st.success("🏆 PERIODIC MASTER ACHIEVED!")
        if st.button("Restart Laboratory"):
            st.session_state.clear()
            st.rerun()

st.write("---")
st.markdown(f"<div class='score-card'>Laboratory Score: {st.session_state.score}</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey; font-size: 10px; margin-top: 20px;'>MSc Project | Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
