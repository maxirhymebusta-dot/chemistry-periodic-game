import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Row", layout="centered")

# 2. Comprehensive Element Database
# Values are: (Atomic No, Mass No, Group, Period, Overview)
ELEMENTS_DB = {
    "NEON": (10, 20, 18, 2, "A noble gas used in bright signs. It is chemically inert and glows reddish-orange."),
    "BORON": (5, 11, 13, 2, "A metalloid used in fiberglass and pyrotechnics. Essential for plant growth."),
    "OXYGEN": (8, 16, 16, 2, "A highly reactive nonmetal. Vital for respiration and combustion."),
    "SODIUM": (11, 23, 1, 3, "A soft alkali metal. Highly reactive with water; found in common table salt."),
    "CARBON": (6, 12, 14, 2, "The basis of organic chemistry. Exists as graphite, diamond, and coal."),
    "HELIUM": (2, 4, 18, 1, "The second most abundant element. Used in balloons and cryogenics."),
    "SILICON": (14, 28, 14, 3, "A semiconductor used in computer chips and solar cells."),
    "LITHIUM": (3, 7, 1, 2, "Lightest metal. Crucial for high-density rechargeable batteries."),
    "SULPHUR": (16, 32, 16, 3, "A yellow nonmetal used in gunpowder, matches, and sulfuric acid."),
    "CHLORINE": (17, 35, 17, 3, "A toxic green gas used for water purification and disinfectants."),
    "FLUORINE": (9, 19, 17, 2, "The most electronegative element. Used in toothpaste and refrigerants."),
    "CALCIUM": (20, 40, 2, 4, "An alkaline earth metal vital for bones, teeth, and cellular functions.")
}

ELEMENT_LIST = list(ELEMENTS_DB.keys())

if 'lvl' not in st.session_state: st.session_state.lvl = 0

target_word = ELEMENT_LIST[st.session_state.lvl]

# 3. THE GAME ENGINE (Optimized for Mobile)
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Arial+Black&display=swap');
        body {{ font-family: sans-serif; margin: 0; padding: 5px; display: flex; flex-direction: column; align-items: center; background: transparent; overflow: hidden; }}
        .game-card {{
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            padding: 15px; border-radius: 20px; color: white; text-align: center;
            width: 100%; max-width: 340px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative;
        }}
        .tile-row {{ display: flex; flex-direction: row; justify-content: center; gap: 5px; margin: 8px 0; min-height: 42px; }}
        .tile {{
            width: 40px; height: 40px; background: #ffffff; color: #1a2a6c; border-radius: 8px;
            display: flex; align-items: center; justify-content: center; font-weight: 900;
            font-size: 16px; box-shadow: 0 4px 0 #bdc3c7; cursor: pointer; user-select: none;
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
        .music-btn {{ background: rgba(255,255,255,0.2); border: 1px solid white; color: white; border-radius: 20px; padding: 4px 12px; font-size: 11px; cursor: pointer; margin-top: 5px; }}
    </style>
</head>
<body>
<div class="game-card" id="card">
    <div id="msg-overlay"></div>
    <h2 style="font-family: 'Arial Black'; margin:0; font-size: 18px;">ATOMIC ROW</h2>
    <p style="font-size:10px; opacity:0.8;">Level {st.session_state.lvl + 1}</p>
    <div class="tile-row" id="ans-row"></div>
    <div style="font-size:9px; opacity:0.6; margin:2px 0;">LETTER POOL</div>
    <div class="tile-row" id="pool-row"></div>
    <button class="music-btn" id="musicToggle" onclick="toggleMusic()">🎵 Music: OFF</button>
</div>
<script>
    let target = "{target_word}";
    let pool = target.split('').sort(() => Math.random() - 0.5);
    let answer = [];
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    let musicNode = null;

    function playSound(freq, type, dur, vol=0.1) {{
        const osc = audioCtx.createOscillator(); const g = audioCtx.createGain();
        osc.type = type; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        g.gain.setValueAtTime(vol, audioCtx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + dur);
        osc.connect(g); g.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + dur);
    }}

    function toggleMusic() {{
        const btn = document.getElementById('musicToggle');
        if(!musicNode) {{
            musicNode = audioCtx.createGain(); musicNode.gain.value = 0.03;
            setInterval(() => {{
                if(musicNode) {{
                    const t = audioCtx.currentTime; const osc = audioCtx.createOscillator();
                    osc.type = 'triangle'; osc.frequency.setValueAtTime([110, 130, 165][Math.floor(t % 3)], t);
                    osc.connect(musicNode); musicNode.connect(audioCtx.destination);
                    osc.start(t); osc.stop(t + 0.5);
                }}
            }}, 500);
            btn.innerText = "🎵 Music: ON";
        }} else {{ musicNode.disconnect(); musicNode = null; btn.innerText = "🎵 Music: OFF"; }}
    }}

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        ansRow.innerHTML = ""; poolRow.innerHTML = "";
        for(let i=0; i<target.length; i++) {{
            let div = document.createElement('div'); div.className = 'tile';
            if(!answer[i]) div.style.background = "rgba(255,255,255,0.1)";
            div.innerText = answer[i] || "?";
            if(answer[i]) div.onclick = () => {{ playSound(800, 'sine', 0.1, 0.05); removeLetter(i); }};
            ansRow.appendChild(div);
        }}
        pool.forEach((char, i) => {{
            let div = document.createElement('div'); div.className = 'tile'; div.innerText = char;
            div.onclick = () => {{ playSound(800, 'sine', 0.1, 0.05); addLetter(i); }};
            poolRow.appendChild(div);
        }});
        if(answer.length === target.length) {{
            const msg = document.getElementById('msg-overlay');
            if(answer.join('') === target) {{
                msg.innerText = "STABILIZED! ✨"; msg.className = "msg-correct show-msg";
                playSound(523, 'sine', 0.4); playSound(659, 'sine', 0.5);
            }} else {{
                msg.innerText = "UNSTABLE! ❌"; msg.className = "msg-wrong show-msg";
                playSound(100, 'square', 0.3); document.getElementById('card').classList.add('shake');
                setTimeout(() => {{ 
                    msg.classList.remove('show-msg'); document.getElementById('card').classList.remove('shake');
                    answer = []; pool = target.split('').sort(() => Math.random() - 0.5); render();
                }}, 1200);
            }}
        }}
    }}
    function addLetter(i) {{ if(answer.length < target.length) {{ answer.push(pool.splice(i, 1)[0]); render(); }} }}
    function removeLetter(i) {{ pool.push(answer.splice(i, 1)[0]); render(); }}
    render();
