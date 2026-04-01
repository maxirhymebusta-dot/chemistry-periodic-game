import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Row", layout="centered")

# 2. Level Data
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM", "MAGNESIUM", "ALUMINIUM"]

if 'lvl' not in st.session_state: 
    st.session_state.lvl = 0
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

target_word = ELEMENTS[st.session_state.lvl]

# 3. Handle Unlock Signal (Hidden trigger to show the button)
if st.query_params.get("status") == "success":
    st.session_state.unlocked = True
    st.query_params.clear()

# 4. THE GAME ENGINE (Internal Logic + Sound + Unlock Signal)
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Arial+Black&display=swap');
        body {{ font-family: sans-serif; margin: 0; padding: 10px; display: flex; flex-direction: column; align-items: center; }}
        .game-card {{
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            padding: 25px; border-radius: 30px; color: white; text-align: center;
            width: 100%; max-width: 360px; box-shadow: 0 15px 50px rgba(0,0,0,0.6);
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
            padding: 15px 25px; border-radius: 50px; font-weight: bold; font-size: 22px; z-index: 100;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .msg-correct {{ background: #82c91e; color: white; box-shadow: 0 0 20px #82c91e; }}
        .msg-wrong {{ background: #ff4b2b; color: white; box-shadow: 0 0 20px #ff4b2b; }}
        .show-msg {{ transform: translate(-50%, -50%) scale(1) !important; }}
        .btn-reset {{
            margin-top: 15px; padding: 10px 20px; background: rgba(255,255,255,0.2);
            border: 1px solid white; color: white; border-radius: 15px; cursor: pointer;
            display: none; width: 100%;
        }}
        .visible {{ display: block !important; }}
    </style>
</head>
<body>
<div class="game-card" id="card">
    <div id="msg-overlay"></div>
    <h1 style="font-family: 'Arial Black'; margin:0; font-size: 26px;">ATOMIC ROW</h1>
    <p style="font-size:14px; opacity:0.8;">Level {st.session_state.lvl + 1}</p>
    <div style="font-size:11px; margin-top:15px; opacity:0.7;">YOUR WORD</div>
    <div class="tile-row" id="ans-row"></div>
    <div style="font-size:11px; margin-top:5px; opacity:0.7;">LETTER POOL</div>
    <div class="tile-row" id="pool-row"></div>
    <button id="reset-btn" class="btn-reset" onclick="resetGame()">Reset Level ♻️</button>
</div>

<script>
    let target = "{target_word}";
    let pool = target.split('').sort(() => Math.random() - 0.5);
    let answer = [];
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playTone(freq, type, duration) {{
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + duration);
    }}

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        const resetBtn = document.getElementById('reset-btn');
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

        if(answer.length === target.length) {{
            if(answer.join('') === target) {{
                playTone(523, 'sine', 0.5);
                document.getElementById('msg-overlay').innerText = "CORRECT! ✨";
                document.getElementById('msg-overlay').className = "msg-correct show-msg";
                // TRIGGER UNLOCK: Reload parent with a query param
                setTimeout(() => {{ window.parent.location.href = window.parent.location.pathname + "?status=success"; }}, 1000);
            }} else {{
                playTone(150, 'sawtooth', 0.3);
                document.getElementById('msg-overlay').innerText = "WRONG! ❌";
                document.getElementById('msg-overlay').className = "msg-wrong show-msg";
                resetBtn.classList.add('visible');
            }}
        }}
    }}

    function addLetter(i) {{ if(answer.length < target.length) {{ answer.push(pool.splice(i, 1)[0]); render(); }} }}
    function removeLetter(i) {{ pool.push(answer.splice(i, 1)[0]); render(); }}
    function resetGame() {{ 
        answer = []; pool = target.split('').sort(() => Math.random() - 0.5); 
        document.getElementById('msg-overlay').classList.remove('show-msg');
        document.getElementById('reset-btn').classList.remove('visible');
        render(); 
    }}
    render();
</script>
</body>
</html>
"""

# 5. Render Game
components.html(game_html, height=480)

st.write("---")

# 6. LOCKED PROGRESSION (Appears ABOVE How to Play)
if st.session_state.unlocked:
    if st.button("🚀 PROCEED TO NEXT LEVEL", use_container_width=True):
        st.session_state.lvl += 1
        st.session_state.unlocked = False # Relock for next level
        if st.session_state.lvl >= len(ELEMENTS):
            st.session_state.lvl = 0
            st.success("🏆 YOU COMPLETED ALL ELEMENTS!")
        st.rerun()
else:
    st.info("🔒 Solve the puzzle to unlock the next level.")

# 7. HOW TO PLAY (Below the Unlock Button)
st.markdown("""
<div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #ddd; margin-top:10px;">
    <h4 style="margin-top:0;">📖 How to Play:</h4>
    <ul style="font-size: 14px;">
        <li><b>Objective:</b> Unscramble the letters to spell the first 20 elements.</li>
        <li><b>Tapping:</b> Tap a letter in the <b>Pool</b> to move it to your word.</li>
        <li><b>Corrections:</b> Tap a letter in <b>Your Word</b> to send it back to the pool.</li>
        <li><b>Locking:</b> The 'Next Level' button will only appear once the current element is stabilized.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777; font-size:10px; margin-top:20px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
