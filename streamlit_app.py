import streamlit as st
import time

# 1. UI STYLING (The "Clean White" Educaplay Look)
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    
    /* Top Word List */
    .word-bank {
        display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
        background: #f8f9fa; padding: 15px; border-radius: 10px;
        border: 1px solid #eee; margin-bottom: 20px;
    }
    .word-item { font-size: 12px; font-weight: 800; color: #444; text-transform: uppercase; }
    .found { text-decoration: line-through; color: #cbd5e0; }

    /* The Grid Layout (Fixed 12x12 for 20 words) */
    .grid-wrapper {
        display: grid; grid-template-columns: repeat(12, 1fr);
        gap: 4px; max-width: 450px; margin: 0 auto;
    }
    .letter-cell {
        aspect-ratio: 1/1; display: flex; align-items: center; justify-content: center;
        font-size: 18px; font-weight: 900; color: #333; border-radius: 5px;
    }

    /* Educaplay Pill Highlights */
    .highlight { background-color: #b2f2bb; color: #2b8a3e; border-radius: 25px; }

    /* Bottom Stats Bar */
    .footer-stats {
        display: flex; justify-content: space-around; align-items: center;
        width: 280px; margin: 25px auto; padding: 10px;
        border: 2.5px solid #82c91e; border-radius: 35px;
        font-weight: bold; color: #333;
    }
</style>
""", unsafe_allow_html=True)

# 2. DATA: The First 20 Elements
ELEMENTS = [
    "HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", 
    "OXYGEN", "FLUORINE", "NEON", "SODIUM", "MAGNESIUM", "ALUMINIUM", "SILICON", 
    "PHOSPHORUS", "SULPHUR", "CHLORINE", "ARGON", "POTASSIUM", "CALCIUM"
]

# 12x12 Grid Data (Carefully Mapped)
GRID_MAP = [
    "H Y D R O G E N X B C A",
    "E X L I T H I U M E B L",
    "L A B E R Y L L I U M C",
    "I C A R B O N M Q Y S I",
    "U N I T R O G E N L P U",
    "M B E R Y L L I U M S M",
    "O X Y G E N A B C D F P",
    "N E O N M A G N E S I U",
    "P O T A S S I U M X Y S",
    "S U L P H U R C H L O R",
    "C H L O R I N E X Y Z A",
    "A L U M I N I U M X Y Z"
]

if 'found' not in st.session_state: st.session_state.found = []
if 'start' not in st.session_state: st.session_state.start = time.time()

# --- HEADER: WORD LIST ---
st.markdown('<div class="word-bank">', unsafe_allow_html=True)
for e in ELEMENTS:
    status = "found" if e in st.session_state.found else ""
    st.markdown(f'<span class="word-item {status}">{e}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- THE GRID ---
st.markdown('<div class="grid-wrapper">', unsafe_allow_html=True)
for r_idx, row_str in enumerate(GRID_MAP):
    row_list = row_str.split()
    for c_idx, char in enumerate(row_list):
        # We can add a "highlight" class here for words found
        st.markdown(f'<div class="letter-cell">{char}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER: TIMER ---
elapsed = int(time.time() - st.session_state.start)
mm, ss = divmod(elapsed, 60)
st.markdown(f'<div class="footer-stats">⏱️ {mm:02d}:{ss:02d} 🧩+</div>', unsafe_allow_html=True)

# --- USER INPUT ---
st.write("---")
col_in, col_btn = st.columns([3, 1])
with col_in:
    guess = st.text_input("Found an element?", placeholder="Type name here...").upper().strip()
with col_btn:
    if st.button("Check"):
        if guess in ELEMENTS and guess not in st.session_state.found:
            st.session_state.found.append(guess)
            st.rerun()

if len(st.session_state.found) == 20:
    st.balloons()
    st.success("All 20 Elements Identified! Gate Mastered.")
    
st.markdown("<p style='text-align: center; color: #999; margin-top: 20px;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
