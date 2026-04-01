import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Row", layout="centered")

# 2. Level Data
ELEMENTS = ["NEON", "BORON", "OXYGEN", "SODIUM", "CARBON", "HELIUM", "SILICON", "LITHIUM", "SULPHUR", "CALCIUM", "MAGNESIUM", "ALUMINIUM"]

if 'lvl' not in st.session_state: st.session_state.lvl = 0

target_word = ELEMENTS[st.session_state.lvl]

# 3. THE GAME ENGINE (HTML + JS + NEW AUDIO)
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
            padding: 20px; border-radius: 25px; color: white; text-align: center;
            width: 100%; max-width: 340px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative;
        }}

        .tile-row {{ display: flex; flex-direction: row; justify-content: center; gap: 5px; margin: 10px 0; min-height: 45px; }}
        
        .tile {{
            width: 40px; height: 40px; background: #ffffff; color: #1a2a6c; border-radius: 8px;
            display: flex; align-items: center; justify-content: center; font-weight: 900;
            font-size: 16px; box-shadow: 0 4px 0 #bdc3c7; cursor: pointer;
        }}

        #msg-overlay {{
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%) scale(0);
            padding: 8px 20px; border-radius: 50px; font-weight: bold; font-size: 18px; z-index: 100;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); pointer-events: none;
        }}
        .msg-correct {{ background: #82c91e; color: white; box-shadow: 0 0 15px #82c91e; }}
        .msg-wrong {{ background: #ff4b2b; color: white; box-shadow: 0 0 15px #ff4b2b; }}
        .show-msg {{ transform: translateX(-50%) scale(1) !important; }}

        .shake {{ animation: shake 0.3s ease-in-out; }}
        @keyframes shake {{ 0%, 100% {{transform: translateX(0);}} 25% {{transform: translateX(-8px);}} 75% {{transform: translateX(8px);}} }}
        
        #canvas {{ position: absolute; top: 0; left: 0; pointer-events: none; }}
        
        .music-btn {{ background: rgba(255,255,255,0.2); border: 1px solid white; color: white; border-radius: 20px; padding: 5px 15px; font-size: 12px; cursor: pointer; margin-top:10px; }}
    </style>
</head>
<body>
<div class="game-card" id="card">
    <canvas id="canvas"></canvas>
    <div id="msg-overlay"></div>

    <h2 style="font-family: 'Arial Black'; margin:0; font-size: 20px;">ATOMIC ROW</h2>
    <p style="font-size:10px; opacity:0.8;">Element Challenge: Level {st.session_state.lvl + 1}</p>

    <div class="tile-row" id="ans-row"></div>
    <div style="font-size:9px; opacity:0.6; margin:5px 0;">POOL (TAP TO SELECT)</div>
    <div class="tile-row" id="pool-row"></div>

    <button class="music-btn" id="musicToggle" onclick="toggleMusic()">🎵 Theme: OFF</button>
</div>

<script>
    let target = "{target_word}";
    let pool = target.split('').sort(() => Math.random() - 0.5);
    let answer = [];
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 340; canvas.height = 300;
    let particles = [];
    
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    let themeLoop = null;

    function playTone(freq, type, dur, vol=0.1) {{
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = type; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        g.gain.setValueAtTime(vol, audioCtx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + dur);
        osc.connect(g); g.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + dur);
    }}

    function toggleMusic() {{
        const btn = document.getElementById('musicToggle');
        if(!themeLoop) {{
            themeLoop = audioCtx.createOscillator();
            const g = audioCtx.createGain();
            themeLoop.type = 'sine';
            themeLoop.frequency.setValueAtTime(150, audioCtx.currentTime);
            g.gain.setValueAtTime(0.02, audioCtx.currentTime);
            themeLoop.connect(g); g.connect(audioCtx.destination);
            themeLoop.start();
            btn.innerText = "🎵 Theme: ON";
        }} else {{
            themeLoop.stop(); themeLoop = null;
            btn.innerText = "🎵 Theme: OFF";
        }}
    }}

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
                playTone(440, 'sine', 0.4); playTone(880, 'sine', 0.6);
                createExplosion();
            }} else {{
                msg.innerText = "UNSTABLE! ❌";
                msg.className = "msg-wrong show-msg";
                playTone(100, 'square', 0.3);
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
        for(let i=0; i<30; i++) {{
            particles.push({{ x: 170, y: 80, vx: (Math.random()-0.5)*8, vy: (Math.random()-0.5)*8, color: '#82c91e', s: Math.random()*3+2 }});
        }}
        animate();
    }}

    function animate() {{
        if(particles.length === 0) return;
        ctx.clearRect(0,0,340,300);
        particles.forEach((p,i) => {{
            p.x += p.vx; p.y += p.vy; p.vy += 0.15;
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

# 4. Render Game
components.html(game_html, height=400)

# 5. THE STABLE UNLOCK (Manual Entry)
st.write("---")
verify_text = st.text_input("🔬 Enter Element to Stabilize:", placeholder="Solve puzzle above, then type here...")

if verify_text.upper() == target_word:
    if st.button("🚀 PROCEED TO NEXT LEVEL", use_container_width=True):
        st.session_state.lvl += 1
        if st.session_state.lvl >= len(ELEMENTS):
            st.session_state.lvl = 0
            st.balloons()
        st.rerun()
else:
    st.button("🔒 LEVEL LOCKED (Solve First)", disabled=True, use_container_width=True)

# 6. Instructions
st.markdown("""
<div style="background: #fdfdfd; padding: 15px; border-radius: 15px; border: 1px solid #eee; color: #333;">
    <h4 style="margin:0; color: #1a2a6c;">📖 Mission Briefing:</h4>
    <p style="font-size: 13px;">• Unscramble the element name in the card.<br>
    • When <b>STABILIZED</b>, type the element name in the box to unlock the next level.<br>
    • Toggle the music button for laboratory atmosphere.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777; font-size:10px; margin-top:20px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
