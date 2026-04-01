import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Row", layout="centered")

# 2. Level Data
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM"]

if 'lvl' not in st.session_state: st.session_state.lvl = 0
target_word = ELEMENTS[st.session_state.lvl]

# 3. Game Logic (Session State)
if 'ans_tiles' not in st.session_state: st.session_state.ans_tiles = []
if 'pool_tiles' not in st.session_state:
    p = list(target_word)
    random.shuffle(p)
    st.session_state.pool_tiles = p

# Handle Tile Clicks via Query Params (to keep it fast)
params = st.query_params
if "action" in params:
    act = params["action"]
    idx = int(params["idx"])
    
    if act == "add":
        val = st.session_state.pool_tiles.pop(idx)
        st.session_state.ans_tiles.append(val)
    elif act == "remove":
        val = st.session_state.ans_tiles.pop(idx)
        st.session_state.pool_tiles.append(val)
    
    st.query_params.clear()
    st.rerun()

# 4. CUSTOM HTML/CSS ENGINE
# This forces the horizontal layout using Flexbox
tile_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Arial+Black&display=swap');
    
    .game-body {
        font-family: sans-serif;
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
        padding: 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
    }
    
    /* THE MAGIC: Forces horizontal alignment */
    .tile-row {
        display: flex;
        flex-direction: row;
        justify-content: center;
        flex-wrap: nowrap; 
        gap: 8px;
        margin: 15px 0;
        overflow-x: auto; /* Adds scroll if word is very long */
        padding: 10px 0;
    }

    .tile {
        width: 45px;
        height: 45px;
        background: #fdfdfd;
        color: #1a2a6c;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 18px;
        box-shadow: 0 4px 0 #bdc3c7, 0 6px 10px rgba(0,0,0,0.3);
        cursor: pointer;
        text-decoration: none;
    }

    .empty-tile {
        background: rgba(255,255,255,0.1);
        border: 2px dashed rgba(255,255,255,0.3);
        box-shadow: none;
        color: rgba(255,255,255,0.2);
    }
    
    .label { font-size: 12px; font-weight: bold; letter-spacing: 2px; color: #eee; margin-top: 20px;}
</style>
"""

# Build the Answer Row HTML
ans_html = "".join([f'<div class="tile">{char}</div>' for char in st.session_state.ans_tiles])
# Add empty slots for remaining letters
empty_slots = len(target_word) - len(st.session_state.ans_tiles)
ans_html += "".join(['<div class="tile empty-tile">?</div>' for _ in range(empty_slots)])

# Build the Pool Row HTML (with links to trigger Python logic)
pool_html = ""
for i, char in enumerate(st.session_state.pool_tiles):
    # Using a simple link that Streamlit can catch
    pool_html += f'<a href="?action=add&idx={i}" target="_self" class="tile">{char}</a>'

# Combine everything
full_html = f"""
{tile_css}
<div class="game-body">
    <h1 style="font-family: 'Arial Black'; margin:0;">🧪 ATOMIC ROW</h1>
    <p style="font-size:14px; opacity:0.8;">Level {st.session_state.lvl + 1}</p>
    
    <div class="label">YOUR WORD</div>
    <div class="tile-row">
        {ans_html}
    </div>

    <div class="label">LETTER POOL</div>
    <div class="tile-row">
        {pool_html}
    </div>
</div>
"""

# Render the custom HTML
st.components.v1.html(full_html, height=450)

# 5. WIN & RESET (Back in Streamlit)
if "".join(st.session_state.ans_tiles) == target_word:
    st.balloons()
    st.success(f"STABILIZED: {target_word}")
    if st.button("NEXT LEVEL 🚀", use_container_width=True):
        st.session_state.lvl += 1
        st.session_state.ans_tiles = []
        if st.session_state.lvl < len(ELEMENTS):
            st.session_state.pool_tiles = list(ELEMENTS[st.session_state.lvl])
            random.shuffle(st.session_state.pool_tiles)
            st.rerun()

if st.button("Reset Level ♻️", use_container_width=True):
    st.session_state.ans_tiles = []
    p = list(target_word)
    random.shuffle(p)
    st.session_state.pool_tiles = p
    st.rerun()

st.markdown("<p style='text-align: center; color: #777; font-size:10px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
