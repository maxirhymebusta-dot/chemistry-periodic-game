import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Quest: SS1 Edition", layout="centered")

# 2. SS1 Curriculum Element Database
# Data: (Atomic No, Mass No, Group, Period, Symbol, Description)
ELEMENTS_DB = {
    "NEON": (10, 20, 18, 2, "Ne", "A noble gas with a stable octet structure. It does not react because its outer shell is full."),
    "BORON": (5, 11, 13, 2, "B", "A metalloid used in heat-resistant glass. It has 3 electrons in its valence shell."),
    "OXYGEN": (8, 16, 16, 2, "O", "A non-metal essential for respiration. It is diatomic (O₂) and highly electronegative."),
    "SODIUM": (11, 23, 1, 3, "Na", "A highly reactive alkali metal. It is stored in oil to prevent reaction with air or moisture."),
    "CARBON": (6, 12, 14, 2, "C", "A non-metal that shows allotropy (Diamond and Graphite). It is the basis of organic chemistry."),
    "HELIUM": (2, 4, 18, 1, "He", "A noble gas with a duplet structure. It is used in weather balloons because it is very light."),
    "SILICON": (14, 28, 14, 3, "Si", "The second most abundant element in the Earth's crust. Used extensively in electronics."),
    "LITHIUM": (3, 7, 1, 2, "Li", "The lightest metal. It belongs to the Alkali Metal family in Group 1."),
    "SULPHUR": (16, 32, 16, 3, "S", "A yellow non-metal found in Group 16. It is used to vulcanize rubber and make matches."),
    "CHLORINE": (17, 35.5, 17, 3, "Cl", "A halogen gas. It is a strong oxidizing agent used in water treatment to kill germs."),
    "FLUORINE": (9, 19, 17, 2, "F", "The most reactive non-metal. It has the highest electronegativity on the periodic table."),
    "CALCIUM": (20, 40, 2, 4, "Ca", "An alkaline earth metal. It is vital for the formation of strong bones and teeth.")
}

ELEMENT_LIST = list(ELEMENTS_DB.keys())

# --- SESSION STATE ---
if 'lvl' not in st.session_state: st.session_state.lvl = 0
if 'lives' not in st.session_state: st.session_state.lives = 3
if 'game_over' not in st.session_state: st.session_state.game_over = False

# HIDE THE INTERNAL TRIGGER BUTTON
st.markdown("""
    <style>
    div[data-testid="stButton"] button:has(div:contains("💣")) {
        display: none !important;
        height: 0px !important;
        width: 0px !important;
        visibility: hidden !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("💣"):
    st.session_state.lives -= 1
    if st.session_state.lives <= 0:
        st.session_state.game_over = True
    st.rerun()

target_word = ELEMENT_LIST[st.session_state.lvl]

# 3. THE QUEST ENGINE (60s TIMER)
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
        #timer {{ color: #f1c40f; font-family: monospace; font-size: 18px; }}
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
        <span id="lives-display">❤️ × {st.session_state.lives}</span>
        <span id="timer">60</span>
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
    let timeLeft = 60;
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
        if(timeLeft <= 10) document.getElementById('timer').style.color = "#ff4757";
        
        if(timeLeft <= 0) {{
            timerActive = false;
            clearInterval(timerInterval);
            document.getElementById('msg-overlay').innerText = "TIME UP! ⏳";
            document.getElementById('msg-overlay').className = "msg-wrong show-msg";
            setTimeout(() => {{ 
                const btn = window.parent.document.querySelectorAll('button');
                for (let b of btn) if(b.innerText.includes("💣")) b.click();
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

        if(answer.length === target.length) {{
            const msg = document.getElementById('msg-overlay');
            if(answer.join('') === target) {{
                timerActive = false;
                msg.innerText = "STABILIZED! 🏆";
                msg.className = "msg-correct show-msg";
                playSound(523, 'sine', 0.4);
            }} else {{
                msg.innerText = "ERROR! 💀";
                msg.className = "msg-wrong show-msg";
                setTimeout(() => {{ 
                    msg.classList.remove('show-msg'); 
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

# 4. App Logic
if st.session_state.game_over:
    st.error("💀 GAME OVER! Your energy has fully depleted.")
    if st.button("♻️ RESTART SS1 CURRICULUM", use_container_width=True):
        st.session_state.lvl = 0
        st.session_state.lives = 3
        st.session_state.game_over = False
        st.rerun()
else:
    components.html(game_html, height=260)
    st.write("---")
    
    # 5. SS1 DATA SHEET
    verify_text = st.text_input("📜 Scroll of Truth:", placeholder="Type name to unlock SS1 notes...", label_visibility="collapsed")

    if verify_text.upper() == target_word:
        d = ELEMENTS_DB[target_word]
        st.markdown(f"""
        <div style="background: #ffffff; padding: 20px; border-radius: 15px; border: 2px solid #f39c12; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #333;">
            <div style="text-align: center; border-bottom: 2px solid #f39c12; margin-bottom: 15px;">
                <h2 style="margin: 0; color: #2c3e50;">{target_word}</h2>
                <span style="font-size: 40px; font-weight: bold; color: #f39c12;">{d[4]}</span>
            </div>
            <div style="display: flex; justify-content: space-around; font-size: 14px; margin-bottom: 15px;">
                <div style="text-align: center;"><b>Atomic Number (Z)</b><br><span style="font-size: 20px;">{d[0]}</span></div>
                <div style="text-align: center;"><b>Mass Number (A)</b><br><span style="font-size: 20px;">{d[1]}</span></div>
            </div>
            <div style="display: flex; justify-content: space-around; font-size: 14px; margin-bottom: 15px; background: #f9f9f9; padding: 10px; border-radius: 8px;">
                <div style="text-align: center;"><b>Group</b><br>{d[2]}</div>
                <div style="text-align: center;"><b>Period</b><br>{d[3]}</div>
            </div>
            <p style="font-size: 13px; line-height: 1.6; text-align: justify; color: #555;"><b>SS1 Curriculum Overview:</b> {d[5]}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 ADVANCE TO NEXT STAGE", use_container_width=True):
            st.session_state.lvl = (st.session_state.lvl + 1) % len(ELEMENT_LIST)
            st.rerun()
    else:
        st.button("🔒 PATH BLOCKED", disabled=True, use_container_width=True)

# 6. SS1 STUDENT GUIDE
st.markdown("---")
[attachment_0](attachment)
st.markdown("""
<div style="background: #2c3e50; padding: 20px; border-radius: 15px; border-left: 8px solid #f39c12; color: white;">
    <h3 style="margin-top:0; color: #f39c12;">🗺️ SS1 Quest Manual</h3>
    <div style="font-size: 14px; line-height: 1.6;">
        <p><b>1. Master the Symbols:</b> Use your SS1 chemistry knowledge to unscramble the element name within <b>60 seconds</b>.</p>
        <p><b>2. Life Management:</b> If the <b>💣</b> triggers (timer hits zero), you lose 1 Heart. Protect your 3 Hearts to reach the final element.</p>
        <p><b>3. Periodic Law:</b> Once you stabilize an element, check the <i>Scroll of Truth</i>. Study the <b>Atomic Number</b> (number of protons) and <b>Mass Number</b> (protons + neutrons) carefully.</p>
        <p><b>4. SS1 Exam Prep:</b> Focus on the <b>Group</b> (valence electrons) and <b>Period</b> (number of shells) to master the periodic table for your WAEC/NECO exams.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777; font-size:10px; margin-top:25px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
