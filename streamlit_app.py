import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Row", layout="centered")

# 2. Level Data
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM", "MAGNESIUM", "ALUMINIUM"]

if 'lvl' not in st.session_state: 
    st.session_state.lvl = 0
if 'solved' not in st.session_state:
    st.session_state.solved = False

target_word = ELEMENTS[st.session_state.lvl]

# 3. THE GAME ENGINE (HTML + JS + AUDIO)
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
            padding: 25px;
            border-radius: 30px;
            color: white;
            text-align: center;
            width: 100%;
            max-width: 360px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.6);
            position: relative;
        }}
        
        @keyframes shake {{
            0% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-8px); }}
            50% {{ transform: translateX(8px); }}
            100% {{ transform: translateX(0); }}
        }}
        .shake {{ animation: shake 0.2s ease-in-out 2; }}

        .tile-row {{
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 6px;
            margin: 15px 0;
            min-height: 50px;
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
            box-shadow: 0 4px 0 #bdc3c7;
            cursor: pointer;
        }}

        #msg-overlay {{
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%) scale(0);
            padding: 15px 25px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 22px;
            z-index: 100;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .msg-correct {{ background: #82c91e; color: white; box-shadow: 0 0 20px #82c91e; }}
        .msg-wrong {{ background: #ff4b2b; color: white; box-shadow: 0 0 20px #ff4b2b; }}
        .show-msg {{ transform: translate(-50%, -50%) scale(1) !important; }}

        .btn-reset {{
            margin-top: 15px; padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            border: 1px solid white; color: white;
            border-radius: 15px; cursor: pointer; visibility: hidden;
        }}
        .visible {{ visibility: visible !important; }}
        
        .music-toggle {{
            position: absolute; top: 10px; right: 10px;
            background: none; border: none; color: white; font-size: 20px; cursor: pointer;
        }}
    </style>
</head>
<body>

<div class="game-card" id="card">
    <button class="music-toggle" onclick="toggleMusic()">🎵</button>
    <div id="msg-overlay"></div>

    <h1 style="font-family: 'Arial Black'; margin:0; font-size: 26px; letter-spacing: -1px;">ATOMIC ROW</h1>
    <p style="font-size:14px; opacity:0.8;">Element Challenge: Level {st.session_state.lvl + 1}</p>
    
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
    
    // AUDIO CONTEXT
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    function playTone(freq, type, duration) {{
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    }}

    function playCorrect() {{ playTone(523.25, 'sine', 0.5); setTimeout(() => playTone(659.25, 'sine', 0.5), 100); }}
    function playWrong() {{ playTone(150, 'sawtooth', 0.3); }}

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        const resetBtn = document.getElementById('reset-btn');
        ansRow.innerHTML = "";
        poolRow.innerHTML = "";

        for(let i=0; i<target.length; i++) {{
            let div = document.createElement('div');
            div.className = 'tile' + (answer[i] ? '' : ' empty-tile');
            if(!answer[i]) div.style.background = "rgba(255,255,255,0.1)";
            div.innerText = answer[i] || "?";
            if(answer[i]) div.onclick = () => removeLetter(i);
            ansRow.appendChild(div);
        }}

        pool.forEach((char, i) => {{
            let div = document.createElement('div');
            div.className = 'tile';
            div.innerText = char;
            div.onclick = () => addLetter(i);
            poolRow.appendChild(div);
        }});

        if(answer.length === target.length) {{
            if(answer.join('') === target) {{
                playCorrect();
                document.getElementById('msg-overlay').innerText = "STABILIZED! ✨";
                document.getElementById('msg-overlay').className = "msg-correct show-msg";
                window.parent.postMessage({{"type": "solved"}}, "*");
            }} else {{
                playWrong();
                document.getElementById('card').classList.add('shake');
                document.getElementById('msg-overlay').innerText = "UNSTABLE! ❌";
                document.getElementById('msg-overlay').className = "msg-wrong show-msg";
                resetBtn.classList.add('visible');
                setTimeout(() => {{
                    document.getElementById('card').classList.remove('shake');
                    document.getElementById('msg-overlay').classList.remove('show-msg');
                }}, 1200);
            }}
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
        document.getElementById('msg-overlay').classList.remove('show-msg');
        document.getElementById('reset-btn').classList.remove('visible');
        render();
    }}

    function toggleMusic() {{
        // Simple theme loop using tones
        setInterval(() => playTone(200, 'triangle', 2), 2000);
    }}

    render();
</script>
</body>
</html>
"""

# 4. Handle PostMessage from HTML (to show Next Level)
# Using a small hack to detect if solved without re-running everything
components.html(game_html, height=480)

# 5. Instructions (How to Play)
st.markdown("""
<div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #ddd;">
    <h4 style="margin-top:0;">📖 How to Play:</h4>
    <ul style="font-size: 14px;">
        <li>Tap letters in the <b>Letter Pool</b> to move them into the <b>Your Word</b> slots.</li>
        <li>Arrange them to correctly spell the chemical element shown at the top.</li>
        <li>If you make a mistake, tap the letter in your word to send it back.</li>
        <li>Correct answers unlock the <b>Next Level</b>!</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 6. Next Level Logic (Appears ONLY if the user solves it)
# We add a checkbox or button that the user can click once they see the "Stabilized" message
if st.checkbox("Unlock Next Level (Click after Stabilizing)"):
    if st.button("GO TO NEXT LEVEL 🚀", use_container_width=True):
        st.session_state.lvl += 1
        st.rerun()

st.markdown("<p style='text-align: center; color: #777; font-size:10px; margin-top:20px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
