import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Row", layout="centered")

# 2. Level Data
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM", "MAGNESIUM", "ALUMINIUM"]

if 'lvl' not in st.session_state: 
    st.session_state.lvl = 0

target_word = ELEMENTS[st.session_state.lvl]

# 3. THE GAME ENGINE
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
            border-radius: 25px;
            color: white;
            text-align: center;
            width: 100%;
            max-width: 350px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            position: relative;
            transition: transform 0.2s;
        }}
        
        /* SHAKE ANIMATION FOR WRONG ANSWER */
        @keyframes shake {{
            0% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-10px); }}
            50% {{ transform: translateX(10px); }}
            75% {{ transform: translateX(-10px); }}
            100% {{ transform: translateX(0); }}
        }}
        .shake-effect {{ animation: shake 0.3s ease-in-out; }}

        .tile-row {{
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 6px;
            margin: 15px 0;
            min-height: 55px;
        }}

        .tile {{
            width: 42px;
            height: 42px;
            background: #ffffff;
            color: #1a2a6c;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 18px;
            box-shadow: 0 4px 0 #bdc3c7, 0 6px 12px rgba(0,0,0,0.3);
            cursor: pointer;
        }}

        /* FEEDBACK MESSAGES */
        #msg-overlay {{
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%) scale(0);
            padding: 15px 30px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 22px;
            z-index: 100;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            pointer-events: none;
        }}

        .msg-correct {{ background: #82c91e; color: white; box-shadow: 0 0 20px #82c91e; }}
        .msg-wrong {{ background: #ff4b2b; color: white; box-shadow: 0 0 20px #ff4b2b; }}
        .show-msg {{ transform: translate(-50%, -50%) scale(1) !important; }}

        #canvas {{ position: absolute; top: 0; left: 0; pointer-events: none; }}
        .label {{ font-size: 11px; font-weight: bold; letter-spacing: 2px; color: rgba(255,255,255,0.7); margin-top: 15px; }}
        .btn-reset {{
            margin-top: 20px; padding: 8px 18px;
            background: rgba(255,255,255,0.15);
            border: 1px solid white; color: white;
            border-radius: 12px; cursor: pointer; font-size: 12px;
        }}
    </style>
</head>
<body>

<div class="game-card" id="card">
    <canvas id="canvas"></canvas>
    <div id="msg-overlay"></div>

    <h1 style="font-family: 'Arial Black'; margin:0; font-size: 24px;">🧪 ATOMIC ROW</h1>
    <p style="font-size:14px; opacity:0.8;">Level {st.session_state.lvl + 1}</p>
    
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
    const card = document.getElementById('card');
    const msg = document.getElementById('msg-overlay');

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        ansRow.innerHTML = "";
        poolRow.innerHTML = "";

        for(let i=0; i<target.length; i++) {{
            let div = document.createElement('div');
            if(answer[i]) {{
                div.className = 'tile';
                div.innerText = answer[i];
                div.onclick = () => removeLetter(i);
            }} else {{
                div.className = 'tile empty-tile';
                div.style.background = "rgba(255,255,255,0.1)";
                div.style.border = "2px dashed rgba(255,255,255,0.3)";
                div.innerText = "?";
            }}
            ansRow.appendChild(div);
        }}

        pool.forEach((char, i) => {{
            let div = document.createElement('div');
            div.className = 'tile';
            div.innerText = char;
            div.onclick = () => addLetter(i);
            poolRow.appendChild(div);
        }});

        // CHECK LOGIC
        if(answer.length === target.length) {{
            if(answer.join('') === target) {{
                showFeedback("CORRECT! ✨", "msg-correct");
                // Particle code simplified for space
            }} else {{
                showFeedback("TRY AGAIN! ❌", "msg-wrong");
                card.classList.add('shake-effect');
                setTimeout(() => card.classList.remove('shake-effect'), 500);
            }}
        }}
    }}

    function showFeedback(text, className) {{
        msg.innerText = text;
        msg.className = className + " show-msg";
        if(className === "msg-wrong") {{
            setTimeout(() => msg.classList.remove('show-msg'), 1500);
        }}
    }}

    function addLetter(i) {{
        if(answer.length < target.length) {{
            answer.push(pool.splice(i, 1)[0]);
            render();
        }}
    }}

    function removeLetter(i) {{
        msg.classList.remove('show-msg');
        pool.push(answer.splice(i, 1)[0]);
        render();
    }}

    function resetGame() {{
        answer = [];
        pool = target.split('').sort(() => Math.random() - 0.5);
        msg.classList.remove('show-msg');
        render();
    }}

    render();
</script>

</body>
</html>
"""

# 4. Render the UI
components.html(game_html, height=500)

# 5. Next Level Button
st.write("---")
if st.button("NEXT LEVEL 🚀", use_container_width=True):
    st.session_state.lvl += 1
    if st.session_state.lvl >= len(ELEMENTS):
        st.session_state.lvl = 0
    st.rerun()

st.markdown("<p style='text-align: center; color: #777; font-size:10px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
