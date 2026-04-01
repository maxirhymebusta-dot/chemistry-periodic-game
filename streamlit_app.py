import streamlit as st
import time

# 1. THE STYLES (Clean White, Pill Shapes, and Table Grid)
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .word-header {
        display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
        background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;
    }
    .tag { font-size: 10px; font-weight: 700; color: #444; text-transform: uppercase; }
    .found { text-decoration: line-through; color: #ccc; }

    /* THE FIX: Standard HTML Table for a perfect Grid */
    table.game-grid {
        margin-left: auto; margin-right: auto;
        border-collapse: separate; border-spacing: 4px;
    }
    td.cell {
        width: 32px; height: 32px;
        text-align: center; vertical-align: middle;
        font-size: 18px; font-weight: 900; color: #333;
        font-family: sans-serif;
    }

    /* Pill Highlights from your Screenshot */
    .pill-red { background-color: #ffc9c9; border-radius: 50%; color: #c92a2a; }
    .pill-blue { background-color: #a5d8ff; border-radius: 50%; color: #1971c2; }
    .pill-green { background-color: #b2f2bb; border-radius: 50%; color: #2b8a3e; }

    .footer-bar {
        display: flex; justify-content: space-around; align-items: center;
        width: 280px; margin: 25px auto; padding: 8px;
        border: 2px solid #82c91e; border-radius: 30px;
        font-weight: bold; color: #333;
    }
</style>
""", unsafe_allow_html=True)

# 2. DATA (First 20 Elements)
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

# --- WORD LIST ---
st.markdown('<div class="word-header">', unsafe_allow_html=True)
for e in ELEMENTS:
    status = "found" if e in st.session_state.found else ""
    st.markdown(f'<span class="tag {status}">{e}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- THE GRID (Using Table to Force Format) ---
grid_html = '<table class="game-grid">'
for r_idx, row_str in enumerate(GRID_DATA):
    grid_html += '<tr>'
    letters = row_str.split()
    for c_idx, char in enumerate(letters):
        h = ""
        # Manual Highlight Mapping
        if r_idx == 0 and c_idx in range(1,7): h = "pill-red"
        if r_idx == 8 and c_idx in range(0,7): h = "pill-blue"
        if c_idx == 9 and r_idx in range(0,9): h = "pill-green"
        grid_html += f'<td class="cell {h}">{char}</td>'
    grid_html += '</tr>'
grid_html += '</table>'

st.markdown(grid_html, unsafe_allow_html=True)

# --- FOOTER ---
elapsed = int(time.time() - st.session_state.start)
m, s = divmod(elapsed, 60)
st.markdown(f'<div class="footer-bar">⏱️ {m:02d}:{s:02d} 🧩+</div>', unsafe_allow_html=True)

# --- INPUT ---
val = st.text_input("Found an element?", placeholder="Type name here...").upper().strip()
if st.button("Check"):
    if val in ELEMENTS and val not in st.session_state.found:
        st.session_state.found.append(val)
        st.rerun()

st.markdown("<p style='text-align: center; color: #aaa; font-size: 10px;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
