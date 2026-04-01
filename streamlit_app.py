import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Scramble", layout="centered")

# 2. COMPLETE FIRST 20 ELEMENTS DATABASE
ELEMENTS_DB = {
    "HYDROGEN": (1, 1, 1, 1, "H", "The lightest element. It is flammable and usually exists as a diatomic gas (H2)."),
    "HELIUM": (2, 4, 18, 1, "He", "A noble gas with a duplet structure. Non-reactive and used in weather balloons."),
    "LITHIUM": (3, 7, 1, 2, "Li", "The lightest metal. An alkali metal used in high-performance batteries."),
    "BERYLLIUM": (4, 9, 2, 2, "Be", "A hard, grey alkaline earth metal used in alloys for aircraft and spacecraft."),
    "BORON": (5, 11, 13, 2, "B", "A metalloid used in heat-resistant glass (Pyrex). It has 3 valence electrons."),
    "CARBON": (6, 12, 14, 2, "C", "A non-metal that shows allotropy (Diamond/Graphite). The basis of life."),
    "NITROGEN": (7, 14, 15, 2, "N", "Makes up 78% of the atmosphere. Used in the production of fertilizers."),
    "OXYGEN": (8, 16, 16, 2, "O", "Essential for respiration and combustion. It is a diatomic non-metal."),
    "FLUORINE": (9, 19, 17, 2, "F", "The most electronegative and reactive non-metal. Used in toothpaste."),
    "NEON": (10, 20, 18, 2, "Ne", "A noble gas with a stable octet. Used in bright reddish-orange neon signs."),
    "SODIUM": (11, 23, 1, 3, "Na", "A soft alkali metal. Highly reactive with water; stored under paraffin oil."),
    "MAGNESIUM": (12, 24, 2, 3, "Mg", "Burns with a brilliant white flame. Used in fireworks and flashbulbs."),
    "ALUMINIUM": (13, 27, 13, 3, "Al", "A lightweight metal that does not corrode easily. Used for kitchen foil."),
    "SILICON": (14, 28, 14, 3, "Si", "A metalloid used as a semiconductor in computer chips and solar cells."),
    "PHOSPHORUS": (15, 31, 15, 3, "P", "A reactive non-metal used in the manufacture of matches and fertilizers."),
    "SULPHUR": (16, 32, 16, 3, "S", "A yellow non-metal used to vulcanize rubber and produce sulphuric acid."),
    "CHLORINE": (17, 35.5, 17, 3, "Cl", "A greenish-yellow poisonous halogen gas used to disinfect water."),
    "ARGON": (18, 40, 18, 3, "Ar", "A noble gas used in electric light bulbs to prevent the filament from burning."),
    "POTASSIUM": (19, 39, 1, 4, "K", "A very reactive alkali metal. Its compounds are vital for plant growth."),
    "CALCIUM": (20, 40, 2, 4, "Ca", "An alkaline earth metal essential for building strong bones and teeth.")
}

ELEMENT_LIST = list(ELEMENTS_DB.keys())

# --- SESSION STATE MANAGEMENT ---
if 'lvl' not in st.session_state: st.session_state.lvl = 0
if 'lives' not in st.session_state: st.session_state.lives = 3
if 'game_over' not in st.session_state: st.session_state.game_over = False

# HIDE INTERNAL TRIGGER BUTTONS
st.markdown("""
    <style>
    div[data-testid="stButton"] button:has(div:contains("💣")),
    div[data-testid="stButton"] button:has(div:contains("💖")) {
        display: none !important;
        height: 0px !important;
        width: 0px !important;
        visibility: hidden !important;
    }
    </style>
""", unsafe_allow_html=True)

# Penalty Trigger
if st.button("💣"):
    st.session_state.lives -= 1
    if st.session_state.lives <= 0:
        st.session_state.game_over = True
    st.rerun()

# Bonus Trigger
if st.button("💖"):
    st.session_state.lives += 2
    st.rerun()

target_word = ELEMENT_LIST[st.session_state.lvl]

