import streamlit as st
import time

# 1. THE LAYOUT (Clean White Grid)
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .word-bank {
        display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
        background: #f8f9fa; padding: 10px; border-radius: 10px; margin-bottom: 15px;
    }
    .word-tag { font-size: 11px; font-weight: bold; color: #555; text-transform: uppercase; }
    .found { text-decoration: line-through; color: #cbd5e0; }

    /* FORCED GRID: This ensures 10 columns on ALL screens */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        gap: 5px;
        max-width: 350px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# 2. DATA (First 20 Elements)
ELEMENTS = ["HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", "OXYGEN"]
GRID_DATA = [
    "B", "O", "X", "Y", "G", "E", "N", "N", "N", "N",
    "L", "E", "A", "P", "T", "U", "E", "C", "I", "I",
    "O", "S", "R", "B", "Z", "G", "I", "A", "T", "T",
    "Z", "H", "W", "Y", "O", "J", "W", "R", "R", "R",
    "U", "R", "E", "R", "L", "R", "I", "B", "O", "O",
    "E", "B", "D", "L", "A", "L", "O", "O", "G", "G",
    "I", "Y", "M", "U", "I", "I", "I", "N", "E", "E",
    "H", "B", "R", "U", "D", "U", "H", "U", "N", "N",
    "L", "I", "T", "H", "I", "U", "M", "L", "M", "M",
    "C", "A", "L", "C", "I", "U", "M", "X", "Y", "Z"
]

if 'found' not in st.session_state: st.session_state.found = []
if 'clicks' not in st.session_state: st.session_state.clicks = []

# --- TOP: WORD BANK ---
st.markdown('<div class="word-bank">', unsafe_allow_html=True)
for e in ELEMENTS:
    cls = "found" if e in st.session_state.found else ""
    st.markdown(f'<span class="word-tag {cls}">{e}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- MIDDLE: THE INTERACTIVE GRID ---
st.write("### 🧪 Tap the First & Last letter of the word")

# Creating the grid using standard Streamlit buttons (High Reliability)
cols = st.columns(10)
for idx, char in enumerate(GRID_DATA):
    # Determine the color of the button
    btn_type = "primary" if idx in st.session_state.clicks else "secondary"
    
    with cols[idx % 10]:
        if st.button(char, key=f"btn_{idx}"):
            st.session_state.clicks.append(idx)
            
            # When two letters are clicked, try to form a word
            if len(st.session_state.clicks) == 2:
                start, end = sorted(st.session_state.clicks)
                # Simple logic to get the string between two clicks
                word = "".join([GRID_DATA[i] for i in range(start, end + 1)])
                
                if word in ELEMENTS:
                    st.session_state.found.append(word)
                    st.success(f"Confirmed: {word}!")
                    time.sleep(1)
                else:
                    st.error("Try a different path!")
                
                st.session_state.clicks = [] # Reset clicks
                st.rerun()

# --- FOOTER ---
if st.button("Reset Laboratory"):
    st.session_state.clear()
    st.rerun()

st.markdown("<p style='text-align: center; color: #999;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
