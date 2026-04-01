import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Quest", layout="centered")

# 2. Comprehensive Element Database
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

# 3. THE QUEST ENGINE (ADVENTURE AUDIO + APPLAUSE)
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Arial+Black&display=swap');
        body {{ font-family: sans-serif; margin: 0; padding: 5px; display: flex; flex-direction: column; align-items: center; background: transparent; overflow: hidden; }}
        .game-card {{
            background: linear-gradient(135deg, #2c3e50, #000000);
            padding: 15px; border-radius: 20px; color: white; text-align: center;
            width: 100%; max-width: 340px; box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            border: 2px solid #f39c12; position: relative;
        }}
        .tile-row {{ display: flex; flex-direction: row; justify-content: center; gap: 5px; margin: 8px 0; min-height: 42px; }}
        .tile {{
            width: 40px; height: 40px; background: #f39c12; color: #fff; border-radius: 5px;
            display: flex; align-items: center; justify-content: center; font-weight: 900;
            font-size: 16px; box-shadow: 0 4px 0 #d35400; cursor: pointer; user-select: none;
        }}
        #msg-overlay {{
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%) scale(0);
            padding: 8px 20px; border-radius: 50px; font-weight: bold; font-size: 18px; z-index: 100;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); pointer-events: none;
        }}
        .msg-correct {{ background: #f1c40f; color: #000; box-shadow: 0 0 15px #f1c40f; }}
        .msg-wrong {{ background: #e74c3c; color: white; box-shadow: 0 0 15px #e74c3c; }}
        .show-msg {{ transform: translateX(-50%) scale(1) !important; }}
        .shake {{ animation: shake 0.3s ease-in-out; }}
        @keyframes shake {{ 0%, 100% {{transform: translateX(0);}} 25% {{transform: translateX(-8px);}} 75% {{transform: translateX(8px);}} }}
        .music-btn {{ background: rgba(0,0,0,0.5); border: 1px solid #f39c12; color: #f39c12; border-radius: 20px; padding: 5px 15px; font-size: 11px; font-weight:bold; cursor: pointer; margin-top: 5px; }}
    </style>
</head>
<body>
<div class="game-card" id="card">
    <div id="msg-overlay"></div>
    <h2 style="font-family: 'Arial Black'; margin:0; font-size: 18px; color:#f39c12;">ATOMIC QUEST</h2>
    <p style="font-size:10px; opacity:0.8;">Stage {st.session_state.lvl + 1}</p>
    <div class="tile-row" id="ans-row"></div>
    <div style="font-size:9px; opacity:0.6; margin:2px 0;">INVENTORY</div>
    <div class="tile-row" id="pool-row"></div>
    <button class="music-btn" id="musicToggle" onclick="toggleMusic()">⚔️ QUEST THEME: OFF</button>
</div>

<script>
    let target = "{target_word}";
    let pool = target.split('').sort(() => Math.random() - 0.5);
    let answer = [];
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    let musicInterval = null;

    function playSound(freq, type, dur, vol=0.1) {{
        if(audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator(); const g = audioCtx.createGain();
        osc.type = type; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        g.gain.setValueAtTime(vol, audioCtx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + dur);
        osc.connect(g); g.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + dur);
    }}

    function playApplause() {{
        // Synthesized applause sound using white noise bursts
        const dur = 1.5;
        for (let i = 0; i < 15; i++) {{
            const t = audioCtx.currentTime + (Math.random() * 0.5);
            const bufferSize = audioCtx.sampleRate * 0.2;
            const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let j = 0; j < bufferSize; j++) data[j] = Math.random() * 2 - 1;
            const source = audioCtx.createBufferSource();
            const filter = audioCtx.createBiquadFilter();
            const gain = audioCtx.createGain();
            source.buffer = buffer;
            filter.type = 'bandpass'; filter.frequency.value = 1000 + (Math.random() * 2000);
            gain.gain.setValueAtTime(0.05, t);
            gain.gain.exponentialRampToValueAtTime(0.001, t + 0.4);
            source.connect(filter); filter.connect(gain); gain.connect(audioCtx.destination);
            source.start(t);
        }}
    }}

    function toggleMusic() {{
        const btn = document.getElementById('musicToggle');
        if(!musicInterval) {{
            btn.innerText = "⚔️ QUEST THEME: ON";
            musicInterval = setInterval(() => {{
                const t = audioCtx.currentTime;
                // Adventure march bassline
                playSound(82, 'triangle', 0.4, 0.04);
                setTimeout(() => playSound(110, 'triangle', 0.2, 0.03), 200);
                setTimeout(() => playSound(123, 'triangle', 0.2, 0.03), 400);
            }}, 1000);
        } else {{
            clearInterval(musicInterval); musicInterval = null;
            btn.innerText = "⚔️ QUEST THEME: OFF";
        }}
    }}

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        ansRow.innerHTML = ""; poolRow.innerHTML = "";
        for(let i=0; i<target.length; i++) {{
            let div = document.createElement('div'); div.className = 'tile';
            if(!answer[i]) div.style.background = "rgba(255,255,255,0.05)";
            div.innerText = answer[i] || "?";
            if(answer[i]) div.onclick = () => {{ playSound(200, 'sine', 0.1, 0.05); removeLetter(i); }};
            ansRow.appendChild(div);
        }}
        pool.forEach((char, i) => {{
            let div = document.createElement('div'); div.className = 'tile'; div.innerText = char;
            div.onclick = () => {{ playSound(200, 'sine', 0.1, 0.05); addLetter(i); }};
            poolRow.appendChild(div);
        }});
        if(answer.length === target.length) {{
            const msg = document.getElementById('msg-overlay');
            if(answer.join('') === target) {{
                msg.innerText = "QUEST COMPLETE! 🏆"; msg.className = "msg-correct show-msg";
                playApplause();
            }} else {{
                msg.innerText = "DEFEATED! 💀"; msg.className = "msg-wrong show-msg";
                playSound(150, 'sawtooth', 0.3); document.getElementById('card').classList.add('shake');
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
components.html(game_html, height=290)

# 5. DATA SHEET & VERIFICATION
st.markdown("<div style='margin-top: -15px;'>", unsafe_allow_html=True)
verify_text = st.text_input("📜 Scroll of Truth (Type name to unlock):", placeholder="Enter name...", label_visibility="collapsed")

if verify_text.upper() == target_word:
    data = ELEMENTS_DB[target_word]
    st.markdown(f"""
    <div style="background: #fff; padding: 15px; border-radius: 10px; border: 2px solid #f39c12; margin-bottom: 10px;">
        <h4 style="color: #2c3e50; margin-top:0;">🛡️ {target_word} KNOWLEDGE SCROLL</h4>
        <table style="width:100%; font-size:13px; text-align:left;">
            <tr style="border-bottom: 1px solid #eee;"><td><b>Atomic No:</b></td><td>{data[0]}</td></tr>
            <tr style="border-bottom: 1px solid #eee;"><td><b>Mass No:</b></td><td>{data[1]}</td></tr>
            <tr style="border-bottom: 1px solid #eee;"><td><b>Group:</b></td><td>{data[2]}</td></tr>
            <tr style="border-bottom: 1px solid #eee;"><td><b>Period:</b></td><td>{data[3]}</td></tr>
        </table>
        <p style="font-size: 13px; color: #555; margin-top:10px;"><b>Lore:</b> {data[4]}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 ADVANCE TO NEXT STAGE", use_container_width=True):
        st.session_state.lvl = (st.session_state.lvl + 1) % len(ELEMENT_LIST)
        st.rerun()
else:
    st.button("🔒 PATH BLOCKED", disabled=True, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# 6. ENHANCED HOW TO PLAY (ADVENTURE STYLE)
st.markdown("---")
st.markdown("""
<div style="background: #2c3e50; padding: 18px; border-radius: 15px; border-left: 6px solid #f39c12; color: white;">
    <h3 style="margin-top:0; color: #f39c12;">🗺️ Quest Guide</h3>
    <p style="font-size: 14px; line-height: 1.5;">
        Brave Alchemist, you must restore the elements of the Periodic Table to their true form.
    </p>
    <ul style="font-size: 14px; padding-left: 20px;">
        <li style="margin-bottom: 8px;"><b>Loot Letters:</b> Tap letters in your Inventory to place them in the Quest Slots.</li>
        <li style="margin-bottom: 8px;"><b>Rearrange:</b> Tap a misplaced letter in the slots to send it back to your Inventory.</li>
        <li style="margin-bottom: 8px;"><b>Victory:</b> Spell the element correctly to receive the <b>Quest Complete</b> applause.</li>
        <li style="margin-bottom: 8px;"><b>Scroll of Truth:</b> Enter the name into the scroll below to unlock the hidden lore and move to the next stage.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777; font-size:10px; margin-top:25px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
