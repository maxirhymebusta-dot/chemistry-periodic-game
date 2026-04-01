import streamlit as st
import streamlit.components.v1 as components

# 1. Clean Layout
st.set_page_config(page_title="Periodic Master", layout="centered")
st.markdown("<h3 style='text-align: center; color: #2b8a3e;'>🧪 FIRST 20: LABORATORY GRID</h3>", unsafe_allow_html=True)

# 2. THE ENGINE: Zero-Latency Pointer Capture
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        /* THIS STOPS THE SHIT: Total browser lock */
        html, body { 
            touch-action: none; 
            -webkit-touch-callout: none; 
            -webkit-user-select: none; 
            user-select: none; 
            overflow: hidden; 
            overscroll-behavior: none;
            background: white; margin: 0; padding: 10px;
            font-family: sans-serif;
            display: flex; flex-direction: column; align-items: center;
        }
        
        .word-bank { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px; justify-content: center; max-width: 300px; }
        .word { font-size: 10px; font-weight: bold; color: #444; border: 1px solid #ddd; padding: 2px 5px; border-radius: 4px; }
        .done { text-decoration: line-through; color: #ccc; background: #f9f9f9; }

        .grid-container { 
            display: grid; 
            grid-template-columns: repeat(10, 32px); 
            gap: 4px; 
            padding: 10px; 
            border: 3px solid #82c91e;
            border-radius: 12px;
            touch-action: none;
        }
        
        .cell { 
            width: 32px; height: 32px; 
            display: flex; align-items: center; justify-content: center; 
            background: #fff; border: 1px solid #eee; 
            font-weight: 800; font-size: 16px; border-radius: 4px;
            pointer-events: none; /* Crucial: allows grid to track the finger */
        }

        .active { background-color: #a5d8ff !important; color: #1971c2; transform: scale(1.1); }
        .solved { background-color: #b2f2bb !important; color: #2b8a3e; border-radius: 50% !important; border: none !important; }
        
        #current-word { margin-top: 15px; font-size: 18px; font-weight: bold; color: #1971c2; height: 30px; }
    </style>
</head>
<body>

    <div class="word-bank" id="bank"></div>
    <div class="grid-container" id="g"></div>
    <div id="current-word">DRAG ACROSS LETTERS</div>

    <script>
        const elements = ["HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", "OXYGEN"];
        const grid = ["B","O","X","Y","G","E","N","N","N","N","L","E","A","P","T","U","E","C","I","I","O","S","R","B","Z","G","I","A","T","T","Z","H","W","Y","O","J","W","R","R","R","U","R","E","R","L","R","I","B","O","O","E","B","D","L","A","L","O","O","G","G","I","Y","M","U","I","I","I","N","E","E","H","B","R","U","D","U","H","U","N","N","L","I","T","H","I","U","M","L","M","M","C","A","L","C","I","U","M","X","Y","Z"];

        let path = [];
        let solved = [];
        let dragging = false;

        const container = document.getElementById('g');
        const status = document.getElementById('current-word');

        // Render Grid
        grid.forEach((char, i) => {
            const div = document.createElement('div');
            div.className = 'cell'; div.id = 'idx' + i; div.innerText = char;
            container.appendChild(div);
        });

        function refreshBank() {
            document.getElementById('bank').innerHTML = elements.map(e => 
                `<span class="word ${solved.includes(e) ? 'done' : ''}">${e}</span>`).join('');
        }

        // POINTER LOCK LOGIC
        container.onpointerdown = (e) => {
            dragging = true;
            path = [];
            container.setPointerCapture(e.pointerId);
            track(e);
        };

        container.onpointermove = (e) => { if (dragging) track(e); };

        container.onpointerup = (e) => {
            dragging = false;
            container.releasePointerCapture(e.pointerId);
            check();
        };

        function track(e) {
            const target = document.elementFromPoint(e.clientX, e.clientY);
            if (target && target.id.startsWith('idx')) {
                const i = parseInt(target.id.replace('idx',''));
                if (!path.includes(i)) {
                    path.push(i);
                    target.classList.add('active');
                    status.innerText = path.map(p => grid[p]).join('');
                }
            }
        }

        function check() {
            const word = path.map(p => grid[p]).join('');
            if (elements.includes(word)) {
                solved.push(word);
                path.forEach(i => {
                    document.getElementById('idx' + i).classList.remove('active');
                    document.getElementById('idx' + i).classList.add('solved');
                });
                refreshBank();
                status.innerText = "✓ " + word;
            } else {
                path.forEach(i => {
                    const el = document.getElementById('idx' + i);
                    if (!el.classList.contains('solved')) el.classList.remove('active');
                });
                status.innerText = "TRY AGAIN";
            }
            path = [];
        }

        refreshBank();
    </script>
</body>
</html>
"""

components.html(game_html, height=550)
st.markdown("<p style='text-align: center; color: #999; font-size: 11px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
