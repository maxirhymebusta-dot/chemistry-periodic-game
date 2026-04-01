import streamlit as st
import time

# 1. FIXED CSS: Forces horizontal grid and pill highlights
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    
    /* Word list at the top */
    .word-header {
        display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
        background: #f8f9fa; padding: 15px; border-radius: 10px;
        margin-bottom: 20px; border: 1px solid #eee;
    }
    .word-tag { font-size: 11px; font-weight: 700; color: #555; text-transform: uppercase; }
    .found { text-decoration: line-through; color: #ccc; }

    /* THE FIX: Forced Grid Layout */
    .grid-wrapper {
        display: grid;
        grid-template-columns: repeat(10, 1fr); /* Forces 10 columns exactly */
        gap: 2px;
        max-width: 400px;
        margin: 0 auto;
    }
    .cell {
        aspect-ratio: 1 / 1; /* Makes cells perfect squares */
        display: flex; align-items: center; justify-content: center;
        font-size: 18px; font-weight: 800; color: #333;
        font-family: sans-serif;
    }

    /* Educaplay Pill Highlights */
    .pill-red { background-color: #ffc9c9; color: #c92a2a; border-radius: 50%; }
    .pill-blue { background-color: #a5d8ff; color: #1971c2; border-radius: 50%; }
    .pill-green { background-color: #b2f2bb; color: #2b8a3e; border-radius: 50%; }

    /* Bottom Bar */
    .footer-box {
        display: flex; justify-content: space-around;
        border: 2px solid #82c91e; border-radius: 25px;
        padding: 10px; margin: 20px auto; width: 80%;
        font-weight: bold; color: #333;
    }
</style>
""", unsafe_allow_html=True)

# 2. Elements & Grid Data
ELEMENTS = [
    "HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", 
    "OXYGEN", "FLUORINE", "NEON", "SODIUM", "MAGNESIUM", "ALUMINIUM", "SILICON", 
    "PHOSPHORUS", "SULPHUR", "CHLORINE", "ARGON", "POTASSIUM", "CALCIUM"
]

GRID_DATA = [
    "B O X Y G E N N N N", "L E A P T U E C I I", "O S R B Z G I A T T", 
    "Z H W Y O J W R R R", "U R E R L R I B O O", "E B D L A L O O G G", 
    "I Y M U I I I N E E", "H B R U D U H U N N", "L I T H I U M L M M", 
    "C A L C I U M X Y Z"
]

if 'found' not in st.session_state: st.session_state.found = []
if 'start' not in st.session_state: st.session_state.start = time.time()

# --- TOP SECTION: WORD LIST ---
st.markdown('<div class="word-header">', unsafe_allow_html=True)
for e in ELEMENTS:
    cls = "word-tag found" if e in st.session_state.found else "word-tag"
    st.markdown(f'<span class="{cls}">{e}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- MIDDLE SECTION: THE GRID (FIXED) ---
st.markdown('<div class="grid-wrapper">', unsafe_allow_html=True)
for r_idx, row_str in enumerate(GRID_DATA):
    row_list = row_str.split()
    for c_idx, char in enumerate(row_list):
        highlight = ""
        # Match highlights from your screenshot
        if r_idx == 0 and c_idx in range(1, 7): highlight = "pill-red"    # OXYGEN
        if r_idx == 8 and c_idx in range(0, 7): highlight = "pill-blue"   # LITHIUM
        if c_idx == 9 and r_idx in range(0, 9): highlight = "pill-green"  # NITROGEN
        
        st.markdown(f'<div class="cell {highlight}">{char}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- BOTTOM SECTION: STATS ---
elapsed = int(time.time() - st.session_state.start)
mins, secs = divmod(elapsed, 60)
st.markdown(f'<div class="footer-box">⏱️ {mins:02d}:{secs:02d} 🧩+</div>', unsafe_allow_html=True)

# --- INTERACTION ---
user_guess = st.text_input("Found an element?", placeholder="Type name here...").upper().strip()
if st.button("Submit Discovery"):
    if user_guess in ELEMENTS and user_guess not in st.session_state.found:
        st.session_state.found.append(user_guess)
        st.rerun()

if len(st.session_state.found) == 20:
    st.balloons()
    st.success("All 20 Elements Found!")
    
