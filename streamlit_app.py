import streamlit as st
import random

# 1. Premium Game Aesthetics
st.set_page_config(page_title="Atomic Scramble", layout="centered")

st.markdown("""
<style>
    /* Dark Sci-Fi Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* The Horizontal Slot Row */
    .word-row {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin: 20px 0;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 3D Scrabble-Style Tiles */
    .stButton>button {
        width: 50px !important;
        height: 50px !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        color: #1a2a6c !important;
        background: #fdfdfd !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 0 #bdc3c7, 0 8px 15px rgba(0,0,0,0.4) !important;
        transition: all 0.1s ease;
    }

    .stButton>button:active {
        transform: translateY(3px) !important;
        box-shadow: 0 2px 0 #bdc3c7 !important;
    }

    .game-title {
        text-align: center;
        color: #82c91e;
        text-shadow: 0 0 10px rgba(130, 201, 30, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# 2. Elements Data
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM"]

# 3. Game Logic Setup
if 'lvl' not in st.session_state: st.session_state.lvl = 0
if 'ans_row' not in st.session_state: st.session_state.ans_row = []
if 'pool_grid' not in st.session_state:
    target = ELEMENTS[st.session_state.lvl]
    p = list(target)
    random.shuffle(p)
    st.session_state.pool_grid = p

target_word = ELEMENTS[st.session_state.lvl]

# 4. Header
st.markdown("<h1 class='game-title'>🧪 ATOMIC SCRAMBLE</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'><b>Level {st.session_state.lvl + 1}: Arrange the letters</b></p>", unsafe_allow_html=True)

# 5. THE HORIZONTAL ANSWER ROW (⬜⬜⬜⬜)
st.write("### Your Word")
ans_cols = st.columns(len(target_word) if len(target_word) > 0 else 1)
for i in range(len(target_word)):
    with ans_cols[i]:
        char = st.session_state.ans_row[i] if i < len(st.session_state.ans_row) else " "
        if st.button(char, key=f"ans_{i}_{char}"):
            if i < len(st.session_state.ans_row):
                val = st.session_state.ans_row.pop(i)
                st.session_state.pool_grid.append(val)
                st.rerun()

st.write("---")

# 6. THE LETTER POOL GRID (⬜⬜⬜⬜)
st.write("### Letter Pool")
pool_cols = st.columns(5)
for i, char in enumerate(st.session_state.pool_grid):
    with pool_cols[i % 5]:
        if st.button(char, key=f"p_{i}_{char}"):
            val = st.session_state.pool_grid.pop(i)
            st.session_state.ans_row.append(val)
            st.rerun()

# 7. WIN LOGIC
if "".join(st.session_state.ans_row) == target_word:
    st.balloons()
    st.success(f"STABILIZED: {target_word}")
    if st.button("PROCEED TO NEXT LEVEL 🚀", use_container_width=True):
        st.session_state.lvl += 1
        st.session_state.ans_row = []
        next_w = ELEMENTS[st.session_state.lvl]
        p = list(next_w)
        random.shuffle(p)
        st.session_state.pool_grid = p
        st.rerun()

# 8. Reset Option
if st.button("Reset Level ♻️", use_container_width=True):
    st.session_state.ans_row = []
    p = list(target_word)
    random.shuffle(p)
    st.session_state.pool_grid = p
    st.rerun()

st.markdown("<br><p style='text-align: center; color: #777;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
        
