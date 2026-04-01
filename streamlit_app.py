import streamlit as st
import random

# 1. Advanced Game Aesthetics
st.set_page_config(page_title="Atomic Stack", layout="centered")

st.markdown("""
<style>
    /* Gradient Background for the whole app */
    .stApp {
        background: linear-gradient(180deg, #1a2a6c 0%, #b21f1f 50%, #fdbb2d 100%);
        color: white;
    }
    
    /* Vertical Slot Container */
    .vertical-stack {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        min-height: 400px;
        width: 120px;
        margin: 0 auto;
    }

    /* Scrabble Tile Styling */
    .stButton>button {
        width: 60px !important;
        height: 60px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        color: #2d3436 !important;
        background: #f9f9f9 !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 0 #d1d1d1, 0 8px 15px rgba(0,0,0,0.3) !important;
        transition: all 0.1s ease;
    }

    .stButton>button:active {
        transform: translateY(4px) !important;
        box-shadow: 0 2px 0 #d1d1d1 !important;
    }

    /* Target Text */
    .game-status {
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# 2. Level Data (First 20 Elements)
ELEMENTS = [
    "NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", 
    "SILICON", "LITHIUM", "SULPHUR", "CHLORINE", "FLUORINE", 
    "ALUMINIUM", "MAGNESIUM", "POTASSIUM", "CALCIUM"
]

# 3. State Management
if 'level' not in st.session_state: st.session_state.level = 0
if 'ans_tiles' not in st.session_state: st.session_state.ans_tiles = []
if 'pool_tiles' not in st.session_state:
    target = ELEMENTS[st.session_state.level]
    pool = list(target)
    random.shuffle(pool)
    st.session_state.pool_tiles = pool

target_word = ELEMENTS[st.session_state.level]

# 4. Header UI
st.markdown("<h1 class='game-status'>🔬 ATOMIC STACK</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 class='game-status'>Level {st.session_state.level + 1}: Unstack the Element</h3>", unsafe_allow_html=True)

# 5. THE VERTICAL STACK (The Answer Area)
st.write(" ")
cols = st.columns([1, 1, 1]) # Center the vertical line

with cols[1]:
    st.markdown("<p style='text-align:center; font-weight:bold;'>Vertical Answer</p>", unsafe_allow_html=True)
    # This creates the vertical visual line
    for i in range(len(target_word)):
        char = st.session_state.ans_tiles[i] if i < len(st.session_state.ans_tiles) else "?"
        if st.button(char, key=f"ans_{i}_{char}"):
            if i < len(st.session_state.ans_tiles):
                val = st.session_state.ans_tiles.pop(i)
                st.session_state.pool_tiles.append(val)
                st.rerun()

# 6. THE LETTER POOL (Horizontal Grid at Bottom)
st.write("---")
st.markdown("<p style='text-align:center; font-weight:bold;'>Letter Pool (Tap to move to stack)</p>", unsafe_allow_html=True)
pool_cols = st.columns(6)
for i, char in enumerate(st.session_state.pool_tiles):
    with pool_cols[i % 6]:
        if st.button(char, key=f"pool_{i}_{char}"):
            val = st.session_state.pool_tiles.pop(i)
            st.session_state.ans_tiles.append(val)
            st.rerun()

# 7. WIN LOGIC
user_word = "".join(st.session_state.ans_tiles)
if user_word == target_word:
    st.balloons()
    st.success(f"🏆 STABILIZED! It is {target_word}")
    if st.button("NEXT LEVEL 🚀", use_container_width=True):
        st.session_state.level += 1
        if st.session_state.level < len(ELEMENTS):
            next_word = ELEMENTS[st.session_state.level]
            p = list(next_word)
            random.shuffle(p)
            st.session_state.pool_tiles = p
            st.session_state.ans_tiles = []
            st.rerun()
        else:
            st.write("Master Chemist Level Reached!")

# 8. Reset Option
if st.button("Reset Stack ♻️", use_container_width=True):
    st.session_state.ans_tiles = []
    p = list(target_word)
    random.shuffle(p)
    st.session_state.pool_tiles = p
    st.rerun()

st.markdown("<br><p style='text-align: center; color: white; font-size: 12px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
    
