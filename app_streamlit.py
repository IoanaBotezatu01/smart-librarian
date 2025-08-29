# app_streamlit.py
import streamlit as st
from chatbot import RAGChatbot
from utils import is_offensive, maybe_tts, maybe_image

st.set_page_config(page_title="Smart Librarian", page_icon="📚")

st.title("📚 Smart Librarian")

if "bot" not in st.session_state:
    st.session_state.bot = RAGChatbot()

with st.sidebar:
    st.markdown("### Options")
    tts = st.checkbox("Generate audio (TTS)")
    img = st.checkbox("Generate book cover image")

q = st.text_input("Your question:", placeholder="I want a book about friendship and magic")

if st.button("Ask") and q:
    if is_offensive(q):
        st.warning("⚠️ Please phrase your question politely. Your input was blocked.")
    else:
        ans = st.session_state.bot.ask(q)
        st.markdown(ans)

        if tts:
            path = maybe_tts(ans)
            if path:
                st.success(f"Audio saved: {path}")
                st.audio(path)
        if img:
            ipath = maybe_image(q, ans)
            if ipath:
                st.image(ipath, caption="Generated cover")
