import streamlit as st
import random

# 1. Page Config & Custom Branding
st.set_page_config(page_title="MSc Periodic Master", page_icon="🧪", layout="wide")

# 2. Custom CSS for "Beautification" and Responsiveness
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: scale(1.02);
    }
    .clue-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #007bff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stats-card {
        text-align: center;
        padding: 10px;
        background: white;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data Dictionary (8 Levels) ---
levels_data = {
    1: {"name": "The Essentials", "data": [
        {"name": "Hydrogen", "symbol": "H", "clue": "Lightest element, atomic number 1."},
        {"name": "Helium", "symbol": "He", "clue": "Noble gas used in balloons."},
        {"name": "Carbon", "symbol": "C", "clue": "Basis of all organic life."},
        {"name": "Oxygen", "symbol": "O", "clue": "Needed for respiration and fires."},
        {"name": "Nitrogen", "symbol": "N", "clue": "78% of Earth's atmosphere."}
    ]},
    2: {"name": "Alkali & Alkaline Earth", "data": [
        {"name": "Sodium", "symbol": "Na", "clue": "Group 1 metal, reacts with water."},
        {"name": "Potassium", "symbol": "K", "clue": "Found in bananas, symbol is K."},
        {"name": "Magnesium", "symbol": "Mg", "clue": "Burns with a bright white flame."},
        {"name": "Calcium", "symbol": "Ca", "clue": "Essential for bones and teeth."},
        {"name": "Lithium", "symbol": "Li", "clue": "Used in rechargeable batteries."}
    ]},
    3: {"name": "The Halogens", "data": [
        {"name": "Fluorine", "symbol": "F", "clue": "Most electronegative element."},
        {"name": "Chlorine", "symbol": "Cl", "clue": "Disinfects swimming pools."},
        {"name": "Bromine", "symbol": "Br", "clue": "Only non-metal liquid at room temp."},
        {"name": "Iodine", "symbol": "I", "clue": "Purple solid antiseptic."},
        {"name": "Astatine", "symbol": "At", "clue": "Rarest natural element."}
    ]},
    4: {"name": "The Noble Gases", "data": [
        {"name": "Neon", "symbol": "Ne", "clue": "Orange advertising signs."},
        {"name": "Argon", "symbol": "Ar", "clue": "Most abundant noble gas."},
        {"name": "Krypton", "symbol": "Kr", "clue": "Named after 'hidden' in Greek."},
        {"name": "Xenon", "symbol": "Xe", "clue": "Used in high-speed flashes."},
        {"name": "Radon", "symbol": "Rn", "clue": "Radioactive gas in soil."}
    ]},
    5: {"name": "Transition Metals", "data": [
        {"name": "Iron", "symbol": "Fe", "clue": "Magnetic, used to make steel."},
        {"name": "Copper", "symbol": "Cu", "clue": "Reddish electrical wiring."},
        {"name": "Zinc", "symbol": "Zn", "clue": "Used to galvanize steel."},
        {"name": "Nickel", "symbol": "Ni", "clue": "Used in stainless steel."},
        {"name": "Titanium", "symbol": "Ti", "clue": "Strong, light aircraft metal."}
    ]},
    6: {"name": "Precious Metals", "data": [
        {"name": "Gold", "symbol": "Au", "clue": "Yellow metal, 'Aurum'."},
        {"name": "Silver", "symbol": "Ag", "clue": "Conducts electricity, 'Argentum'."},
        {"name": "Platinum", "symbol": "Pt", "clue": "Dense jewelry catalyst."},
        {"name": "Mercury", "symbol": "Hg", "clue": "Liquid metal, 'Hydrargyrum'."},
        {"name": "Palladium", "symbol": "Pd", "clue": "Used in catalytic converters."}
    ]},
    7: {"name": "Metalloids & Poor Metals", "data": [
        {"name": "Silicon", "symbol": "Si", "clue": "Used in computer chips."},
        {"name": "Arsenic", "symbol": "As", "clue": "Toxic metalloid symbol As."},
        {"name": "Lead", "symbol": "Pb", "clue": "Heavy metal, 'Plumbum'."},
        {"name": "Tin", "symbol": "Sn", "clue": "Coats cans, symbol Sn."},
        {"name": "Aluminum", "symbol": "Al", "clue": "Light foil and soda cans."}
    ]},
    8: {"name": "Radioactive Elements", "data": [
        {"name": "Uranium", "symbol": "U", "clue": "Nuclear power plant fuel."},
        {"name": "Plutonium", "symbol": "Pu", "clue": "Used in space batteries."},
        {"name": "Radium", "symbol": "Ra", "clue": "Marie Curie's discovery."},
        {"name": "Thorium", "symbol": "Th", "clue": "Radioactive fuel potential."},
        {"name": "Oganesson", "symbol": "Og", "clue": "Last element on the table."}
    ]}
}

# --- Session State ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'q_count' not in st.session_state: st.session_state.q_count = 1
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = random.choice(levels_data[1]['data'])

# --- Header Section ---
st.title("🛡️ Periodic Table: The Grand Quest")
progress = ((st.session_state.level - 1) * 5 + st.session_state.q_count) / 40
st.progress(progress)

# --- Layout: 2 Columns for Stats ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='stats-card'><b>LEVEL</b><br><span style='font-size:24px;color:#007bff'>{st.session_state.level}/8</span></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='stats-card'><b>QUESTION</b><br><span style='font-size:24px;color:#007bff'>{st.session_state.q_count}/5</span></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='stats-card'><b>SCORE</b><br><span style='font-size:24px;color:#007bff'>{st.session_state.score}</span></div>", unsafe_allow_html=True)

st.write("---")

# --- Gameplay ---
if st.session_state.level <= 8:
    st.markdown(f"### 📍 Now Exploring: <span style='color:#007bff'>{levels_data[st.session_state.level]['name']}</span>", unsafe_allow_html=True)
    
    # Clue Box
    st.markdown(f"""
        <div class="clue-box">
            <h4 style="margin:0; color:#555;">Detective Clue:</h4>
            <p style="font-size:18px; color:#111;">{st.session_state.current_q['clue']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input area
    user_ans = st.text_input("Identify the element (Name or Symbol):", placeholder="e.g. Oxygen or O", key=f"inp_{st.session_state.level}_{st.session_state.q_count}")

    if st.button("VERIFY ANSWER"):
        target = st.session_state.current_q
        if user_ans.lower() == target['name'].lower() or user_ans.upper() == target['symbol']:
            st.balloons()
            st.success(f"✅ Correct! That was {target['name']} ({target['symbol']})")
            st.session_state.score += 20
        else:
            st.error(f"❌ Incorrect. It was {target['name']} ({target['symbol']})")

        # Logic to move forward
        if st.session_state.q_count < 5:
            st.session_state.q_count += 1
            st.session_state.current_q = random.choice(levels_data[st.session_state.level]['data'])
            st.rerun()
        else:
            st.session_state.level += 1
            st.session_state.q_count = 1
            if st.session_state.level <= 8:
                st.session_state.current_q = random.choice(levels_data[st.session_state.level]['data'])
                st.toast(f"Level {st.session_state.level-1} Cleared!", icon='🔥')
                st.rerun()
            else:
                st.rerun()
else:
    st.header("🏆 YOU ARE A MASTER CHEMIST!")
    st.balloons()
    st.metric("FINAL SCORE", st.session_state.score, "out of 800")
    if st.button("PLAY AGAIN"):
        st.session_state.level = 1
        st.session_state.q_count = 1
        st.session_state.score = 0
        st.session_state.current_q = random.choice(levels_data[1]['data'])
        st.rerun()
