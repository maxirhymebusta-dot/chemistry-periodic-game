import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="First 20 Elements", layout="centered")

# 2. Professional Header (Matches your request)
st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #2b8a3e; margin-bottom: 0;">🧪 First 20 Elements Word Search</h1>
        <p style="color: #666; font-style: italic;">Mastering Chemical Symbols through Play</p>
    </div>
""", unsafe_allow_html=True)

# 3. THE "CLEAN" EMBED (Focusing only on the Start/Game area)
# We use a div with 'overflow: hidden' to crop out the ads and website menus
st.markdown("""
    <div style="display: flex; justify-content: center; overflow: hidden; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <iframe 
            src="https://www.educaplay.com/game/28499055-first_8_elements_word_search.html" 
            width="400" 
            height="600" 
            style="border:none; margin-top: -60px;" 
            allow="fullscreen; autoplay">
        </iframe>
    </div>
""", unsafe_allow_html=True)

# 4. Professional Footer
st.markdown("<br><p style='text-align: center; color: #999; font-size: 14px;'>Developed by Ukazim Chidinma Favour</p>", unsafe_allow_html=True)
