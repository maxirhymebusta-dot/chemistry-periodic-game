import streamlit as st
import streamlit.components.v1 as components

# 1. Page Setup
st.set_page_config(page_title="MSc Project: Chemical Grid", layout="centered")
st.markdown("<h2 style='text-align: center; color: #2b8a3e;'>🧪 ELEMENT DRAG-MATCH</h2>", unsafe_allow_html=True)

# 2. THE ENGINE: High-Sensitivity Pointer Capture
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        /* CRITICAL: Stops the browser from stealing the touch */
        * { touch-action: none; user-select: none; -webkit-user-select: none; box-sizing: border-box; }
        
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: white; margin: 0; padding: 10px; }
        
        .word-list { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px; justify-content: center; max-width: 300px; }
        .word-item { font-size: 10px; font-weight: bold; color: #333; text-transform: uppercase; border: 1px solid #ddd; padding: 3px; border-radius: 4px; }
        .crossed { text-decoration: line-through; color: #ccc; background: #fafafa; }

        .grid-board { 
            display: grid; 
            grid-template-columns: repeat(10, 32px); 
            gap: 5px; 
            background: #ffffff; 
            padding: 10px; 
            border: 3px solid #82c91e;
            border-radius: 15px;
            touch-action: none; /* FORCES MOBILE TO IGNORE SCROLL */
        }
        
        .cell { 
            width: 32px; height: 32px; 
            display: flex; align-items: center; justify-content: center; 
            background: #fdfdfd; border: 1px solid #eee; 
            font-weight: 800; font-size: 16px; border-radius: 5px;
            pointer-events: none; /* Let the finger 'see through' to the board */
        }

        .highlighted { background-color: #a5d8ff !important; color: #1971c2; transform: scale(1.1); transition: 0.1s; }
        .found { background-color: #b2f2bb !important; color: #2b8a3e; border-radius: 50% !important; border: none !important; }
        
        #status-bar { margin-top: 15px; font-size: 18px; font-weight: bold; color: #1971c2; height: 25px; }
    </style>
</head>
<body>

    <div class="word-list" id="wordList"></div>
    
    <div class="grid-board" id="board">
        </div>
    
    <div id="status-bar">Wipe to Spell!</div>

    <script>
        const elements = ["HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", "OXYGEN"];
        const gridData = ["B","O","X","Y","G","E","N","N","N","N","L","E","A","P","T","U","E","C","I","I","O","S","R","B","Z","G","I","A","T","T","Z","H","W","Y","O","J","W","R","R","R","U","R","E","R","L","R","I","B","O","O","E","B","D","L","A","L","O","O","G","G","I","Y","M","U","I","I","I","N","E","E","H","B","R","U","D","U","H","U","N","N","L","I","T","H","I","U","M","L","M","M","C","A","L","C","I","U","M","X","Y","Z"];

        let activeIndices = [];
        let discovered = [];
        let isTouching = false;

        const board = document.getElementById('board');
        const status = document.getElementById('status-bar');

        // Create Grid
        gridData.forEach((char, i) => {
            const d = document.createElement('div');
            d.className = 'cell'; d.id = 'c' + i; d.innerText = char;
            board.appendChild(d);
        });

        function updateUI() {
            document.getElementById('wordList').innerHTML = elements.map(e => 
                `<span class="word-item ${discovered.includes(e) ? 'crossed' : ''}">${e}</span>`).join('');
        }

        // THE CORE DRAG LOGIC (Pointer Events)
        board.onpointerdown = (e) => {
            isTouching = true;
            activeIndices = [];
            board.setPointerCapture(e.pointerId); // LOCKS INPUT TO THIS GRID
            processMove(e);
        };

        board.onpointermove = (e) => {
            if (isTouching) processMove(e);
        };

        board.onpointerup = (e) => {
            isTouching = false;
            board.releasePointerCapture(e.pointerId);
            finalize();
        };

        function processMove(e) {
            const hit = document.elementFromPoint(e.clientX, e.clientY);
            if (hit && hit.id.startsWith('c')) {
                const idx = parseInt(hit.id.substring(1));
                if (!activeIndices.includes(idx)) {
                    activeIndices.push(idx);
                    hit.classList.add('highlighted');
                    status.innerText = activeIndices.map(i => gridData[i]).join('');
                }
            }
        }

        function finalize() {
            const word = activeIndices.map(i => gridData[i]).join('');
            if (elements.includes(word)) {
                discovered.push(word);
                activeIndices.forEach(idx => {
                    const el = document.getElementById('c' + idx);
                    el.classList.remove('highlighted');
                    el.classList.add('found');
                });
                updateUI();
                status.innerText = "✓ FOUND!";
            } else {
                activeIndices.forEach(idx => {
                    const el = document.getElementById('c' + idx);
                    if (!el.classList.contains('found')) el.classList.remove('highlighted');
                });
                status.innerText = "Try Again";
            }
            activeIndices = [];
        }

        updateUI();
    </script>
</body>
</html>
"""

components.html(game_html, height=600)
st.markdown("<p style='text-align: center; color: #999; font-size: 11px;'>MSc | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
