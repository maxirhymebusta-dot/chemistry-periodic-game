import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="First 20 Elements Master", layout="centered")

# 2. Project Header
st.markdown("""
    <div style="text-align: center; margin-top: 10px; margin-bottom: 20px;">
        <h2 style="color: #2b8a3e; font-family: sans-serif; font-weight: 800;">
            🧪 FIRST 20 ELEMENTS: LABORATORY GRID
        </h2>
        <p style="color: #666; font-size: 14px;">Find all chemical names to complete the gate.</p>
    </div>
""", unsafe_allow_html=True)

# 3. THE "FOCUSED" GAME BOX (Now using the correct Component)
# This creates the green-bordered container
st.markdown("""
    <div id="game-container" style="
        width: 100%; 
        max-width: 450px; 
        height: 520px; 
        overflow: hidden; 
        border: 4px solid #82c91e; 
        border-radius: 25px; 
        margin: 0 auto;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        position: relative;">
    </div>
""", unsafe_allow_html=True)

# This part actually injects the game into the screen
with st.container():
    components.html(
        """
        <div style="position: absolute; top: -180px; left: -50px;">
            <iframe 
                src="https://www.educaplay.com/game/28499055-first_8_elements_word_search.html" 
                width="550px" 
                height="800px" 
                style="border: none;"
                allow="fullscreen; autoplay">
            </iframe>
        </div>
        """,
        height=520, 
    )

# 4. Professional Project Footer
st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <hr style="border: 0.5px solid #eee; width: 50%; margin: 20px auto;">
        <p style="color: #999; font-size: 12px; font-weight: bold; letter-spacing: 1px;">
            DEVELOPED BY UKAZIM CHIDINMA FAVOUR
        </p>
    </div>
""", unsafe_allow_html=True)
