import streamlit as st
import random

# 1. Page Setup & Jigsaw Styling
st.set_page_config(page_title="Atomic Jigsaw", layout="centered")

st.markdown("""
<style>
    /* Puzzle Tile Styling */
    .puzzle-tile {
        height: 70px; display: flex; align-items: center; justify-content: center;
        background-color: #ffffff; border: 2px solid #82c91e;
        border-radius: 10px; font-weight: 800; font-size: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #333;
    }
    .selected-tile { background-color: #a5d8ff !important; border-color: #1971c2 !important; }
    .correct-row { background-color: #b2f2bb !important; border-color: #2b8a3e !important; }
    .header-text { text-align: center; color: #2b8a3e; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 2. Data for the Puzzle (First 20 Elements)
ELEMENTS = [
    {"num": "1", "sym": "H", "name": "Hydrogen"},
    {"num": "2", "sym": "He", "name": "Helium"},
    {"num": "3", "sym": "Li", "name": "Lithium"},
    {"num": "4", "sym": "Be", "name": "Beryllium"},
    {"num": "5", "sym": "B", "name": "Boron"}
]

# 3. Initialize Game State
if 'board' not in st.session_state:
    # Create a scrambled list of all pieces
    nums = [e['num'] for e in ELEMENTS]
    syms = [e['sym'] for e in ELEMENTS]
    names = [e['name'] for e in ELEMENTS]
    random.shuffle(nums); random.shuffle(syms); random.shuffle(names)
    st.session_state.board = {"nums": nums, "syms": syms, "names": names}

if 'selected' not in st.session_state: st.session_state.selected = None # (column, index)

# 4. Game UI
st.markdown("<h2 class='header-text'>🧩 THE ATOMIC JIGSAW</h2>", unsafe_allow_html=True)
st.write("Tap two tiles in the same column to swap them. Align the rows correctly!")

# 5. The Puzzle Grid
cols = st.columns(3)
column_keys = ["nums", "syms", "names"]
column_titles = ["Atomic #", "Symbol", "Name"]

for i, col_key in enumerate(column_keys):
    with cols[i]:
        st.markdown(f"<p style='text-align:center; font-weight:bold;'>{column_titles[i]}</p>", unsafe_allow_html=True)
        for idx, val in enumerate(st.session_state.board[col_key]):
            # Check if this row is already correct
            is_correct = (
                st.session_state.board["nums"][idx] == ELEMENTS[idx]["num"] and
                st.session_state.board["syms"][idx] == ELEMENTS[idx]["sym"] and
                st.session_state.board["names"][idx] == ELEMENTS[idx]["name"]
            )
            
            # Check if selected
            is_sel = st.session_state.selected == (col_key, idx)
            
            # Button Logic
            tile_style = "correct-row" if is_correct else ("selected-tile" if is_sel else "")
            
            if st.button(val, key=f"{col_key}_{idx}", use_container_width=True):
                if st.session_state.selected is None:
                    st.session_state.selected = (col_key, idx)
                    st.rerun()
                else:
                    prev_col, prev_idx = st.session_state.selected
                    if prev_col == col_key: # Only swap within the same column
                        # Swap values
                        st.session_state.board[col_key][prev_idx], st.session_state.board[col_key][idx] = \
                            st.session_state.board[col_key][idx], st.session_state.board[col_key][prev_idx]
                        st.session_state.selected = None
                        st.rerun()
                    else:
                        st.session_state.selected = (col_key, idx)
                        st.rerun()

# 6. Check Win Condition
all_correct = True
for idx in range(len(ELEMENTS)):
    if not (st.session_state.board["nums"][idx] == ELEMENTS[idx]["num"] and
            st.session_state.board["syms"][idx] == ELEMENTS[idx]["sym"] and
            st.session_state.board["names"][idx] == ELEMENTS[idx]["name"]):
        all_correct = False

if all_correct:
    st.balloons()
    st.success("🏆 ATOM STABILIZED! Level Complete.")
    if st.button("Next Level"):
        st.session_state.clear()
        st.rerun()

st.write("---")
st.markdown("<p style='text-align: center; color: #999;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
    
