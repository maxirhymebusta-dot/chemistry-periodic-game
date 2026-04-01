import streamlit as st
import random

# 1. Page Config & Professional Styling
st.set_page_config(page_title="Atomic Unscrambler", layout="centered")

st.markdown("""
<style>
    .letter-btn {
        margin: 5px; font-size: 20px !important; font-weight: bold !important;
        height: 50px; width: 50px; border-radius: 10px !important;
        border: 2px solid #82c91e !important; background-color: #ffffff;
    }
    .slot-btn {
        margin: 5px; font-size: 20px !important; font-weight: bold !important;
        height: 50px; width: 50px; border-radius: 10px !important;
        border: 2px dashed #1971c2 !important; background-color: #f0f7ff;
        color: #1971c2;
    }
    .header-text { text-align: center; color: #2b8a3e; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 2. Data: First 20 Elements (Ordered by Difficulty)
ELEMENT_LIST = [
    "NEON", "BORON", "HELIUM", "OXYGEN", "SODIUM", "CARBON", 
    "SULPHUR", "LITHIUM", "SILICON", "CHLORINE", "FLUORINE", 
    "ALUMINIUM", "MAGNESIUM", "POTASSIUM", "BERYLLIUM", "PHOSPHORUS"
]

# 3. Game State Management
if 'lvl' not in st.session_state: st.session_state.lvl = 0
if 'scrambled' not in st.session_state: 
    word = ELEMENT_LIST[st.session_state.lvl]
    s_list = list(word)
    random.shuffle(s_list)
    st.session_state.scrambled = s_list
if 'answer' not in st.session_state: st.session_state.answer = []

# 4. UI Header
st.markdown(f"<h2 class='header-text'>🔬 Level {st.session_state.lvl + 1}: Unscramble the Element</h2>", unsafe_allow_html=True)
st.write(f"**Target:** {len(ELEMENT_LIST[st.session_state.lvl])} Letters")

# 5. THE ANSWER SLOTS (Where letters go when tapped)
st.markdown("### Your Answer")
cols_ans = st.columns(10)
for i in range(len(ELEMENT_LIST[st.session_state.lvl])):
    with cols_ans[i]:
        char = st.session_state.answer[i] if i < len(st.session_state.answer) else ""
        if st.button(char, key=f"ans_{i}"):
            if char != "": # If they tap a filled slot, remove the letter
                st.session_state.scrambled.append(st.session_state.answer.pop(i))
                st.rerun()

# 6. THE SCRAMBLED LETTERS (The pool to pick from)
st.write("---")
st.markdown("### Scrambled Pool")
cols_pool = st.columns(10)
for i, char in enumerate(st.session_state.scrambled):
    with cols_pool[i % 10]:
        if st.button(char, key=f"pool_{i}_{char}"):
            st.session_state.answer.append(char)
            st.session_state.scrambled.pop(i)
            st.rerun()

# 7. WIN LOGIC
current_word = "".join(st.session_state.answer)
target_word = ELEMENT_LIST[st.session_state.lvl]

if current_word == target_word:
    st.balloons()
    st.success(f"✅ Correct! It's {target_word}!")
    if st.button("NEXT LEVEL 🚀"):
        st.session_state.lvl += 1
        if st.session_state.lvl < len(ELEMENT_LIST):
            # Reset for next level
            next_word = ELEMENT_LIST[st.session_state.lvl]
            s_list = list(next_word)
            random.shuffle(s_list)
            st.session_state.scrambled = s_list
            st.session_state.answer = []
            st.rerun()
        else:
            st.success("🏆 YOU COMPLETED ALL LEVELS!")

# 8. Footer
st.write("---")
if st.button("Reset Level ♻️"):
    st.session_state.answer = []
    word = ELEMENT_LIST[st.session_state.lvl]
    s_list = list(word)
    random.shuffle(s_list)
    st.session_state.scrambled = s_list
    st.rerun()

st.markdown("<p style='text-align: center; color: grey;'>MSc Project | Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
