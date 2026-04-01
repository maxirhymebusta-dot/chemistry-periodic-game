import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Row", layout="centered")

# 2. Level Data
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM", "MAGNESIUM", "ALUMINIUM"]

if 'lvl' not in st.session_state: st.session_state.lvl = 0

target_word = ELEMENTS[st.session_state.lvl]

# 3. THE GAME ENGINE (HTML + JS + AUTO-UNLOCK)
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Arial+Black&display=swap');
        body {{ font-family: sans-serif; margin: 0; padding: 10px; display: flex; flex-direction: column; align-items: center; background: transparent; overflow: hidden; }}
        .game-card {{
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            padding: 25px; border-radius: 25px; color: white; text-align: center;
            width: 100%; max-width: 340px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative; transition: transform 0.2s;
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
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); pointer-events: none;
        }}
        .msg-correct {{ background: #82c91e; color: white; box-shadow: 0 0 20px #82c91e; }}
        .msg-wrong {{ background: #ff4b2b; color: white; box-shadow: 0 0 20px #ff4b2b; }}
        .show-msg {{ transform: translate(-50%, -50%) scale(1) !important; }}
        .shake {{ animation: shake 0.3s ease-in-out; }}
        @keyframes shake {{ 0%, 100% {{transform: translateX(0);}} 25% {{transform: translateX(-10px);}} 75% {{transform: translateX(10px);}} }}
        #canvas {{ position: absolute; top: 0; left: 0; pointer-events: none; }}
    </style>
</head>
<body>
<div class="game-card" id="card">
    <canvas id="canvas"></canvas>
    <div id="msg-overlay"></div>
    <h1 style="font-family: 'Arial Black'; margin:0; font-size: 24px;">ATOMIC ROW</h1>
    <p style="font-size:12px; opacity:0.8;">Level {st.session_state.lvl + 1}</p>
    <div class="tile-row" id="ans-row"></div>
    <div class="tile-row" id="pool-row"></div>
</div>

<script>
    let target = "{target_word}";
    let pool = target.split('').sort(() => Math.random() - 0.5);
    let answer = [];
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 340; canvas.height = 300;
    let particles = [];

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

        if(answer.length === target.length) {{
            const msg = document.getElementById('msg-overlay');
            if(answer.join('') === target) {{
                msg.innerText = "STABILIZED! ✨";
                msg.className = "msg-correct show-msg";
                createExplosion();
                // Send signal to Streamlit
                setTimeout(() => {{ window.parent.postMessage({{type: 'streamlit:setComponentValue', value: true}}, '*'); }}, 500);
            }} else {{
                msg.innerText = "UNSTABLE! ❌";
                msg.className = "msg-wrong show-msg";
                document.getElementById('card').classList.add('shake');
                setTimeout(() => {{ 
                    msg.classList.remove('show-msg'); 
                    document.getElementById('card').classList.remove('shake');
                    answer = []; pool = target.split('').sort(() => Math.random() - 0.5);
                    render();
                }}, 1500);
            }}
        }}
    }}

    function createExplosion() {{
        for(let i=0; i<40; i++) {{
            particles.push({{ x: 170, y: 150, vx: (Math.random()-0.5)*10, vy: (Math.random()-0.5)*10, color: `hsl(${{Math.random()*360}},70%,60%)`, s: Math.random()*4+2 }});
        }}
        animate();
    }}

    function animate() {{
        if(particles.length === 0) return;
        ctx.clearRect(0,0,340,300);
        particles.forEach((p,i) => {{
            p.x += p.vx; p.y += p.vy; p.vy += 0.2;
            ctx.fillStyle = p.color; ctx.beginPath(); ctx.arc(p.x,p.y,p.s,0,Math.PI*2); ctx.fill();
            if(p.y > 300) particles.splice(i,1);
        }});
        requestAnimationFrame(animate);
    }}

    function addLetter(i) {{ if(answer.length < target.length) {{ answer.push(pool.splice(i, 1)[0]); render(); }} }}
    function removeLetter(i) {{ pool.push(answer.splice(i, 1)[0]); render(); }}
    render();
</script>
</body>
</html>
"""

# 4. Render Game and Catch the Unlock Signal
# components.declare_component or simple return value handling
result = components.html(game_html, height=420)

# 5. THE DYNAMIC BUTTON
# If the game sends 'true', the Next Level button appears automatically
if st.button("🚀 PROCEED TO NEXT LEVEL", use_container_width=True):
    st.session_state.lvl += 1
    if st.session_state.lvl >= len(ELEMENTS):
        st.session_state.lvl = 0
    st.rerun()

# 6. HOW TO PLAY
st.markdown("""
<div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #ddd; margin-top:10px;">
    <h4 style="margin:0;">📖 Game Instructions:</h4>
    <p style="font-size: 14px;">• Unscramble the letters to stabilize the element.<br>
    • <b>Wrong:</b> The screen shakes and resets.<br>
    • <b>Right:</b> Particles explode and you can proceed!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777; font-size:10px; margin-top:20px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
