import streamlit as st
import streamlit.components.v1 as components

# 1. Clean Layout
st.set_page_config(page_title="Periodic Master", layout="centered")
st.markdown("<h3 style='text-align: center; color: #2b8a3e;'>🧪 FIRST 20: LABORATORY GRID</h3>", unsafe_allow_html=True)

# 2. THE ENGINE: High-Pressure Pointer Tracking
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        /* CRITICAL: Stops the browser from stealing the touch for scrolling */
        * { touch-action: none; -webkit-touch-callout: none; -webkit-user-select: none; user-select: none; box-sizing: border-box; }
        
        body { 
            font-family: sans-serif; display: flex; flex-direction: column; 
            align-items: center; background: white; margin: 0; padding: 10px;
            overflow: hidden; touch-action: none;
        }
        
        .word-bank { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px; justify-content: center; max-width: 300px; }
        .word { font-size: 10px; font-weight: bold; color: #444; border: 1px solid #ddd; padding: 2px 5px; border-radius: 4px; background: white; }
        .done { text-decoration: line-through; color: #ccc; background: #f9f9f9 !important; border-color: #eee; }

        .grid-container { 
            display: grid; 
            grid-template-columns: repeat(10, 32px); 
            gap: 4px; 
            padding: 10px; 
            border: 3px solid #82c91e;
            border-radius: 12px;
            background: #fff;
            touch-action: none;
            position: relative;
        }
        
        .cell { 
            width: 32px; height: 32px; 
            display: flex; align-items: center; justify-content: center; 
            background: #fff; border: 1px solid #eee; 
            font-weight: 800; font-size: 16px; border-radius: 4px;
            pointer-events: none; /* Allows the finger to be tracked by the grid background */
        }

        /* The Visual Feedback */
        .active { background-color: #a5d8ff !important; color: #1971c2; transform: scale(1.1); box-shadow: 0 0 5px rgba(0,0,0,0.1); }
        .solved { background-color: #b2f2bb !important; color: #2b8a3e; border-radius: 50% !important; border: none !important; }
        
        #status-bar { margin-top: 15px; font-size: 18px; font-weight: bold; color: #1971c2; height: 30px; text-align: center; }
    </style>
</head>
<body oncontextmenu="return false;">

    <div class="word-bank" id="bank"></div>
    <div class="grid-container" id="gContainer"></div>
    <div id="status-bar">Wipe across letters!</div>

    <script>
        const elements = ["HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", "OXYGEN"];
        const gridData = ["B","O","X","Y","G","E","N","N","N","N","L","E","A","P","T","U","E","C","I","I","O","S","R","B","Z","G","I","A","T","T","Z","H","W","Y","O","J","W","R","R","R","U","R","E","R","L","R","I","B","O","O","E","B","D","L","A","L","O","O","G","G","I","Y","M","U","I","I","I","N","E","E","H","B","R","U","D","U","H","U","N","N","L","I","T","H","I","U","M","L","M","M","C","A","L","C","I","U","M","X","Y","Z"];

        let isDragging = false;
        let selectedIndices = [];
        let solvedWords = [];

        const container = document.getElementById('gContainer');
        const status = document.getElementById('status-bar');

        // Create Grid Cells
        gridData.forEach((char, i) => {
            const div = document.createElement('div');
            div.className = 'cell'; div.id = 'idx' + i; div.innerText = char;
            container.appendChild(div);
        });

        function refreshBank() {
            document.getElementById('bank').innerHTML = elements.map(e => 
                `<span class="word ${solvedWords.includes(e) ? 'done' : ''}">${e}</span>`).join('');
        }

        // THE FIX: Direct Pointer Event Handling
        container.onpointerdown = (e) => {
            isDragging = true;
            selectedIndices = [];
            container.setPointerCapture(e.pointerId); // LOCKS THE TOUCH TO THE GRID
            processPoint(e);
        };

        container.onpointermove = (e) => {
            if (isDragging) processPoint(e);
        };

        container.onpointerup = (e) => {
            if (!isDragging) return;
            isDragging = false;
            container.releasePointerCapture(e.pointerId);
            validateSelection();
        };

        function processPoint(e) {
            // Find which cell is under the finger right now
            const target = document.elementFromPoint(e.clientX, e.clientY);
            if (target && target.id.startsWith('idx')) {
                const idx = parseInt(target.id.replace('idx',''));
                if (!selectedIndices.includes(idx)) {
                    selectedIndices.push(idx);
                    target.classList.add('active'); // Turn it Blue immediately
                    status.innerText = selectedIndices.map(i => gridData[i]).join('');
                }
            }
        }

        function validateSelection() {
            const word = selectedIndices.map(i => gridData[i]).join('');
            if (elements.includes(word) && !solvedWords.includes(word)) {
                solvedWords.push(word);
                selectedIndices.forEach(idx => {
                    const el = document.getElementById('idx' + idx);
                    el.classList.remove('active');
                    el.classList.add('solved'); // Turn it Green
                });
                refreshBank();
                status.innerText = "✓ " + word;
            } else {
                // If wrong, remove the blue highlights
                selectedIndices.forEach(idx => {
                    const el = document.getElementById('idx' + idx);
                    if (!el.classList.contains('solved')) el.classList.remove('active');
                });
                status.innerText = "TRY AGAIN";
            }
            selectedIndices = [];
        }

        refreshBank();
    </script>
</body>
</html>
"""

components.html(game_html, height=580)
st.markdown("<p style='text-align: center; color: #999; font-size: 11px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
