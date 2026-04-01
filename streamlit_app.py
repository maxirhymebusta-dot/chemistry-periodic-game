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

# 3. THE GAME ENGINE (HTML + JAVASCRIPT + PARTICLES)
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
            overflow: hidden;
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
            position: relative;
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

        /* SUCCESS POPUP */
        #success-msg {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            background: #82c91e;
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 20px;
            box-shadow: 0 0 20px rgba(130, 201, 30, 0.6);
            z-index: 100;
            transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            pointer-events: none;
        }}

        .show-success {{ transform: translate(-50%, -50%) scale(1) !important; }}

        /* PARTICLE CANVAS */
        #canvas {{
            position: absolute;
            top: 0; left: 0;
            pointer-events: none;
        }}

        .label {{ font-size: 12px; font-weight: bold; letter-spacing: 2px; color: #eee; margin-top: 15px; }}
        .btn-reset {{
            margin-top: 20px;
            padding: 8px 15px;
            background: rgba(255,255,255,0.1);
            border: 1px solid white;
            color: white;
            border-radius: 10px;
            font-size: 12px;
            cursor: pointer;
        }}
    </style>
</head>
<body>

<div class="game-card" id="card">
    <canvas id="canvas"></canvas>
    <div id="success-msg">CORRECT! ✨</div>

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

    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 350;
    canvas.height = 400;

    let particles = [];

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        ansRow.innerHTML = "";
        poolRow.innerHTML = "";

        // Render Answer
        for(let i=0; i<target.length; i++) {{
            let div = document.createElement('div');
            if(answer[i]) {{
                div.className = 'tile';
                div.innerText = answer[i];
                div.onclick = () => removeLetter(i);
            }} else {{
                div.className = 'tile empty-tile';
                div.innerText = "?";
            }}
            ansRow.appendChild(div);
        }}

        // Render Pool
        pool.forEach((char, i) => {{
            let div = document.createElement('div');
            div.className = 'tile';
            div.innerText = char;
            div.onclick = () => addLetter(i);
            poolRow.appendChild(div);
        }});

        if(answer.join('') === target) {{
            document.getElementById('success-msg').classList.add('show-success');
            createExplosion();
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
        document.getElementById('success-msg').classList.remove('show-success');
        render();
    }}

    // Particle Logic
    function createExplosion() {{
        for(let i=0; i<50; i++) {{
            particles.push({{
                x: canvas.width / 2,
                y: canvas.height / 2,
                vx: (Math.random() - 0.5) * 10,
                vy: (Math.random() - 0.5) * 10,
                color: `hsl(${{Math.random() * 360}}, 70%, 60%)`,
                size: Math.random() * 5 + 2
            }});
        }}
        animate();
    }}

    function animate() {{
        if(particles.length === 0) return;
        ctx.clearRect(0,0, canvas.width, canvas.height);
        particles.forEach((p, i) => {{
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.1; // gravity
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
            ctx.fill();
            if(p.y > canvas.height) particles.splice(i, 1);
        }});
        requestAnimationFrame(animate);
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
