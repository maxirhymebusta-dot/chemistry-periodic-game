import streamlit as st
import streamlit.components.v1 as components

# 1. Page Setup
st.set_page_config(page_title="Chemical Word Search", layout="wide")

# 2. Centered Title
st.markdown("<h1 style='text-align: center; color: #82c91e;'>🔍 First 8 Elements: Word Search</h1>", unsafe_allow_html=True)
st.write("---")

# 3. The Embed Code
# We use a container to make sure the iframe stays centered
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # This is the exact iframe code for your Educaplay game
    # Height is set to 700 to ensure the full game board and timer are visible
    components.html(
        """
        <iframe 
            src="https://www.educaplay.com/game/28499055-first_8_elements_word_search.html" 
            width="100%" 
            height="700" 
            frameborder="0" 
            allow="fullscreen; autoplay" 
            allowfullscreen>
        </iframe>
        """,
        height=720, # This height matches the iframe + a little extra padding
    )

# 4. Footer
st.markdown("<p style='text-align: center; color: grey;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