# 3. THE GAME ENGINE
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
        .tile-row {{ display: flex; flex-direction: row; justify-content: center; gap: 5px; margin: 8px 0; min-height: 40px; }}
        .tile {{
            width: 38px; height: 38px; background: #f39c12; color: #fff; border-radius: 5px;
            display: flex; align-items: center; justify-content: center; font-weight: 900;
            font-size: 14px; box-shadow: 0 4px 0 #d35400; cursor: pointer;
        }}
        #msg-overlay {{
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%) scale(0);
            padding: 8px 15px; border-radius: 50px; font-weight: bold; font-size: 18px; z-index: 100;
            transition: 0.15s ease-in-out; pointer-events: none;
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
    <h2 style="font-family: 'Arial Black'; margin:0; font-size: 18px; color:#f39c12;">ATOMIC SCRAMBLE</h2>
    <p style="font-size: 10px; opacity:0.6;">STAGE {st.session_state.lvl + 1} OF 20</p>
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

    function triggerPython(icon) {{
        const btn = window.parent.document.querySelectorAll('button');
        for (let b of btn) if(b.innerText.includes(icon)) b.click();
    }}

    const timerInterval = setInterval(() => {{
        if(!timerActive) return;
        timeLeft--;
        document.getElementById('timer').innerText = timeLeft;
        if(timeLeft <= 0) {{
            timerActive = false;
            clearInterval(timerInterval);
            triggerPython("💣");
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
            if(answer[i] && timerActive) d.onclick = () => removeLetter(i);
            ansRow.appendChild(d);
        }}
        pool.forEach((char, i) => {{
            let d = document.createElement('div'); d.className = 'tile'; d.innerText = char;
            if(timerActive) d.onclick = () => addLetter(i);
            poolRow.appendChild(d);
        }});

        if(answer.length === target.length) {{
            const msg = document.getElementById('msg-overlay');
            if(answer.join('') === target) {{
                timerActive = false;
                msg.innerText = "+2 ❤️ BONUS!";
                msg.className = "msg-correct show-msg";
                setTimeout(() => {{ triggerPython("💖"); }}, 600);
            }} else {{
                msg.innerText = "-1 ❤️ PENALTY!";
                msg.className = "msg-wrong show-msg";
                setTimeout(() => {{ triggerPython("💣"); }}, 600);
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
    st.error("💀 GAME OVER! Your atomic energy has depleted.")
    if st.button("♻️ RESTART FROM STAGE 1", use_container_width=True):
        st.session_state.lvl = 0
        st.session_state.lives = 3
        st.session_state.game_over = False
        st.rerun()
else:
    components.html(game_html, height=260)
    st.write("---")
    
    # 5. DATA SHEET
    verify_text = st.text_input("📜 Scroll of Truth:", placeholder="Type in the element name to unlock level", label_visibility="collapsed")

    if verify_text.upper() == target_word:
        final_data = ELEMENTS_DB[target_word]
        st.markdown(f"""
        <div style="background: #ffffff; padding: 20px; border-radius: 15px; border: 2px solid #f39c12; color: #333;">
            <div style="text-align: center; border-bottom: 2px solid #f39c12; margin-bottom: 15px;">
                <h2 style="margin: 0; color: #2c3e50;">{target_word}</h2>
                <span style="font-size: 40px; font-weight: bold; color: #f39c12;">{final_data[4]}</span>
            </div>
            <div style="display: flex; justify-content: space-around; font-size: 14px; margin-bottom: 15px;">
                <div style="text-align: center;"><b>Atomic Number (Z)</b><br><span style="font-size: 20px;">{final_data[0]}</span></div>
                <div style="text-align: center;"><b>Mass Number (A)</b><br><span style="font-size: 20px;">{final_data[1]}</span></div>
            </div>
            <div style="display: flex; justify-content: space-around; font-size: 14px; margin-bottom: 15px; background: #f9f9f9; padding: 10px; border-radius: 8px;">
                <div style="text-align: center;"><b>Group</b><br>{final_data[2]}</div>
                <div style="text-align: center;"><b>Period</b><br>{final_data[3]}</div>
            </div>
            <p style="font-size: 13px; line-height: 1.6; text-align: justify; color: #555;"><b>Element Overview:</b> {final_data[5]}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 ADVANCE TO NEXT STAGE", use_container_width=True):
            st.session_state.lvl = (st.session_state.lvl + 1) % len(ELEMENT_LIST)
            st.rerun()
    else:
        st.button("🔒 PATH BLOCKED", disabled=True, use_container_width=True)

# 6. HOW TO PLAY
st.markdown("---")
st.markdown("""
<div style="background: #2c3e50; padding: 20px; border-radius: 15px; border-left: 8px solid #f39c12; color: white;">
    <h3 style="margin-top:0; color: #f39c12;">📖 How to Play</h3>
    <div style="font-size: 14px; line-height: 1.6;">
        <p><b>1. Assemble the Atom:</b> Unscramble the name within <b>60 seconds</b>.</p>
        <p><b>2. Life Rewards:</b> Correct answers grant a <b>+2 ❤️ Bonus</b>. Incorrect attempts or time-outs result in a <b>-1 ❤️ Penalty</b>.</p>
        <p><b>3. Scientific Mastery:</b> Unlock the <i>Scroll of Truth</i> to study the atomic properties required for SS1 Chemistry.</p>
    </div>
</div>
""", unsafe_allow_html=True)
