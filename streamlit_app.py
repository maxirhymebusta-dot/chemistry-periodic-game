import streamlit as st
import random

# 1. High-End Game Aesthetics
st.set_page_config(page_title="Atomic Column", layout="centered")

st.markdown("""
<style>
    /* Professional Dark Lab Theme */
    .stApp {
        background: radial-gradient(circle, #1a2a6c, #b21f1f, #fdbb2d);
        background-attachment: fixed;
        color: white;
    }
    
    /* Vertical Column Container */
    .vertical-tube {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        padding: 30px 10px;
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px; /* Makes it look like a test tube */
        backdrop-filter: blur(15px);
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
        width: 100px;
        margin: 0 auto;
    }

    /* 3D Scrabble Tile Styling */
    .stButton>button {
        width: 65px !important;
        height: 65px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #1a2a6c !important;
        background: #fdfdfd !important;
        border: none !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 0 #bdc3c7, 0 12px 20px rgba(0,0,0,0.4) !important;
        transition: all 0.1s ease;
    }

    .stButton>button:active {
        transform: translateY(6px) !important;
        box-shadow: 0 2px 0 #bdc3c7 !important;
    }

    /* Labels and Headers */
    .game-text {
        text-align: center;
        font-family: 'Trebuchet MS', sans-serif;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
    }
</style>
""", unsafe_allow_html=True)

# 2. Level Data (First 20 Elements)
ELEMENTS = [
    "NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", 
    "SILICON", "LITHIUM", "SULPHUR", "CHLORINE", "FLUORINE", 
    "ALUMINIUM", "MAGNESIUM", "POTASSIUM", "CALCIUM"
]

# 3. Game State Logic
if 'lvl' not in st.session_state: st.session_state.lvl = 0
if 'ans_stack' not in st.session_state: st.session_state.ans_stack = []
if 'pool_grid' not in st.session_state:
    target = ELEMENTS[st.session_state.lvl]
    p = list(target)
    random.shuffle(p)
    st.session_state.pool_grid = p

target_word = ELEMENTS[st.session_state.lvl]

# 4. Header UI
st.markdown("<h1 class='game-text'>⚗️ ATOMIC COLUMN</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 class='game-text'>Level {st.session_state.lvl + 1}: Unstack {target_word[0]}...</h3>", unsafe_allow_html=True)

# 5. THE VERTICAL COLUMN (Answer Area)
st.write(" ")
c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    st.markdown("<div class='vertical-tube'>", unsafe_allow_html=True)
    for i in range(len(target_word)):
        # Display letters already picked or a placeholder
        char = st.session_state.ans_stack[i] if i < len(st.session_state.ans_stack) else "?"
        if st.button(char, key=f"v_{i}_{char}"):
            if i < len(st.session_state.ans_stack):
                # Return letter to pool
                removed = st.session_state.ans_stack.pop(i)
                st.session_state.pool_grid.append(removed)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 6. THE LETTER POOL (Horizontal Grid at Bottom)
st.write("---")
st.markdown("<p style='text-align:center; font-weight:bold; letter-spacing:2px;'>TAP TO FILL THE COLUMN</p>", unsafe_allow_html=True)
pool_cols = st.columns(6)
for i, char in enumerate(st.session_state.pool_grid):
    with pool_cols[i % 6]:
        if st.button(char, key=f"p_{i}_{char}"):
            val = st.session_state.pool_grid.pop(i)
            st.session_state.ans_stack.append(val)
            st.rerun()

# 7. WIN LOGIC
if "".join(st.session_state.ans_stack) == target_word:
    st.balloons()
    st.success(f"🧪 COLUMN STABILIZED: {target_word}")
    if st.button("NEXT LEVEL ➡️", use_container_width=True):
        st.session_state.lvl += 1
        # Refresh for next element
        next_w = ELEMENTS[st.session_state.lvl]
        p = list(next_w)
        random.shuffle(p)
        st.session_state.pool_grid = p
        st.session_state.ans_stack = []
        st.rerun()

# 8. Reset Button
if st.button("Empty Column ♻️", use_container_width=True):
    st.session_state.ans_stack = []
    p = list(target_word)
    random.shuffle(p)
    st.session_state.pool_grid = p
    st.rerun()

st.markdown("<br><p style='text-align: center; color: white; opacity: 0.7;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
