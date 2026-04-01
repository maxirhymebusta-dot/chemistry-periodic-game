import streamlit as st

# 1. CSS for Selection and Highlights
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .word-header {
        display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
        background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;
    }
    .tag-found { text-decoration: line-through; color: #adb5bd; font-weight: bold; }
    .tag-pending { color: #333; font-weight: bold; }

    /* The Grid Layout */
    .grid-container {
        display: grid; grid-template-columns: repeat(10, 1fr);
        gap: 5px; max-width: 350px; margin: 0 auto;
    }
    
    /* Letter Button Styling */
    .stButton>button {
        width: 35px !important; height: 35px !important;
        padding: 0px !important; font-size: 18px !important;
        font-weight: 900 !important; border-radius: 50% !important;
        border: 1px solid #eee !important; background-color: white !important;
        color: #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. DATA (First 20 Elements)
ELEMENTS = ["HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", "OXYGEN"]

GRID_DATA = [
    "B O X Y G E N N N N", "L E A P T U E C I I", "O S R B Z G I A T T", 
    "Z H W Y O J W R R R", "U R E R L R I B O O", "E B D L A L O O G G", 
    "I Y M U I I I N E E", "H B R U D U H U N N", "L I T H I U M L M M", 
    "C A L C I U M X Y Z"
]

# 3. SESSION STATE
if 'found' not in st.session_state: st.session_state.found = []
if 'selection' not in st.session_state: st.session_state.selection = ""

# --- TOP: WORD BANK ---
st.markdown('<div class="word-header">', unsafe_allow_html=True)
for e in ELEMENTS:
    cls = "tag-found" if e in st.session_state.found else "tag-pending"
    st.markdown(f'<span class="{cls}">{e}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- MIDDLE: THE INTERACTIVE GRID ---
st.write(f"### Current Selection: `{st.session_state.selection}`")

# Create columns for the grid
cols = st.columns(10)
for r_idx, row_str in enumerate(GRID_DATA):
    letters = row_str.split()
    for c_idx, char in enumerate(letters):
        # Unique key for every button
        if cols[c_idx].button(char, key=f"btn_{r_idx}_{c_idx}"):
            st.session_state.selection += char
            
            # Check if the built string matches any element
            for word in ELEMENTS:
                if st.session_state.selection == word:
                    if word not in st.session_state.found:
                        st.session_state.found.append(word)
                        st.success(f"Discovered: {word}!")
                        st.session_state.selection = "" # Clear after find
                        st.rerun()

# --- CONTROLS ---
col_clear, col_reset = st.columns(2)
with col_clear:
    if st.button("Clear Selection ❌"):
        st.session_state.selection = ""
        st.rerun()
with col_reset:
    if st.button("Reset Game ♻️"):
        st.session_state.clear()
        st.rerun()

st.markdown("<p style='text-align: center; color: #999; margin-top: 30px;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
