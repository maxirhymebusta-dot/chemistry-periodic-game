import streamlit as st
import random

# 1. Page Config & Scramble Aesthetics
st.set_page_config(page_title="Atomic Scramble", layout="centered")

st.markdown("""
<style>
    /* The Scramble Tile Look */
    .stButton>button {
        width: 45px !important;
        height: 45px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #333 !important;
        background-color: #fdfae5 !important; /* Cream/Paper color like Scrabble */
        border: 2px solid #d4c18d !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 0 #bca76d !important;
        margin: 2px !important;
        transition: 0.1s;
    }
    .stButton>button:active {
        transform: translateY(3px) !important;
        box-shadow: 0 1px 0 #bca76d !important;
    }
    
    /* Empty Slot Look */
    .empty-slot {
        border: 2px dashed #cbd5e0;
        background-color: #f8f9fa;
        color: transparent;
    }
    
    .game-title { text-align: center; color: #2b8a3e; font-family: 'Arial Black', sans-serif; }
    .level-indicator { text-align: center; color: #666; font-weight: bold; margin-bottom: 20px; }
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

# 4. Header
st.markdown("<h1 class='game-title'>🧪 ATOMIC SCRAMBLE</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='level-indicator'>LEVEL {st.session_state.level + 1} / {len(ELEMENTS)}</p>", unsafe_allow_html=True)

# 5. THE ANSWER AREA (Row Format)
st.write("### Your Word")
ans_cols = st.columns(10)
for i in range(len(target_word)):
    with ans_cols[i]:
        char = st.session_state.ans_tiles[i] if i < len(st.session_state.ans_tiles) else ""
        if char == "":
            st.button(" ", key=f"empty_{i}", disabled=True)
        else:
            if st.button(char, key=f"ans_{i}_{char}"):
                # Remove from answer, put back in pool
                val = st.session_state.ans_tiles.pop(i)
                st.session_state.pool_tiles.append(val)
                st.rerun()

st.write("---")

# 6. THE LETTER POOL (Grid Format)
st.write("### Letter Pool (Tap to Move)")
# We create a 4x4 or 5x2 grid for the pool
pool_cols = st.columns(5)
for i, char in enumerate(st.session_state.pool_tiles):
    with pool_cols[i % 5]:
        if st.button(char, key=f"pool_{i}_{char}"):
            # Move from pool to answer
            val = st.session_state.pool_tiles.pop(i)
            st.session_state.ans_tiles.append(val)
            st.rerun()

# 7. WIN LOGIC
user_word = "".join(st.session_state.ans_tiles)
if user_word == target_word:
    st.balloons()
    st.success(f"🏆 Correct! It is {target_word}")
    if st.button("NEXT ELEMENT 🚀", use_container_width=True):
        st.session_state.level += 1
        # Reset tiles for next level
        next_word = ELEMENTS[st.session_state.level]
        p = list(next_word)
        random.shuffle(p)
        st.session_state.pool_tiles = p
        st.session_state.ans_tiles = []
        st.rerun()

# 8. Footer/Reset
st.write(" ")
if st.button("Reset Level ♻️"):
    st.session_state.ans_tiles = []
    p = list(target_word)
    random.shuffle(p)
    st.session_state.pool_tiles = p
    st.rerun()

st.markdown("<p style='text-align: center; color: grey; font-size: 10px; margin-top: 30px;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
