import streamlit as st
import time

# 1. UI STYLING (The "Educaplay" Skin)
st.markdown("""
<style>
    /* White Canvas */
    .stApp { background-color: #ffffff; color: #333; }
    
    /* Header Word List (At the Top) */
    .word-header {
        display: flex; flex-wrap: wrap; gap: 15px; justify-content: center;
        background: #ffffff; padding: 20px; border-bottom: 2px solid #f1f3f5;
        margin-bottom: 20px; font-family: sans-serif;
    }
    .word-card { font-weight: 700; font-size: 14px; letter-spacing: 1px; color: #444; }
    .word-card.found { text-decoration: line-through; color: #adb5bd; }

    /* The Grid Layout */
    .grid-wrap {
        display: grid; grid-template-columns: repeat(10, 45px); gap: 5px;
        justify-content: center; margin-top: 20px;
    }
    .char-cell {
        width: 45px; height: 45px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; font-weight: 800; color: #212529;
        border-radius: 4px; transition: 0.2s;
    }
    
    /* Highlights (Pill Shapes from your screenshot) */
    .pill-red { background-color: #ffc9c9; color: #c92a2a; border-radius: 25px; }
    .pill-blue { background-color: #a5d8ff; color: #1971c2; border-radius: 25px; }
    .pill-green { background-color: #b2f2bb; color: #2b8a3e; border-radius: 25px; }

    /* Bottom Timer & Score Bar */
    .footer-bar {
        display: flex; justify-content: space-around; align-items: center;
        width: 300px; margin: 30px auto; padding: 10px;
        border: 2.5px solid #82c91e; border-radius: 35px;
        font-family: monospace; font-size: 20px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 2. DATA (First 20 Elements)
ELEMENTS = [
    "HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", 
    "OXYGEN", "FLUORINE", "NEON", "SODIUM", "MAGNESIUM", "ALUMINIUM", "SILICON", 
    "PHOSPHORUS", "SULPHUR", "CHLORINE", "ARGON", "POTASSIUM", "CALCIUM"
]

# Static Grid based on your Screenshot
RAW_DATA = [
    ["B", "O", "X", "Y", "G", "E", "N", "N", "N", "N"],
    ["L", "E", "A", "P", "T", "U", "E", "C", "I", "I"],
    ["O", "S", "R", "B", "Z", "G", "I", "A", "T", "T"],
    ["Z", "H", "W", "Y", "O", "J", "W", "R", "R", "R"],
    ["U", "R", "E", "R", "L", "R", "I", "B", "O", "O"],
    ["E", "B", "D", "L", "A", "L", "O", "O", "G", "G"],
    ["I", "Y", "M", "U", "I", "I", "I", "N", "E", "E"],
    ["H", "B", "R", "U", "D", "U", "H", "U", "N", "N"],
    ["L", "I", "T", "H", "I", "U", "M", "L", "M", "M"],
    ["C", "A", "L", "C", "I", "U", "M", "X", "Y", "Z"]
]

if 'found' not in st.session_state: st.session_state.found = []
if 'start' not in st.session_state: st.session_state.start = time.time()
if 'score' not in st.session_state: st.session_state.score = 0

# --- HEADER: WORD LIST ---
st.markdown('<div class="word-header">', unsafe_allow_html=True)
for word in ELEMENTS:
    cls = "word-card found" if word in st.session_state.found else "word-card"
    st.markdown(f'<span class="{cls}">{word}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- THE GRID ---
st.markdown('<div class="grid-wrap">', unsafe_allow_html=True)
for r in range(10):
    for c in range(10):
        char = RAW_DATA[r][c]
        highlight = ""
        # Simulate the colored "Pills" from your screenshot
        if r == 0 and c in range(1, 7): highlight = "pill-red"    # OXYGEN
        if r == 8 and c in range(0, 7): highlight = "pill-blue"   # LITHIUM
        if c == 9 and r in range(0, 9): highlight = "pill-green"  # NITROGEN
        st.markdown(f'<div class="char-cell {highlight}">{char}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER: TIMER & SCORE ---
elapsed = int(time.time() - st.session_state.start)
mins, secs = divmod(elapsed, 60)
st.markdown(f'<div class="footer-bar">⏱️ {mins:02d}:{secs:02d} 🧩+</div>', unsafe_allow_html=True)

# --- INPUT ---
val = st.text_input("Found an element?", placeholder="Type here...").upper().strip()
if st.button("Check"):
    if val in ELEMENTS and val not in st.session_state.found:
        st.session_state.found.append(val)
        st.session_state.score += 4167 # Matching your screenshot's math
        st.rerun()

if len(st.session_state.found) == 20:
    st.balloons()
    st.success("Master Chemist! All 20 Elements Found.")
        