</script>
</body>
</html>
"""

# 4. Render Game
components.html(game_html, height=280)

# 5. DATA SHEET & VERIFICATION
st.markdown("<div style='margin-top: -15px;'>", unsafe_allow_html=True)
verify_text = st.text_input("🔬 Verify Element to Unlock:", placeholder="Type name here...", label_visibility="collapsed")

if verify_text.upper() == target_word:
    data = ELEMENTS_DB[target_word]
    
    # Professional Data Sheet Table
    st.markdown(f"""
    <div style="background: white; padding: 15px; border-radius: 10px; border: 2px solid #82c91e; margin-bottom: 10px;">
        <h4 style="color: #1a2a6c; margin-top:0;">📊 {target_word} DATA SHEET</h4>
        <table style="width:100%; font-size:13px; text-align:left; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #eee;"><td><b>Atomic Number ($Z$):</b></td><td>{data[0]}</td></tr>
            <tr style="border-bottom: 1px solid #eee;"><td><b>Mass Number ($A$):</b></td><td>{data[1]}</td></tr>
            <tr style="border-bottom: 1px solid #eee;"><td><b>Group:</b></td><td>{data[2]}</td></tr>
            <tr style="border-bottom: 1px solid #eee;"><td><b>Period:</b></td><td>{data[3]}</td></tr>
        </table>
        <p style="font-size: 13px; color: #555; margin-top:10px;"><b>Overview:</b> {data[4]}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 PROCEED TO NEXT LEVEL", use_container_width=True):
        st.session_state.lvl = (st.session_state.lvl + 1) % len(ELEMENT_LIST)
        st.rerun()
else:
    st.button("🔒 LEVEL LOCKED", disabled=True, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# 6. HOW TO PLAY (REWRITTEN & POLISHED)
st.markdown("---")
st.markdown("""
<div style="background: #ffffff; padding: 18px; border-radius: 15px; border-left: 6px solid #1a2a6c; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <h3 style="margin-top:0; color: #1a2a6c; font-family: sans-serif; display: flex; align-items: center;">
        <span style="font-size: 24px; margin-right: 10px;">📖</span> How to Play
    </h3>
    <p style="font-size: 14px; color: #333; line-height: 1.5;">
        Welcome to the Atomic Lab. Follow these steps to complete your mission:
    </p>
    <ul style="font-size: 14px; color: #444; padding-left: 20px;">
        <li style="margin-bottom: 8px;"><b>1. Assemble:</b> Tap letters in the <b>Letter Pool</b> to fill the empty atomic slots at the top.</li>
        <li style="margin-bottom: 8px;"><b>2. Edit:</b> If you make a mistake, tap a letter already in the <b>Atomic Slot</b> to return it to the pool.</li>
        <li style="margin-bottom: 8px;"><b>3. Stabilize:</b> Once the correct element is spelled, the <b>STABILIZED</b> alert will trigger.</li>
        <li style="margin-bottom: 8px;"><b>4. Discovery:</b> Type the element name into the verification box to generate its <b>Scientific Data Sheet</b> and unlock the next level.</li>
    </ul>
    <p style="font-size: 12px; color: #1a2a6c; font-weight: bold; background: #eef2ff; padding: 8px; border-radius: 5px; text-align: center;">
        PRO TIP: Activate the 🎵 Theme for an immersive laboratory vibe!
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777; font-size:10px; margin-top:25px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
