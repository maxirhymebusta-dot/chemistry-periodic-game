import streamlit as st
import streamlit.components.v1 as components

st.markdown("<h2 style='text-align: center; color: #2b8a3e;'>🧪 ELEMENT DRAG-MATCH</h2>", unsafe_allow_html=True)

# THE GAME ENGINE: Bulletproof Touch-Locking
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { touch-action: none; user-select: none; -webkit-user-select: none; }
        body { 
            font-family: sans-serif; display: flex; flex-direction: column; 
            align-items: center; background: white; margin: 0; padding: 10px; 
        }
        
        .word-list { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px; justify-content: center; max-width: 300px; }
        .word-item { font-size: 10px; font-weight: bold; color: #555; text-transform: uppercase; border: 1px solid #ddd; padding: 2px 5px; border-radius: 4px; }
        .crossed { text-decoration: line-through; color: #bbb; background: #f0f0f0; }

        .grid { 
            display: grid; 
            grid-template-columns: repeat(10, 30px); 
            gap: 4px; 
            background: #ffffff; 
            padding: 10px; 
            border: 2px solid #82c91e;
            border-radius: 15px;
        }
        
        .cell { 
            width: 30px; height: 30px; 
            display: flex; align-items: center; justify-content: center; 
            background: #fdfdfd; border: 1px solid #eee; 
            font-weight: 800; font-size: 15px; border-radius: 5px;
            pointer-events: none; /* Crucial: allows drag to pass through to the container */
        }

        .highlighted { background-color: #a5d8ff !important; color: #1971c2; transform: scale(1.1); }
        .found { background-color: #b2f2bb !important; color: #2b8a3e; border-radius: 50% !important; border: none !important; }

        .status { margin-top: 15px; font-size: 14px; font-weight: bold; color: #1971c2; text-align: center; }
    </style>
</head>
<body>

    <div class="word-list" id="wordList"></div>
    
    <div class="grid" id="gridBoard">
        </div>
    
    <div class="status" id="status">Wipe your finger over the letters!</div>

    <script>
        const elements = ["HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", "OXYGEN"];
        const gridData = [
            "B", "O", "X", "Y", "G", "E", "N", "N", "N", "N",
            "L", "E", "A", "P", "T", "U", "E", "C", "I", "I",
            "O", "S", "R", "B", "Z", "G", "I", "A", "T", "T",
            "Z", "H", "W", "Y", "O", "J", "W", "R", "R", "R",
            "U", "R", "E", "R", "L", "R", "I", "B", "O", "O",
            "E", "B", "D", "L", "A", "L", "O", "O", "G", "G",
            "I", "Y", "M", "U", "I", "I", "I", "N", "E", "E",
            "H", "B", "R", "U", "D", "U", "H", "U", "N", "N",
            "L", "I", "T", "H", "I", "U", "M", "L", "M", "M",
            "C", "A", "L", "C", "I", "U", "M", "X", "Y", "Z"
        ];

        let isDragging = false;
        let currentSelection = [];
        let foundWords = [];

        const board = document.getElementById('gridBoard');
        gridData.forEach((char, idx) => {
            const div = document.createElement('div');
            div.className = 'cell';
            div.innerText = char;
            div.id = 'cell-' + idx;
            board.appendChild(div);
        });

        function updateList() {
            document.getElementById('wordList').innerHTML = elements.map(e => 
                `<span class="word-item ${foundWords.includes(e) ? 'crossed' : ''}">${e}</span>`).join('');
        }

        // UNIVERSAL DRAG LISTENERS
        function handleStart(e) {
            isDragging = true;
            currentSelection = [];
            handleMove(e);
        }

        function handleMove(e) {
            if (!isDragging) return;
            e.preventDefault(); // Stop the phone from scrolling
            
            const touch = e.touches ? e.touches[0] : e;
            const target = document.elementFromPoint(touch.clientX, touch.clientY);
            
            if (target && target.id.startsWith('cell-')) {
                const idx = parseInt(target.id.split('-')[1]);
                if (!currentSelection.includes(idx)) {
                    currentSelection.push(idx);
                    target.classList.add('highlighted');
                    const word = currentSelection.map(i => gridData[i]).join('');
                    document.getElementById('status').innerText = word;
                }
            }
        }

        function handleEnd() {
            if (!isDragging) return;
            isDragging = false;
            const finalWord = currentSelection.map(i => gridData[i]).join('');
            
            if (elements.includes(finalWord)) {
                foundWords.push(finalWord);
                currentSelection.forEach(idx => {
                    document.getElementById('cell-' + idx).classList.add('found');
                });
                updateList();
            } else {
                currentSelection.forEach(idx => {
                    const el = document.getElementById('cell-' + idx);
                    if (!el.classList.contains('found')) el.classList.remove('highlighted');
                });
            }
            currentSelection = [];
            document.getElementById('status').innerText = "Wipe next element...";
        }

        // Attach listeners to the board
        board.addEventListener('mousedown', handleStart);
        window.addEventListener('mousemove', handleMove);
        window.addEventListener('mouseup', handleEnd);

        board.addEventListener('touchstart', handleStart, {passive: false});
        window.addEventListener('touchmove', handleMove, {passive: false});
        window.addEventListener('touchend', handleEnd);

        updateList();
    </script>
</body>
</html>
"""

components.html(game_html, height=580)
st.markdown("<p style='text-align: center; color: #999; font-size: 11px;'>MSc | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
