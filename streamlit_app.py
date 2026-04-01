import streamlit as st
import time

# 1. Setup & Styling
st.set_page_config(page_title="Periodic Master: Level Quest", layout="centered")

st.markdown("""
<style>
    .stButton>button {
        height: 60px; font-size: 18px !important; font-weight: 700 !important;
        border-radius: 12px !important; border: 2px solid #82c91e !important;
        background-color: white; color: #333; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #f1f3f5; border-color: #2b8a3e !important; }
    .level-header { text-align: center; color: #2b8a3e; margin-bottom: 20px; }
    .stat-box { text-align: center; background: #f8f9fa; padding: 10px; border-radius: 10px; border: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

# 2. Data Organization (Level by Level)
LEVELS = {
    1: [("H", "Hydrogen"), ("He", "Helium"), ("Li", "Lithium"), ("Be", "Beryllium"), ("B", "Boron")],
    2: [("C", "Carbon"), ("N", "Nitrogen"), ("O", "Oxygen"), ("F", "Fluorine"), ("Ne", "Neon")],
    3: [("Na", "Sodium"), ("Mg", "Magnesium"), ("Al", "Aluminium"), ("Si", "Silicon"), ("P", "Phosphorus")],
    4: [("S", "Sulphur"), ("Cl", "Chlorine"), ("Ar", "Argon"), ("K", "Potassium"), ("Ca", "Calcium")]
}

# 3. Initialize Session State
if 'current_level' not in st.session_state: st.session_state.current_level = 1
if 'matches' not in st.session_state: st.session_state.matches = []
if 'selected_sym' not in st.session_state: st.session_state.selected_sym = None
if 'score' not in st.session_state: st.session_state.score = 0

# 4. Game Header
st.markdown(f"<h1 class='level-header'>🔬 Level {st.session_state.current_level}: The Atomic Quest</h1>", unsafe_allow_html=True)

# Progress Bar
progress = len(st.session_state.matches) / 5
st.progress(progress)

# --- GAME INTERFACE ---
current_data = LEVELS[st.session_state.current_level]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Symbols")
    for sym, name in current_data:
        is_done = sym in st.session_state.matches
        btn_label = f"✨ {sym}" if is_done else sym
        if st.button(btn_label, key=f"s_{sym}", disabled=is_done, use_container_width=True):
            st.session_state.selected_sym = sym
            st.toast(f"Selected {sym}. Now find its name!", icon="🧪")

with col2:
    st.markdown("### Names")
    # Shuffling names for the UI only
    names_only = sorted(current_data, key=lambda x: x[1])
    for sym, name in names_only:
        is_done = sym in st.session_state.matches
        btn_label = f"✅ {name}" if is_done else name
        if st.button(btn_label, key=f"n_{name}", disabled=is_done, use_container_width=True):
            if st.session_state.selected_sym == sym:
                st.session_state.matches.append(sym)
                st.session_state.score += 20
                st.session_state.selected_sym = None
                st.success(f"Correct! {sym} is {name}")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Incorrect Match!")

# --- LEVEL TRANSITION ---
if len(st.session_state.matches) == 5:
    st.balloons()
    if st.session_state.current_level < 4:
        if st.button("🚀 UNLOCK NEXT LEVEL", use_container_width=True):
            st.session_state.current_level += 1
            st.session_state.matches = []
            st.session_state.selected_sym = None
            st.rerun()
    else:
        st.success("🏆 YOU ARE A PERIODIC MASTER!")
        if st.button("♻️ Reset Laboratory"):
            st.session_state.current_level = 1
            st.session_state.matches = []
            st.session_state.score = 0
            st.rerun()

# 5. Footer Stats
st.write("---")
c1, c2 = st.columns(2)
with c1: st.markdown(f"<div class='stat-box'><b>Total Score:</b> {st.session_state.score}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-box'><b>MSc Project:</b> Favour</div>", unsafe_allow_html=True)
