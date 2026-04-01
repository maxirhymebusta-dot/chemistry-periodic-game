import streamlit as st
import time

# 1. ENHANCED GAME STYLING (Educaplay Style)
st.markdown("""
<style>
    .main { background-color: #0f0c29; }
    .grid-box {
        display: grid;
        grid-template-columns: repeat(15, 30px);
        gap: 2px;
        justify-content: center;
        background: #1a1a2e;
        padding: 10px;
        border: 3px solid #00d2ff;
        border-radius: 10px;
    }
    .letter {
        width: 30px; height: 30px;
        display: flex; align-items: center; justify-content: center;
        color: #00d2ff; font-weight: bold; font-family: monospace;
        border: 1px solid #302b63; cursor: pointer;
    }
    .letter:hover { background: #3a7bd5; color: white; }
    .word-found { color: #00ff00; text-decoration: line-through; font-weight: bold; }
    .word-pending { color: #888; }
    .stat-card {
        background: rgba(255,255,255,0.1);
        padding: 10px; border-radius: 10px; text-align: center;
        border: 1px solid #00d2ff; color: white;
    }
</style>
""", unsafe_allow_html=True)

# 2. DATA: The First 20 Elements
ELEMENTS = [
    "HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", 
    "OXYGEN", "FLUORINE", "NEON", "SODIUM", "MAGNESIUM", "ALUMINIUM", "SILICON", 
    "PHOSPHORUS", "SULPHUR", "CHLORINE", "ARGON", "POTASSIUM", "CALCIUM"
]

# 3. THE GRID (15x15 Fixed for Stability)
RAW_GRID = [
    "H Y D R O G E N Q W E R T Y U",
    "E A S D F G H J K L Z X C V B",
    "L I T H I U M M N B V C X Z A",
    "I Q W E R T Y U I O P L K J H",
    "U B E R Y L L I U M G F D S A",
    "M Z X C V B N M K L J H G F D",
    "B O R O N Q W E R T Y U I O P",
    "C A R B O N Z X C V B N M K L",
    "N I T R O G E N Q W E R T Y U",
    "O X Y G E N A S D F G H J K L",
    "F L U O R I N E Z X C V B N M",
    "N E O N Q W E R T Y U I O P L",
    "S O D I U M A S D F G H J K L",
    "M A G N E S I U M Z X C V B N",
    "A L U M I N I U M Q W E R T Y"
]
grid = [row.split() for row in RAW_GRID]

# 4. GAME STATE
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'found' not in st.session_state: st.session_state.found = []
if 'score' not in st.session_state: st.session_state.score = 0

# --- HEADER SECTION ---
st.markdown('<h1 style="text-align:center; color:#00d2ff;">🔍 Element Discovery: Word Search</h1>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(f'<div class="stat-card"><b>TIME</b><br>{int(time.time() - st.session_state.start_time)}s</div>', unsafe_allow_html=True)
with col_b:
    st.markdown(f'<div class="stat-card"><b>SCORE</b><br>{st.session_state.score}</div>', unsafe_allow_html=True)
with col_c:
    st.markdown(f'<div class="stat-card"><b>FOUND</b><br>{len(st.session_state.found)}/20</div>', unsafe_allow_html=True)

# --- MAIN GAME AREA ---
st.write("---")
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="grid-box">', unsafe_allow_html=True)
    for row in grid:
        for char in row:
            st.markdown(f'<div class="letter">{char}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.subheader("Element List")
    # Input box to simulate "selecting" the word
    word_input = st.text_input("Enter a found word:").upper().strip()
    
    if st.button("Check Word", use_container_width=True):
        if word_input in ELEMENTS and word_input not in st.session_state.found:
            st.session_state.found.append(word_input)
            st.session_state.score += 50
            st.success(f"Confirmed: {word_input}!")
            time.sleep(1)
            st.rerun()
        elif word_input in st.session_state.found:
            st.warning("Already discovered!")
    
    # Scrollable list of words
    st.write("Find these elements:")
    for e in ELEMENTS:
        if e in st.session_state.found:
            st.markdown(f'<span class="word-found">✓ {e}</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="word-pending">• {e}</span>', unsafe_allow_html=True)

# --- VICTORY ---
if len(st.session_state.found) == 20:
    st.balloons()
    final_time = int(time.time() - st.session_state.start_time)
    st.success(f"🏆 MISSION COMPLETE! Final Time: {final_time} seconds.")
    if st.button("Restart Lab"):
        st.session_state.clear()
        st.rerun()
            
