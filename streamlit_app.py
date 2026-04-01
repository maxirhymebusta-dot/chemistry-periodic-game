import streamlit as st
import random

# 1. Premium Game Aesthetics
st.set_page_config(page_title="Atomic Row", layout="centered")

st.markdown("""
<style>
    /* Dark Sci-Fi Laboratory Background */
    .stApp {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
        background-attachment: fixed;
        color: white;
    }
    
    /* 3D Scrabble-Style Tiles */
    .stButton>button {
        width: 50px !important;
        height: 50px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        color: #2c3e50 !important;
        background: #fdfdfd !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 0 #bdc3c7, 0 8px 15px rgba(0,0,0,0.4) !important;
        transition: all 0.1s ease;
        margin-bottom: 10px;
    }

    .stButton>button:active {
        transform: translateY(3px) !important;
        box-shadow: 0 2px 0 #bdc3c7 !important;
    }

    .game-title {
        text-align: center;
        color: white;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        font-family: 'Arial Black', sans-serif;
    }
    
    .section-label {
        font-weight: bold;
        letter-spacing: 1.5px;
        color: #f1f3f5;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Level Data (First 20 Elements)
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM"]

# 3. State Management
if 'lvl' not in st.session_state: st.session_state.lvl = 0
if 'ans_row' not in st.session_state: st.session_state.ans_row = []
if 'pool_row' not in st.session_state:
    target = ELEMENTS[st.session_state.lvl]
    p = list(target)
    random.shuffle(p)
    st.session_state.pool_row = p

target_word = ELEMENTS[st.session_state.lvl]

# 4. Header UI
st.markdown("<h1 class='game-title'>🧪 ATOMIC ROW</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Level {st.session_state.lvl + 1}: Unscramble the Element</p>", unsafe_allow_html=True)

# 5. YOUR WORD (ROW 1: ⬜⬜⬜⬜)
st.markdown("<p class='section-label'>YOUR WORD</p>", unsafe_allow_html=True)
# We create exactly enough columns for the word length to keep it horizontal
ans_cols = st.columns(max(len(target_word), 1))

for i in range(len(target_word)):
    with ans_cols[i]:
        char = st.session_state.ans_row[i] if i < len(st.session_state.ans_row) else "?"
        if st.button(char, key=f"ans_{i}_{char}"):
            if i < len(st.session_state.ans_row):
                removed = st.session_state.ans_row.pop(i)
                st.session_state.pool_row.append(removed)
                st.rerun()

st.write(" ") # Spacer

# 6. LETTER POOL (ROW 2: ⬜⬜⬜⬜)
st.markdown("<p class='section-label'>LETTER POOL</p>", unsafe_allow_html=True)
pool_cols = st.columns(max(len(st.session_state.pool_row) + len(st.session_state.ans_row), 1))

for i, char in enumerate(st.session_state.pool_row):
    with pool_cols[i]:
        if st.button(char, key=f"pool_{i}_{char}"):
            val = st.session_state.pool_row.pop(i)
            st.session_state.ans_row.append(val)
            st.rerun()

# 7. WIN LOGIC
if "".join(st.session_state.ans_row) == target_word:
    st.balloons()
    st.success(f"STABILIZED: {target_word}")
    if st.button("NEXT LEVEL 🚀", use_container_width=True):
        st.session_state.lvl += 1
        st.session_state.ans_row = []
        if st.session_state.lvl < len(ELEMENTS):
            next_w = ELEMENTS[st.session_state.lvl]
            p = list(next_w)
            random.shuffle(p)
            st.session_state.pool_row = p
            st.rerun()

# 8. Reset Option
if st.button("Reset Level ♻️", use_container_width=True):
    st.session_state.ans_row = []
    p = list(target_word)
    random.shuffle(p)
    st.session_state.pool_row = p
    st.rerun()

st.markdown("<br><p style='text-align: center; color: white; opacity: 0.6;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
