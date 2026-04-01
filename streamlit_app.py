import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Quest: Stable", layout="centered")

# 2. Element Database
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

# --- SESSION STATE ---
if 'lvl' not in st.session_state: st.session_state.lvl = 0
if 'lives' not in st.session_state: st.session_state.lives = 3
if 'game_over' not in st.session_state: st.session_state.game_over = False

target_word = ELEMENT_LIST[st.session_state.lvl]

# 3. THE QUEST ENGINE
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
        .msg-correct {{ background: #f1c40f; color: #000; box-shadow: 0 0 15px #f1c40f; }}
        .msg-wrong {{ background: #e74c3c; color: white; box-shadow: 0 0 15px #e74c3c; }}
        .show-msg {{ transform: translateX(-50%) scale(1) !important; }}
        .shake {{ animation: shake 0.3s ease-in-out; }}
        @keyframes shake {{ 0%, 100% {{transform: translateX(0);}} 25% {{transform: translateX(-8px);}} 75% {{transform: translateX(8px);}} }}
    </style>
</head>
<body>
<div class="game-card" id="card">
    <div id="msg-overlay"></div>
    <div class="stats-bar">
        <span id="lives-display">❤️ × {st.session_state.lives}</span>
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

    function playSound(f, t, d, v=0.1) {{
        const o = audioCtx.createOscillator(); const g = audioCtx.createGain();
        o.type = t; o.frequency.setValueAtTime(f, audioCtx.currentTime);
        g.gain.setValueAtTime(v, audioCtx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + d);
        o.connect(g); g.connect(audioCtx.destination);
        o.start(); o.stop(audioCtx.currentTime + d);
    }}

    const timerInterval = setInterval(() => {{
        if(!timerActive) return;
        timeLeft--;
        document.getElementById('timer').innerText = timeLeft;
        if(timeLeft <= 0) {{
            timerActive = false;
            clearInterval(timerInterval);
            document.getElementById('msg-overlay').innerText = "TIME EXPIRED! ⏳";
            document.getElementById('msg-overlay').className = "msg-wrong show-msg";
            setTimeout(() => {{ 
                const btn = window.parent.document.querySelectorAll('button');
                for (let b of btn) if(b.innerText.includes("INTERNAL_REDUCE")) b.click();
            }}, 1000);
        }}
    }}, 1000);

    function render() {{
        const ansRow = document.getElementById('ans-row');
        const poolRow = document.getElementById('pool-row');
        ansRow.innerHTML = ""; poolRow.innerHTML = "";
        
        for(let i=0; i<target.length; i++) {{
            let d = document.createElement('div'); d.className = 'tile';
            if(!answer[i]) d.style.background = "rgba(255,255,255,0.05)";
            d.innerText = answer[i] || "?";
            if(answer[i] && timerActive) d.onclick = () => {{ playSound(200, 'sine', 0.1); removeLetter(i); }};
            ansRow.appendChild(d);
        }}
        
        pool.forEach((char, i) => {{
            let d = document.createElement('div'); d.className = 'tile'; d.innerText = char;
            if(timerActive) d.onclick = () => {{ playSound(200, 'sine', 0.1); addLetter(i); }};
            poolRow.appendChild(d);
        }});

        // IMMEDIATE CHECK LOGIC
        if(answer.length === target.length) {{
            const msg = document.getElementById('msg-overlay');
            if(answer.join('') === target) {{
                timerActive = false;
                msg.innerText = "STABILIZED! 🏆";
                msg.className = "msg-correct show-msg";
                playSound(523, 'sine', 0.4);
            }} else {{
                // WRONG POPUP SHOWS IMMEDIATELY
                msg.innerText = "ERROR! 💀";
                msg.className = "msg-wrong show-msg";
                document.getElementById('card').classList.add('shake');
                playSound(100, 'sawtooth', 0.3, 0.2);
                
                setTimeout(() => {{ 
                    msg.classList.remove('show-msg'); 
                    document.getElementById('card').classList.remove('shake');
                    // Reset slots so they can try again quickly
                    answer.forEach(char => pool.push(char));
                    answer = [];
                    render();
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

# --- HIDDEN LIFE HANDLER ---
st.markdown("<style>div[data-testid='stButton'] button:has(div:contains('INTERNAL_REDUCE')) { display: none; }</style>", unsafe_allow_html=True)
if st.button("INTERNAL_REDUCE"):
    st.session_state.lives -= 1
    if st.session_state.lives <= 0:
        st.session_state.game_over = True
    st.rerun()

# 4. Main App Logic
if st.session_state.game_over:
    st.error("💀 ALL HEARTS LOST! Your journey ends here.")
    if st.button("♻️ RESTART FROM LEVEL 1", use_container_width=True):
        st.session_state.lvl = 0
        st.session_state.lives = 3
        st.session_state.game_over = False
        st.rerun()
else:
    components.html(game_html, height=260)
    st.write("---")
    
    # 5. DATA SHEET
    verify_text = st.text_input("📜 Scroll of Truth:", placeholder="Enter name to reveal knowledge...", label_visibility="collapsed")

    if verify_text.upper() == target_word:
        d = ELEMENTS_DB[target_word]
        st.markdown(f"""
        <div style="background: #fff; padding: 15px; border-radius: 12px; border: 2px solid #f39c12; color: #222;">
            <h3 style="color: #2c3e50; margin: 0 0 10px 0; text-align: center;">🛡️ {target_word} DATA</h3>
            <p style="font-size: 14px; margin: 4px 0;"><b>Atomic No:</b> {d[0]} | <b>Mass No:</b> {d[1]}</p>
            <p style="font-size: 13px; color: #555; border-top: 1px solid #eee; padding-top: 5px;"><b>Lore:</b> {d[4]}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 ADVANCE TO NEXT STAGE", use_container_width=True):
            st.session_state.lvl = (st.session_state.lvl + 1) % len(ELEMENT_LIST)
            st.rerun()
    else:
        st.button("🔒 PATH BLOCKED", disabled=True, use_container_width=True)

# 6. HOW TO PLAY
st.markdown("""
---
### 📖 How to Play
1. **Unscramble:** Tap letters in the inventory to fill the slots.
2. **Speed:** You have **15 seconds** per element.
3. **Wrong Answers:** If you fill the slots incorrectly, the card will shake and show **ERROR!**. Your letters will return to your inventory so you can try again.
4. **Game Over:** If the timer hits zero, you lose a heart. Lose all three, and the game resets to Level 1.
""")
