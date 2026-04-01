import streamlit as st
import streamlit.components.v1 as components

st.markdown("<h2 style='text-align: center; color: #2b8a3e;'>🧪 ELEMENT DRAG-MATCH</h2>", unsafe_allow_html=True)

# THE GAME ENGINE: Drag-to-Select Logic
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: white; margin: 0; padding: 10px; touch-action: none; user-select: none; }
        
        .word-list { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px; justify-content: center; max-width: 340px; }
        .word-item { font-size: 11px; font-weight: bold; color: #555; text-transform: uppercase; border: 1px solid #ddd; padding: 3px 6px; border-radius: 4px; }
        .crossed { text-decoration: line-through; color: #bbb; background: #f0f0f0; border-color: #eee; }

        .grid { 
            display: grid; 
            grid-template-columns: repeat(10, 32px); 
            gap: 4px; 
            background: #ffffff; 
            padding: 5px; 
            position: relative;
        }
        
        .cell { 
            width: 32px; height: 32px; 
            display: flex; align-items: center; justify-content: center; 
            background: #fdfdfd; border: 1px solid #eee; 
            font-weight: 800; font-size: 16px; border-radius: 5px;
            pointer-events: none; /* Let the container handle the touch */
        }

        .highlighted { background-color: #a5d8ff !important; color: #1971c2; }
        .found { background-color: #b2f2bb !important; color: #2b8a3e; border-radius: 50% !important; border: none !important; }

        .status { margin-top: 15px; font-size: 16px; font-weight: bold; color: #1971c2; }
    </style>
</head>
<body>

    <div class="word-list" id="wordList"></div>
    <div class="grid" id="gridBoard" onmousedown="startSelect(event)" ontouchstart="startSelect(event)">
        </div>
    <div class="status" id="status">Drag across letters to spell!</div>

    <script>
        const elements = ["HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", "OXYGEN", "SODIUM", "NEON"];
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

        // Build Board
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

        function startSelect(e) {
            isDragging = true;
            currentSelection = [];
            document.addEventListener('mousemove', handleMove);
            document.addEventListener('mouseup', endSelect);
            document.addEventListener('touchmove', handleMove, {passive: false});
            document.addEventListener('touchend', endSelect);
            handleMove(e);
        }

        function handleMove(e) {
            if (!isDragging) return;
            e.preventDefault();
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

        function endSelect() {
            isDragging = false;
            document.removeEventListener('mousemove', handleMove);
            document.removeEventListener('mouseup', endSelect);
            document.removeEventListener('touchmove', handleMove);
            document.removeEventListener('touchend', endSelect);

            const finalWord = currentSelection.map(i => gridData[i]).join('');
            
            if (elements.includes(finalWord) && !foundWords.includes(finalWord)) {
                foundWords.push(finalWord);
                currentSelection.forEach(idx => {
                    const el = document.getElementById('cell-' + idx);
                    el.classList.remove('highlighted');
                    el.classList.add('found');
                });
                document.getElementById('status').innerText = "✓ " + finalWord;
                updateList();
            } else {
                currentSelection.forEach(idx => {
                    const el = document.getElementById('cell-' + idx);
                    if (!el.classList.contains('found')) el.classList.remove('highlighted');
                });
                document.getElementById('status').innerText = "Try again!";
            }
            currentSelection = [];
        }

        updateList();
    </script>
</body>
</html>
"""

components.html(game_html, height=580)
st.markdown("<p style='text-align: center; color: #999; font-size: 11px;'>MSc | Chemical Games Engine by Favour</p>", unsafe_allow_html=True)
