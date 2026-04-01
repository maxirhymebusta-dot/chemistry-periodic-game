import streamlit as st
import random

# 1. Premium Visual Upgrade
st.set_page_config(page_title="Atomic Column", layout="centered")

st.markdown("""
<style>
    /* Darker, richer gradient so white text pops */
    .stApp {
        background: radial-gradient(circle at center, #2c3e50, #000000);
        color: white;
    }
    
    /* Centered Glass Test Tube */
    .vertical-tube {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        padding: 25px 15px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 40px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 25px rgba(130, 201, 30, 0.2);
        width: 100px;
        margin: 20px auto;
    }

    /* Polished 3D Tiles */
    .stButton>button {
        width: 60px !important;
        height: 60px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        color: #1a2a6c !important;
        background: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 0 #bdc3c7, 0 10px 15px rgba(0,0,0,0.5) !important;
        transition: all 0.1s ease;
    }

    .stButton>button:active {
        transform: translateY(4px) !important;
        box-shadow: 0 2px 0 #bdc3c7 !important;
    }

    .game-text {
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
</style>
""", unsafe_allow_html=True)

# 2. Level Data
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM"]

# 3. Game Logic
if 'lvl' not in st.session_state: st.session_state.lvl = 0
if 'ans_stack' not in st.session_state: st.session_state.ans_stack = []
if 'pool_grid' not in st.session_state:
    target = ELEMENTS[st.session_state.lvl]
    p = list(target)
    random.shuffle(p)
    st.session_state.pool_grid = p

target_word = ELEMENTS[st.session_state.lvl]

# 4. UI Header
st.markdown("<h1 class='game-text'>🧪 ATOMIC COLUMN</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 class='game-text' style='color:#82c91e;'>Level {st.session_state.lvl + 1}</h3>", unsafe_allow_html=True)

# 5. THE CENTERED COLUMN
st.markdown("<div class='vertical-tube'>", unsafe_allow_html=True)
for i in range(len(target_word)):
    char = st.session_state.ans_stack[i] if i < len(st.session_state.ans_stack) else "?"
    if st.button(char, key=f"v_{i}_{char}"):
        if i < len(st.session_state.ans_stack):
            removed = st.session_state.ans_stack.pop(i)
            st.session_state.pool_grid.append(removed)
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# 6. THE LETTER POOL (Bottom Grid)
st.write("---")
st.markdown("<p style='text-align:center; font-weight:bold; color:#aaa;'>SELECT LETTERS BELOW</p>", unsafe_allow_html=True)
pool_cols = st.columns(5)
for i, char in enumerate(st.session_state.pool_grid):
    with pool_cols[i % 5]:
        if st.button(char, key=f"p_{i}_{char}"):
            val = st.session_state.pool_grid.pop(i)
            st.session_state.ans_stack.append(val)
            st.rerun()

# 7. WIN LOGIC
if "".join(st.session_state.ans_stack) == target_word:
    st.balloons()
    st.success(f"STABILIZED: {target_word}")
    if st.button("NEXT LEVEL ➡️", use_container_width=True):
        st.session_state.lvl += 1
        st.session_state.ans_stack = []
        next_w = ELEMENTS[st.session_state.lvl]
        p = list(next_w)
        random.shuffle(p)
        st.session_state.pool_grid = p
        st.rerun()

# 8. Reset
if st.button("Empty Column ♻️", use_container_width=True):
    st.session_state.ans_stack = []
    p = list(target_word)
    random.shuffle(p)
    st.session_state.pool_grid = p
    st.rerun()

st.markdown("<br><p style='text-align: center; color: #555;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
