import streamlit as st
import streamlit.components.v1 as components

# 1. Page Setup
st.set_page_config(page_title="Chemical Grid Master", layout="centered")

st.markdown("<h2 style='text-align: center; color: #2b8a3e;'>🧪 FIRST 20 ELEMENTS: LABORATORY GRID</h2>", unsafe_allow_html=True)
st.write("Tap letters to build the element name. Correct matches will highlight green!")

# 2. THE GAME ENGINE (HTML + CSS + JAVASCRIPT)
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: white; }
        
        /* THE GRID: Forced 10x10 Square */
        .grid { 
            display: grid; 
            grid-template-columns: repeat(10, 35px); 
            gap: 5px; 
            background: #f8f9fa; 
            padding: 10px; 
            border: 2px solid #dee2e6;
            border-radius: 10px;
        }
        
        .cell { 
            width: 35px; height: 35px; 
            display: flex; align-items: center; justify-content: center; 
            background: white; border: 1px solid #eee; 
            font-weight: 800; font-size: 18px; cursor: pointer; 
            user-select: none; border-radius: 4px;
        }

        /* Selection & Found Colors */
        .selected { background-color: #a5d8ff !important; color: #1971c2; }
        .found { background-color: #b2f2bb !important; color: #2b8a3e; border-radius: 50%; }

        .word-list { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; justify-content: center; }
        .word-item { font-size: 12px; font-weight: bold; color: #333; text-transform: uppercase; }
        .crossed { text-decoration: line-through; color: #ccc; }
        
        .controls { margin-top: 20px; display: flex; gap: 10px; }
        button.action { padding: 10px 20px; border-radius: 20px; border: none; background: #82c91e; color: white; font-weight: bold; }
    </style>
</head>
<body>

    <div class="word-list" id="wordList"></div>
    
    <div class="grid" id="gridBoard"></div>

    <div style="margin-top:15px; font-weight:bold; color:#1971c2;">Selection: <span id="currentVal">---</span></div>

    <div class="controls">
        <button class="action" onclick="checkWord()">Check Selection</button>
        <button class="action" style="background:#fa5252;" onclick="resetSelection()">Clear</button>
    </div>

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

        let selectedIndices = [];
        let foundWords = [];

        // Build Word List
        function updateWordList() {
            const listDiv = document.getElementById('wordList');
            listDiv.innerHTML = elements.map(e => `<span class="word-item ${foundWords.includes(e) ? 'crossed' : ''}">${e}</span>`).join('');
        }

        // Build Grid
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
            document.getElementById('currentVal').innerText = currentString;
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
                document.getElementById('currentVal').innerText = "FOUND!";
                updateWordList();
            } else {
                alert("Not a valid element!");
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

# 3. Render the Game
components.html(game_html, height=650)

st.markdown("<p style='text-align: center; color: #999;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
