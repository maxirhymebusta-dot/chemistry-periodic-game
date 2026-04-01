import streamlit as st
import random

# 1. Page Config
st.set_page_config(page_title="Atomic Matcher", layout="centered")

# 2. Custom CSS for a Professional "Lab" look
st.markdown("""
<style>
    .element-card {
        padding: 15px; border-radius: 10px; border: 2px solid #82c91e;
        text-align: center; font-weight: bold; margin: 10px 0; cursor: pointer;
        background-color: #f8f9fa; transition: 0.3s;
    }
    .selected { background-color: #a5d8ff !important; border-color: #1971c2 !important; }
    .matched { background-color: #b2f2bb !important; border-color: #2b8a3e !important; color: #2b8a3e; }
</style>
""", unsafe_allow_html=True)

# 3. Data: First 20 Elements
DATA = [
    {"sym": "H", "name": "Hydrogen"}, {"sym": "He", "name": "Helium"},
    {"sym": "Li", "name": "Lithium"}, {"sym": "Be", "name": "Beryllium"},
    {"sym": "B", "name": "Boron"}, {"sym": "C", "name": "Carbon"},
    {"sym": "N", "name": "Nitrogen"}, {"sym": "O", "name": "Oxygen"}
] # You can easily add all 20 here

if 'score' not in st.session_state: st.session_state.score = 0
if 'selected_sym' not in st.session_state: st.session_state.selected_sym = None
if 'matches' not in st.session_state: st.session_state.matches = []

st.title("🧪 Atomic Matcher")
st.write("Match the **Symbol** to the **Full Name**.")

# 4. Game Logic & UI
col1, col2 = st.columns(2)

# Column 1: Symbols
with col1:
    st.subheader("Symbols")
    for item in DATA:
        is_matched = item['sym'] in st.session_state.matches
        label = f"✨ {item['sym']}" if is_matched else item['sym']
        if st.button(label, key=f"sym_{item['sym']}", disabled=is_matched, use_container_width=True):
            st.session_state.selected_sym = item['sym']

# Column 2: Names
with col2:
    st.subheader("Names")
    # Shuffle names so they aren't directly across from the symbol
    shuffled_data = sorted(DATA, key=lambda x: x['name']) 
    for item in shuffled_data:
        is_matched = item['sym'] in st.session_state.matches
        label = f"✅ {item['name']}" if is_matched else item['name']
        
        if st.button(label, key=f"name_{item['name']}", disabled=is_matched, use_container_width=True):
            if st.session_state.selected_sym == item['sym']:
                st.session_state.matches.append(item['sym'])
                st.toast(f"Correct! {item['sym']} is {item['name']}", icon="🧪")
                st.session_state.score += 10
                st.session_state.selected_sym = None
                st.rerun()
            else:
                st.error("Try again!")

# 5. Progress
st.divider()
st.progress(len(st.session_state.matches) / len(DATA))
st.write(f"**Score:** {st.session_state.score} | **Found:** {len(st.session_state.matches)}/{len(DATA)}")

if len(st.session_state.matches) == len(DATA):
    st.balloons()
    st.success("Congratulations! You've mastered the first elements!")
    if st.button("Restart Experiment"):
        st.session_state.clear()
        st.rerun()

st.markdown("<p style='text-align: center; color: grey;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
                
