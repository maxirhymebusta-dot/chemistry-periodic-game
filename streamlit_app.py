import streamlit as st
import time

# 1. THE GRID SYSTEM (Forced Square Layout)
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    
    /* Top Word Bank */
    .word-bank {
        display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
        background: #f1f3f5; padding: 15px; border-radius: 10px; margin-bottom: 20px;
    }
    .word-tag { font-size: 10px; font-weight: 700; color: #495057; text-transform: uppercase; }
    .word-tag.found { text-decoration: line-through; color: #ced4da; }

    /* THE GRID FIX: This forces the 10x10 shape */
    .grid-container {
        display: flex;
        flex-wrap: wrap;
        width: 320px; /* Fixed width to ensure 10 letters per row */
        margin: 0 auto;
        border: 2px solid #dee2e6;
        padding: 5px;
        background: white;
    }
    .letter-box {
        width: 30px; 
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 800;
        color: #212529;
        font-family: 'Arial', sans-serif;
    }

    /* Pill Highlights (Red/Blue/Green like your screenshot) */
    .p-red { background-color: #ffc9c9; border-radius: 50%; color: #c92a2a; }
    .p-blue { background-color: #a5d8ff; border-radius: 50%; color: #1971c2; }
    .p-green { background-color: #b2f2bb; border-radius: 50%; color: #2b8a3e; }

    /* Stats Bar at Bottom */
    .stats-bar {
        display: flex; justify-content: space-around; align-items: center;
        width: 280px; margin: 25px auto; padding: 8px;
        border: 2px solid #82c91e; border-radius: 30px;
        font-weight: bold; font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# 2. DATA: The First 20 Elements
ELEMENTS = [
    "HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", 
    "OXYGEN", "FLUORINE", "NEON", "SODIUM", "MAGNESIUM", "ALUMINIUM", "SILICON", 
    "PHOSPHORUS", "SULPHUR", "CHLORINE", "ARGON", "POTASSIUM", "CALCIUM"
]

# 10x10 Grid Data
RAW_GRID = [
    "B O X Y G E N N N N", 
    "L E A P T U E C I I", 
    "O S R B Z G I A T T", 
    "Z H W Y O J W R R R", 
    "U R E R L R I B O O", 
    "E B D L A L O O G G", 
    "I Y M U I I I N E E", 
    "H B R U D U H U N N", 
    "L I T H I U M L M M", 
    "C A L C I U M X Y Z"
]

if 'found_words' not in st.session_state: st.session_state.found_words = []
if 'start_t' not in st.session_state: st.session_state.start_t = time.time()

# --- TOP: WORD LIST ---
st.markdown('<div class="word-bank">', unsafe_allow_html=True)
for e in ELEMENTS:
    status = "found" if e in st.session_state.found_words else ""
    st.markdown(f'<span class="word-tag {status}">{e}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- MIDDLE: THE GRID (STRICT FORMAT) ---
st.markdown('<div class="grid-container">', unsafe_allow_html=True)
for r_idx, row_str in enumerate(RAW_GRID):
    letters = row_str.split()
    for c_idx, char in enumerate(letters):
        # Apply the pill colors based on your screenshot
        h = ""
        if r_idx == 0 and c_idx in range(1,7): h = "p-red"   # OXYGEN
        if r_idx == 8 and c_idx in range(0,7): h = "p-blue"  # LITHIUM
        if c_idx == 9 and r_idx in range(0,9): h = "p-green" # NITROGEN
        
        st.markdown(f'<div class="letter-box {h}">{char}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- BOTTOM: TIMER BAR ---
elapsed = int(time.time() - st.session_state.start_t)
m, s = divmod(elapsed, 60)
st.markdown(f'<div class="stats-bar">⏱️ {m:02d}:{s:02d} 🧩+</div>', unsafe_allow_html=True)

# --- INPUT ---
st.write("---")
guess = st.text_input("Found an element?", placeholder="Type name here...").upper().strip()
if st.button("Verify Element"):
    if guess in ELEMENTS and guess not in st.session_state.found_words:
        st.session_state.found_words.append(guess)
        st.rerun()

if len(st.session_state.found_words) == 20:
    st.balloons()
    st.success("All 20 Elements Identified!")

st.markdown("<p style='text-align: center; color: #aaa; font-size: 10px; margin-top: 30px;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
