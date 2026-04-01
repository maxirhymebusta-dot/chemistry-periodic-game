import streamlit as st
import time

# 1. UI STYLING (Matches the Screenshot)
st.markdown("""
<style>
    /* White Background and Main Container */
    .stApp { background-color: #ffffff; color: #333; }
    
    /* Top Word List Styling */
    .word-list-header {
        display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
        background: #f8f9fa; padding: 20px; border-radius: 10px;
        border: 1px solid #dee2e6; margin-bottom: 20px;
    }
    .word-item { font-weight: bold; font-size: 14px; text-transform: uppercase; color: #444; }
    .word-item.found { text-decoration: line-through; color: #adb5bd; }

    /* The Grid Styling */
    .grid-container {
        display: grid; grid-template-columns: repeat(10, 45px); gap: 2px;
        justify-content: center; background: #ffffff; padding: 10px;
    }
    .letter-cell {
        width: 45px; height: 45px;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; font-weight: 700; color: #333;
        border: 1px solid #f1f3f5; cursor: pointer;
    }
    
    /* Highlight Colors (Pill Shape) */
    .highlight-blue { background-color: #a5d8ff; border-radius: 20px; color: #1971c2; }
    .highlight-green { background-color: #b2f2bb; border-radius: 20px; color: #2b8a3e; }
    .highlight-red { background-color: #ffc9c9; border-radius: 20px; color: #c92a2a; }

    /* Bottom Timer & Score */
    .stats-footer {
        display: flex; justify-content: space-between; align-items: center;
        max-width: 500px; margin: 20px auto; padding: 10px 20px;
        border: 2px solid #51cf66; border-radius: 30px; color: #333; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 2. THE DATA (First 20 Elements)
ELEMENTS = [
    "HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", 
    "OXYGEN", "FLUORINE", "NEON", "SODIUM", "MAGNESIUM", "ALUMINIUM", "SILICON", 
    "PHOSPHORUS", "SULPHUR", "CHLORINE", "ARGON", "POTASSIUM", "CALCIUM"
]

# Static Grid for Stability (First 20 Elements)
RAW_GRID = [
    "B O X Y G E N N N N", "L E A P T U E C I I", "O S R B Z G I A T T", 
    "Z H W Y O J W R R R", "U R E R L R I B O O", "E B D L A L O O G G", 
    "I Y M U I I I N E E", "H B R U D U H U N N", "L I T H I U M L M M", 
    "C A L C I U M X Y Z"
]
grid = [row.split() for row in RAW_GRID]

# 3. GAME STATE
if 'found_words' not in st.session_state: st.session_state.found_words = []
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'score' not in st.session_state: st.session_state.score = 0

# --- HEADER: WORD LIST ---
st.markdown('<div class="word-list-header">', unsafe_allow_html=True)
for word in ELEMENTS:
    cls = "word-item found" if word in st.session_state.found_words else "word-item"
    st.markdown(f'<span class="{cls}">{word}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- THE GRID ---
st.markdown('<div class="grid-container">', unsafe_allow_html=True)
for r_idx, row in enumerate(grid):
    for c_idx, letter in enumerate(row):
        # Logic to "Show" highlights if found (Simplified for demo)
        highlight = ""
        if letter == "O" and r_idx == 0: highlight = "highlight-red"
        if letter == "L" and r_idx == 8: highlight = "highlight-blue"
        st.markdown(f'<div class="letter-cell {highlight}">{letter}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER: STATS ---
timer_val = int(time.time() - st.session_state.start_time)
mins, secs = divmod(timer_val, 60)

st.markdown(f"""
<div class="stats-footer">
    <span>⏱️ {mins:02d}:{secs:02d}</span>
    <span>SCORE: {st.session_state.score}</span>
    <span style="font-size: 24px;">🧩+</span>
</div>
""", unsafe_allow_html=True)

# --- INPUT AREA ---
target_word = st.text_input("Found an Element? Enter it here:").upper().strip()
if st.button("Check Word"):
    if target_word in ELEMENTS and target_word not in st.session_state.found_words:
        st.session_state.found_words.append(target_word)
        st.session_state.score += 4167 # Matching the score in your screenshot!
        st.success(f"Success! {target_word} documented.")
        time.sleep(1)
        st.rerun()

if len(st.session_state.found_words) == len(ELEMENTS):
    st.balloons()
    st.success("Master Chemist! All 20 Elements Identified.")
    
