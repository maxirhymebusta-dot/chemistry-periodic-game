import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Quest: Elite", layout="centered")

# 2. Comprehensive Element Database
# Data: (Atomic No, Mass No, Group, Period, Overview)
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

# --- GAME STATE ---
if 'lvl' not in st.session_state: st.session_state.lvl = 0
if 'lives' not in st.session_state: st.session_state.lives = 3

# Life Loss Logic
params = st.query_params
if params.get("lose_life") == "true":
    st.session_state.lives -= 1
    st.query_params.clear()
    if st.session_state.lives <= 0:
        st.session_state.lvl = 0
        st.session_state.lives = 3
        st.error("💀 ALL LIVES LOST! Restarting from Level 1...")
    st.rerun()

target_word = ELEMENT_LIST[st.session_state.lvl]

# 3. THE QUEST ENGINE (15s TIMER)
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
        .stats-bar {{ display: flex; justify-content: space-between; width: 100%; margin-bottom: 5px; font-weight: bold; font-size: 14px; }}
        #timer {{ color: #ff4757; font-family: monospace; font-size: 18px; }}
        .lives-text {{ color: #ff4757; }}
        .tile-row {{ display: flex; flex-direction: row; justify-content: center; gap: 5px; margin: 8px 0; min-height: 40px; }}
        .tile {{
            width: 38px; height: 38px; background: #f39c12; color: #fff; border-radius: 5px;
            display: flex; align-items: center; justify-content: center; font-weight: 900;
            font-size: 14px; box-shadow: 0 4px 0 #d35400; cursor: pointer;
        }}
        #msg-overlay {{
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%) scale(0);
            padding: 8px 15px; border-radius: 50px; font-weight: bold; font-size: 18px; z-index: 100;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); pointer-events: none;
        }}
        .msg-correct {{ background: #f1c40f; color: #000; }}
        .msg-wrong {{ background: #e74c3c; color: white; }}
        .show-msg {{ transform: translateX(-50%) scale(1) !important; }}
    </style>
</head>
<body>
<div class="game-card" id="card">
    <div id="msg-overlay"></div>
    <div class="stats-bar">
        <span class="lives-text">❤️ × {st.session_state.lives}</span>
        <span id="timer">15</span>
    </div>
    <h2 style="font-family: 'Arial Black'; margin:0; font-size: 18px; color:#f39c12;">ATOMIC QUEST</h2>
    
    <div class="tile-row" id="ans-row"></div>
    <div style="font-size:9px; opacity:0.6; margin:2px 0;">INVENTORY</div>
    <div class="tile-row" id="pool-row"></div>
</div>

<script>
    let target = "{target_word}";
    let pool = target.split('').sort(() => Math.random() - 0.5);
    let answer = [];
    let timeLeft = 15;
    let timerActive = true;
    
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playSound(freq, type, dur, vol=0.1) {{
        if(audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator(); const g = audioCtx.createGain();
        osc.type = type; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        g.gain.setValueAtTime(vol, audioCtx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + dur);
        osc.connect(g); g.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + dur);
    }}

    const timerInterval = setInterval(() => {{
        if(!timerActive) return;
        timeLeft--;
        document.getElementById('timer').innerText = timeLeft;
        if(timeLeft <= 5) playSound(400, 'sine', 0.1, 0.05);
        
        if(timeLeft <= 0) {{
            timerActive = false;
            clearInterval(timerInterval);
            window.parent.location.href = window.parent.location.pathname + "?lose_life=true";
        }}
    }}, 1000);

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        ansRow.innerHTML = ""; poolRow.innerHTML = "";
        
        for(let i=0; i<target.length; i++) {{
            let div = document.createElement('div'); div.className = 'tile';
            if(!answer[i]) div.style.background = "rgba(255,255,255,0.05)";
            div.innerText = answer[i] || "?";
            if(answer[i] && timerActive) div.onclick = () => {{ playSound(200, 'sine', 0.1, 0.1); removeLetter(i); }};
            ansRow.appendChild(div);
        }}
        
        pool.forEach((char, i) => {{
            let div = document.createElement('div'); div.className = 'tile'; div.innerText = char;
            if(timerActive) div.onclick = () => {{ playSound(200, 'sine', 0.1, 0.1); addLetter(i); }};
            poolRow.appendChild(div);
        }});

        if(answer.length === target.length) {{
            const msg = document.getElementById('msg-overlay');
            if(answer.join('') === target) {{
                timerActive = false;
                msg.innerText = "STABILIZED! 🏆";
                msg.className = "msg-correct show-msg";
                playSound(523, 'sine', 0.4, 0.1);
                setTimeout(() => {{ msg.classList.remove('show-msg'); }}, 1000);
            }} else {{
                msg.innerText = "ERROR! 💀";
                msg.className = "msg-wrong show-msg";
                playSound(150, 'sawtooth', 0.3, 0.1);
                setTimeout(() => {{ 
                    msg.classList.remove('show-msg'); 
                    answer = []; pool = target.split('').sort(() => Math.random() - 0.5); render();
                }}, 800);
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
components.html(game_html, height=260)

# 5. DETAILED DATA SHEET
st.markdown("<div style='margin-top: -15px;'>", unsafe_allow_html=True)
verify_text = st.text_input("📜 Scroll of Truth:", placeholder="Type name to reveal knowledge...", label_visibility="collapsed")

if verify_text.upper() == target_word:
    data = ELEMENTS_DB[target_word]
    st.markdown(f"""
    <div style="background: #fff; padding: 15px; border-radius: 12px; border: 2px solid #f39c12; color: #222; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <h3 style="color: #2c3e50; margin: 0 0 10px 0; text-align: center; border-bottom: 2px solid #f39c12;">🛡️ {target_word} SCIENTIFIC DATA</h3>
        
        <p style="font-size: 14px; margin: 5px 0;"><b>Atomic Number ($Z$): {data[0]}</b><br>
        <span style="font-size: 12px; color: #666;">This represents the number of protons in the nucleus. It defines the element's identity.</span></p>
        
        <p style="font-size: 14px; margin: 5px 0;"><b>Mass Number ($A$): {data[1]}</b><br>
        <span style="font-size: 12px; color: #666;">The total sum of protons and neutrons. It determines the weight of the atom.</span></p>
        
        <p style="font-size: 14px; margin: 5px 0;"><b>Group: {data[2]} | Period: {data[3]}</b><br>
        <span style="font-size: 12px; color: #666;">Group {data[2]} indicates chemical behavior; Period {data[3]} shows the number of electron shells.</span></p>
        
        <p style="font-size: 13px; color: #1a2a6c; border-top: 1px solid #eee; padding-top: 8px; margin-top: 8px;"><b>Scientific Lore:</b> {data[4]}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 ADVANCE TO NEXT STAGE", use_container_width=True):
        st.session_state.lvl = (st.session_state.lvl + 1) % len(ELEMENT_LIST)
        st.rerun()
else:
    st.button("🔒 PATH BLOCKED", disabled=True, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# 6. HOW TO PLAY (QUEST MANUAL)
st.markdown("---")
st.markdown("""
### 📖 How to Play (Quest Manual)

1. **Unscramble:** Tap the gold letters in your **Inventory** to fill the empty slots within **15 seconds**.
2. **Modify:** Tap a letter in the top slots if you need to send it back to the pool.
3. **The Penalty:** If the timer hits **0**, you lose **1 Heart (❤️)**. Lose all 3, and you fall back to Level 1.
4. **Knowledge Lock:** Once you see "STABILIZED," type the element's name into the **Scroll of Truth** below.
5. **Learn:** Read the **Scientific Data** that appears to understand the element's Atomic Structure ($Z$ and $A$), position, and real-world use.
6. **Advance:** Click "Advance" to move to the next stage of your quest!
""")

st.markdown("<p style='text-align: center; color: #777; font-size:10px; margin-top:20px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
