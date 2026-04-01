import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Row", layout="centered")

# 2. Level Data
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM", "MAGNESIUM", "ALUMINIUM"]

if 'lvl' not in st.session_state: 
    st.session_state.lvl = 0
if 'input_val' not in st.session_state:
    st.session_state.input_val = ""

target_word = ELEMENTS[st.session_state.lvl]

# 3. THE GAME ENGINE
# No more hidden signals—just pure, fast gameplay
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Arial+Black&display=swap');
        body {{ font-family: sans-serif; margin: 0; padding: 10px; display: flex; flex-direction: column; align-items: center; background: transparent; }}
        .game-card {{
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            padding: 25px; border-radius: 25px; color: white; text-align: center;
            width: 100%; max-width: 340px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative;
        }}
        .tile-row {{ display: flex; flex-direction: row; justify-content: center; gap: 6px; margin: 15px 0; min-height: 50px; }}
        .tile {{
            width: 42px; height: 42px; background: #ffffff; color: #1a2a6c; border-radius: 10px;
            display: flex; align-items: center; justify-content: center; font-weight: 900;
            font-size: 18px; box-shadow: 0 4px 0 #bdc3c7; cursor: pointer;
        }}
        #msg-overlay {{
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0);
            padding: 15px 20px; border-radius: 20px; font-weight: bold; font-size: 20px; z-index: 100;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .msg-correct {{ background: #82c91e; color: white; box-shadow: 0 0 20px #82c91e; }}
        .show-msg {{ transform: translate(-50%, -50%) scale(1) !important; }}
    </style>
</head>
<body>
<div class="game-card" id="card">
    <div id="msg-overlay" class="msg-correct">CORRECT! ✨</div>
    <h1 style="font-family: 'Arial Black'; margin:0; font-size: 24px;">ATOMIC ROW</h1>
    <p style="font-size:14px; opacity:0.8;">Level {st.session_state.lvl + 1}</p>
    <div class="tile-row" id="ans-row"></div>
    <div class="tile-row" id="pool-row"></div>
    <button style="background:none; border:1px solid white; color:white; border-radius:5px; padding:5px 10px;" onclick="resetGame()">Reset ♻️</button>
</div>

<script>
    let target = "{target_word}";
    let pool = target.split('').sort(() => Math.random() - 0.5);
    let answer = [];

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        ansRow.innerHTML = ""; poolRow.innerHTML = "";

        for(let i=0; i<target.length; i++) {{
            let div = document.createElement('div');
            div.className = 'tile';
            if(!answer[i]) div.style.background = "rgba(255,255,255,0.1)";
            div.innerText = answer[i] || "?";
            if(answer[i]) div.onclick = () => removeLetter(i);
            ansRow.appendChild(div);
        }}

        pool.forEach((char, i) => {{
            let div = document.createElement('div');
            div.className = 'tile'; div.innerText = char;
            div.onclick = () => addLetter(i);
            poolRow.appendChild(div);
        }});

        if(answer.join('') === target) {{
            document.getElementById('msg-overlay').classList.add('show-msg');
        }} else {{
            document.getElementById('msg-overlay').classList.remove('show-msg');
        }}
    }}

    function addLetter(i) {{ if(answer.length < target.length) {{ answer.push(pool.splice(i, 1)[0]); render(); }} }}
    function removeLetter(i) {{ pool.push(answer.splice(i, 1)[0]); render(); }}
    function resetGame() {{ answer = []; pool = target.split('').sort(() => Math.random() - 0.5); render(); }}
    render();
</script>
</body>
</html>
"""

# 4. Render Game
components.html(game_html, height=420)

# 5. THE VERIFICATION ENGINE (Manual Step)
st.write("---")
# A small text input that acts as the "Verification"
check_val = st.text_input("🧪 Verify Element Name to Proceed:", placeholder="Type answer here...")

if check_val.upper() == target_word:
    if st.button("🚀 PROCEED TO NEXT LEVEL", use_container_width=True):
        st.session_state.lvl += 1
        if st.session_state.lvl >= len(ELEMENTS):
            st.session_state.lvl = 0
            st.balloons()
        st.rerun()
else:
    st.button("🔒 LEVEL LOCKED", disabled=True, use_container_width=True)

# 6. HOW TO PLAY
st.markdown("""
<div style="background: #f8f9fa; padding: 15px; border-radius: 15px; border: 1px solid #ddd; color: #333; margin-top: 10px;">
    <h4 style="margin:0; color: #1a2a6c;">📖 How to Play:</h4>
    <p style="font-size: 14px;">1. Tap letters to spell the element.<br>
    2. Once you see <b>CORRECT!</b>, type the element name in the <b>Verify</b> box below.<br>
    3. The <b>Next Level</b> button will appear instantly!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777; font-size:10px; margin-top:20px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
