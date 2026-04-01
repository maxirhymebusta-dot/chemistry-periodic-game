import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Row", layout="centered")

# 2. Level Data (The First 20 Elements)
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM", "MAGNESIUM", "ALUMINIUM"]

if 'lvl' not in st.session_state: 
    st.session_state.lvl = 0

target_word = ELEMENTS[st.session_state.lvl]

# 3. THE GAME ENGINE (HTML + JAVASCRIPT)
# This handles all the logic internally so duplication cannot happen.
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Arial+Black&display=swap');
        
        body {{
            font-family: sans-serif;
            margin: 0;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .game-card {{
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            padding: 20px;
            border-radius: 20px;
            color: white;
            text-align: center;
            width: 100%;
            max-width: 350px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        .tile-row {{
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 8px;
            margin: 15px 0;
            min-height: 55px;
        }}

        .tile {{
            width: 45px;
            height: 45px;
            background: #ffffff;
            color: #1a2a6c;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 18px;
            box-shadow: 0 4px 0 #bdc3c7, 0 6px 10px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: transform 0.1s;
        }}

        .tile:active {{ transform: translateY(3px); box-shadow: 0 1px 0 #bdc3c7; }}

        .empty-tile {{
            background: rgba(255,255,255,0.1);
            border: 2px dashed rgba(255,255,255,0.3);
            box-shadow: none;
            color: transparent;
        }}
        
        .label {{ font-size: 12px; font-weight: bold; letter-spacing: 2px; color: #eee; margin-top: 15px; }}
        
        .btn-reset {{
            margin-top: 20px;
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            border: 1px solid white;
            color: white;
            border-radius: 10px;
            cursor: pointer;
        }}
    </style>
</head>
<body>

<div class="game-card">
    <h1 style="font-family: 'Arial Black'; margin:0; font-size: 24px;">🧪 ATOMIC ROW</h1>
    <p id="lvl-text" style="font-size:14px; opacity:0.8;">Level {st.session_state.lvl + 1}</p>
    
    <div class="label">YOUR WORD</div>
    <div class="tile-row" id="ans-row"></div>

    <div class="label">LETTER POOL</div>
    <div class="tile-row" id="pool-row"></div>
    
    <button class="btn-reset" onclick="resetGame()">Reset Level ♻️</button>
</div>

<script>
    let target = "{target_word}";
    let pool = target.split('').sort(() => Math.random() - 0.5);
    let answer = [];

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        
        // Render Answer Row
        ansRow.innerHTML = "";
        for(let i=0; i<target.length; i++) {{
            if(answer[i]) {{
                let div = document.createElement('div');
                div.className = 'tile';
                div.innerText = answer[i];
                div.onclick = () => removeLetter(i);
                ansRow.appendChild(div);
            }} else {{
                let div = document.createElement('div');
                div.className = 'tile empty-tile';
                div.innerText = "?";
                ansRow.appendChild(div);
            }}
        }}

        // Render Pool
        poolRow.innerHTML = "";
        pool.forEach((char, i) => {{
            let div = document.createElement('div');
            div.className = 'tile';
            div.innerText = char;
            div.onclick = () => addLetter(i);
            poolRow.appendChild(div);
        }});

        if(answer.join('') === target) {{
            setTimeout(() => {{ alert("STABILIZED: " + target + "! Click the Next Level button below."); }}, 300);
        }}
    }}

    function addLetter(i) {{
        if(answer.length < target.length) {{
            answer.push(pool.splice(i, 1)[0]);
            render();
        }}
    }}

    function removeLetter(i) {{
        pool.push(answer.splice(i, 1)[0]);
        render();
    }}

    function resetGame() {{
        answer = [];
        pool = target.split('').sort(() => Math.random() - 0.5);
        render();
    }}

    render();
</script>

</body>
</html>
"""

# 4. Render the UI
components.html(game_html, height=480)

# 5. Next Level Button (Streamlit Side)
st.write("---")
if st.button("NEXT LEVEL 🚀", use_container_width=True):
    st.session_state.lvl += 1
    if st.session_state.lvl >= len(ELEMENTS):
        st.session_state.lvl = 0 # Loop back to start
    st.rerun()

st.markdown("<p style='text-align: center; color: #777; font-size:10px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
                
