import streamlit as st
import streamlit.components.v1 as components

st.markdown("<h2 style='text-align: center; color: #2b8a3e;'>🧪 FIRST 20 ELEMENTS GRID</h2>", unsafe_allow_html=True)

# THE GAME ENGINE - Updated with Mobile Scaling
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-select=no">
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: white; margin: 0; padding: 5px; }
        
        /* THE WORD LIST: Smaller text for mobile */
        .word-list { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px; justify-content: center; max-width: 320px; }
        .word-item { font-size: 10px; font-weight: bold; color: #333; text-transform: uppercase; border: 1px solid #eee; padding: 2px 5px; border-radius: 4px; }
        .crossed { text-decoration: line-through; color: #ccc; background: #fafafa; }

        /* THE GRID: Adjusted size to 30px per cell to fit all phone screens */
        .grid { 
            display: grid; 
            grid-template-columns: repeat(10, 30px); 
            gap: 3px; 
            background: #f8f9fa; 
            padding: 8px; 
            border: 2px solid #dee2e6;
            border-radius: 10px;
        }
        
        .cell { 
            width: 30px; height: 30px; 
            display: flex; align-items: center; justify-content: center; 
            background: white; border: 1px solid #eee; 
            font-weight: 800; font-size: 14px; cursor: pointer; 
            user-select: none; border-radius: 4px;
        }

        .selected { background-color: #a5d8ff !important; color: #1971c2; }
        .found { background-color: #b2f2bb !important; color: #2b8a3e; border-radius: 50%; }

        .controls { margin-top: 15px; display: flex; gap: 8px; }
        button.action { padding: 8px 15px; border-radius: 20px; border: none; background: #82c91e; color: white; font-weight: bold; font-size: 12px; }
    </style>
</head>
<body>

    <div class="word-list" id="wordList"></div>
    <div class="grid" id="gridBoard"></div>

    <div style="margin-top:10px; font-size: 14px; font-weight:bold; color:#1971c2;">Selection: <span id="currentVal">---</span></div>

    <div class="controls">
        <button class="action" onclick="checkWord()">Check</button>
        <button class="action" style="background:#fa5252;" onclick="resetSelection()">Clear</button>
    </div>

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

        function updateWordList() {
            const listDiv = document.getElementById('wordList');
            listDiv.innerHTML = elements.map(e => `<span class="word-item ${foundWords.includes(e) ? 'crossed' : ''}">${e}</span>`).join('');
        }

        const board = document.getElementById('gridBoard');
        gridData.forEach((char, idx) => {
            const div = document.createElement('div');
            div.className = 'cell';
            div.innerText = char;
            div.onclick = () => toggleSelect(idx, div);
            board.appendChild(div);
        });

        function toggleSelect(idx, el) {
            if (selectedIndices.includes(idx)) {
                selectedIndices = selectedIndices.filter(i => i !== idx);
                el.classList.remove('selected');
            } else {
                selectedIndices.push(idx);
                el.classList.add('selected');
            }
            const currentString = selectedIndices.map(i => gridData[i]).join('');
            document.getElementById('currentVal').innerText = currentString || "---";
        }

        function checkWord() {
            const currentString = selectedIndices.map(i => gridData[i]).join('');
            if (elements.includes(currentString)) {
                foundWords.push(currentString);
                selectedIndices.forEach(idx => {
                    const cells = document.getElementsByClassName('cell');
                    cells[idx].classList.remove('selected');
                    cells[idx].classList.add('found');
                });
                selectedIndices = [];
                updateWordList();
                document.getElementById('currentVal').innerText = "FOUND!";
            } else {
                resetSelection();
            }
        }

        function resetSelection() {
            selectedIndices = [];
            const cells = document.getElementsByClassName('cell');
            for(let cell of cells) { cell.classList.remove('selected'); }
            document.getElementById('currentVal').innerText = "---";
        }

        updateWordList();
    </script>
</body>
</html>
"""

components.html(game_html, height=550)
st.markdown("<p style='text-align: center; color: #999; font-size: 12px;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
