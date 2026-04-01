import streamlit as st
import streamlit.components.v1 as components

st.markdown("<h2 style='text-align: center; color: #2b8a3e;'>🧪 ELEMENT SEQUENCE MATCH</h2>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: white; margin: 0; padding: 10px; }
        
        .word-list { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px; justify-content: center; max-width: 320px; }
        .word-item { font-size: 11px; font-weight: bold; color: #555; text-transform: uppercase; border: 1px solid #ddd; padding: 3px 6px; border-radius: 4px; }
        .crossed { text-decoration: line-through; color: #bbb; background: #f0f0f0; border-color: #eee; }

        .grid { 
            display: grid; 
            grid-template-columns: repeat(10, 32px); 
            gap: 4px; 
            background: #ffffff; 
            padding: 5px; 
        }
        
        .cell { 
            width: 32px; height: 32px; 
            display: flex; align-items: center; justify-content: center; 
            background: #fdfdfd; border: 1px solid #eee; 
            font-weight: 800; font-size: 16px; cursor: pointer; 
            user-select: none; border-radius: 5px;
        }

        /* Feedback Colors */
        .selecting { background-color: #a5d8ff !important; color: #1971c2; transform: scale(1.1); }
        .found { background-color: #b2f2bb !important; color: #2b8a3e; border-radius: 50%; border: none; }

        .status-text { margin-top: 15px; font-size: 16px; font-weight: bold; color: #1971c2; min-height: 20px; }
        .btn-clear { margin-top: 10px; padding: 8px 25px; border-radius: 20px; border: none; background: #fa5252; color: white; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

    <div class="word-list" id="wordList"></div>
    <div class="grid" id="gridBoard"></div>
    <div class="status-text" id="status">Tap letters to spell...</div>
    <button class="btn-clear" onclick="resetSelection()">Reset Selection</button>

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

        let selectedIndices = [];
        let foundWords = [];

        function updateDisplay() {
            const listDiv = document.getElementById('wordList');
            listDiv.innerHTML = elements.map(e => `<span class="word-item ${foundWords.includes(e) ? 'crossed' : ''}">${e}</span>`).join('');
        }

        const board = document.getElementById('gridBoard');
        gridData.forEach((char, idx) => {
            const div = document.createElement('div');
            div.className = 'cell';
            div.innerText = char;
            div.id = 'cell-' + idx;
            div.onclick = () => handleTap(idx, char);
            board.appendChild(div);
        });

        function handleTap(idx, char) {
            if (selectedIndices.includes(idx)) return; // Prevent double-tap

            selectedIndices.push(idx);
            document.getElementById('cell-' + idx).classList.add('selecting');
            
            let currentString = selectedIndices.map(i => gridData[i]).join('');
            document.getElementById('status').innerText = currentString;

            // Check if string matches an element
            if (elements.includes(currentString)) {
                if (!foundWords.includes(currentString)) {
                    foundWords.push(currentString);
                    markAsFound();
                    document.getElementById('status').innerText = "✓ " + currentString;
                }
            }
        }

        function markAsFound() {
            selectedIndices.forEach(idx => {
                const el = document.getElementById('cell-' + idx);
                el.classList.remove('selecting');
                el.classList.add('found');
            });
            selectedIndices = [];
            updateDisplay();
        }

        function resetSelection() {
            selectedIndices.forEach(idx => {
                const el = document.getElementById('cell-' + idx);
                if (!el.classList.contains('found')) {
                    el.classList.remove('selecting');
                }
            });
            selectedIndices = [];
            document.getElementById('status').innerText = "Selection Cleared";
        }

        updateDisplay();
    </script>
</body>
</html>
"""

components.html(game_html, height=550)
st.markdown("<p style='text-align: center; color: #999; font-size: 12px;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
