import streamlit as st
import streamlit.components.v1 as components

# 1. Page Header
st.set_page_config(page_title="First 20 Elements Master", layout="centered")
st.markdown("<h2 style='text-align: center; color: #2b8a3e;'>🧪 FIRST 20: DRAG-MATCH</h2>", unsafe_allow_html=True)

# 2. THE ENGINE: Pointer Capture (Universal Touch)
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { touch-action: none; user-select: none; -webkit-user-select: none; box-sizing: border-box; }
        body { 
            font-family: sans-serif; display: flex; flex-direction: column; 
            align-items: center; background: white; margin: 0; padding: 10px; 
        }
        
        .word-list { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px; justify-content: center; max-width: 300px; }
        .word-item { font-size: 10px; font-weight: bold; color: #555; text-transform: uppercase; border: 1px solid #ddd; padding: 3px 6px; border-radius: 4px; }
        .crossed { text-decoration: line-through; color: #bbb; background: #f0f0f0; }

        .grid { 
            display: grid; 
            grid-template-columns: repeat(10, 32px); 
            gap: 5px; 
            background: #ffffff; 
            padding: 10px; 
            border: 3px solid #82c91e;
            border-radius: 15px;
            touch-action: none;
        }
        
        .cell { 
            width: 32px; height: 32px; 
            display: flex; align-items: center; justify-content: center; 
            background: #fdfdfd; border: 1px solid #eee; 
            font-weight: 800; font-size: 16px; border-radius: 5px;
            pointer-events: none; /* Allows the parent grid to 'see' the touch through the letters */
        }

        .highlighted { background-color: #a5d8ff !important; color: #1971c2; transform: scale(1.1); }
        .found { background-color: #b2f2bb !important; color: #2b8a3e; border-radius: 50% !important; border: none !important; }

        .status { margin-top: 15px; font-size: 16px; font-weight: bold; color: #1971c2; min-height: 20px; }
    </style>
</head>
<body>

    <div class="word-list" id="wordList"></div>
    <div class="grid" id="gridBoard"></div>
    <div class="status" id="status">Drag your finger to spell!</div>

    <script>
        const elements = ["HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", "OXYGEN"];
        const gridData = ["B","O","X","Y","G","E","N","N","N","N","L","E","A","P","T","U","E","C","I","I","O","S","R","B","Z","G","I","A","T","T","Z","H","W","Y","O","J","W","R","R","R","U","R","E","R","L","R","I","B","O","O","E","B","D","L","A","L","O","O","G","G","I","Y","M","U","I","I","I","N","E","E","H","B","R","U","D","U","H","U","N","N","L","I","T","H","I","U","M","L","M","M","C","A","L","C","I","U","M","X","Y","Z"];

        let isDragging = false;
        let selectedIndices = [];
        let foundWords = [];

        const board = document.getElementById('gridBoard');
        gridData.forEach((char, idx) => {
            const div = document.createElement('div');
            div.className = 'cell'; div.innerText = char; div.id = 'cell-' + idx;
            board.appendChild(div);
        });

        function updateList() {
            document.getElementById('wordList').innerHTML = elements.map(e => 
                `<span class="word-item ${foundWords.includes(e) ? 'crossed' : ''}">${e}</span>`).join('');
        }

        // FORCE POINTER CAPTURE
        board.onpointerdown = (e) => {
            isDragging = true;
            selectedIndices = [];
            board.setPointerCapture(e.pointerId); // LOCKS FINGER TO GRID
            handleInteraction(e);
        };

        board.onpointermove = (e) => {
            if (isDragging) handleInteraction(e);
        };

        board.onpointerup = (e) => {
            if (!isDragging) return;
            isDragging = false;
            board.releasePointerCapture(e.pointerId);
            checkSelection();
        };

        function handleInteraction(e) {
            const target = document.elementFromPoint(e.clientX, e.clientY);
            if (target && target.id.startsWith('cell-')) {
                const idx = parseInt(target.id.split('-')[1]);
                if (!selectedIndices.includes(idx)) {
                    selectedIndices.push(idx);
                    target.classList.add('highlighted');
                    document.getElementById('status').innerText = selectedIndices.map(i => gridData[i]).join('');
                }
            }
        }

        function checkSelection() {
            const word = selectedIndices.map(i => gridData[i]).join('');
            if (elements.includes(word)) {
                foundWords.push(word);
                selectedIndices.forEach(idx => document.getElementById('cell-' + idx).classList.add('found'));
                updateList();
            } else {
                selectedIndices.forEach(idx => {
                    let el = document.getElementById('cell-' + idx);
                    if (!el.classList.contains('found')) el.classList.remove('highlighted');
                });
            }
            selectedIndices = [];
            document.getElementById('status').innerText = "Wipe next element...";
        }

        updateList();
    </script>
</body>
</html>
"""

components.html(game_html, height=580)
st.markdown("<p style='text-align: center; color: #999; font-size: 11px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
