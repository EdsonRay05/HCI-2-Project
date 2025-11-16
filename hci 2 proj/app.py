import streamlit as st
import numpy as np

import imageio_ffmpeg
import shutil

ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')

# Debug: show where (if anywhere) 'ffmpeg' is found on PATH
ffmpeg_path = shutil.which("ffmpeg")
if ffmpeg_path:
    st.success(f"ffmpeg binary found at: {ffmpeg_path}")
else:
    st.error("ffmpeg binary NOT found in PATH. PATH is: " + os.environ['PATH'])
    st.info(f"imageio_ffmpeg.get_ffmpeg_exe() points to: {imageio_ffmpeg.get_ffmpeg_exe()}")
    
from config import CLIENT_ID, CLIENT_SECRET
from spotify_api import get_spotify_token, get_episode_preview_url
from audio_processing import download_audio, transcribe_audio, summarize_text, analyze_sentiment
from chatbot import categorize_podcast_content, chatbot_response
from styles import CUSTOM_CSS  # Custom CSS file


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SoundScape",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --- Custom CSS ---
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)



# --- SESSION STATE ---
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'sentiment_data' not in st.session_state:
    st.session_state.sentiment_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'conversion_complete' not in st.session_state:
    st.session_state.conversion_complete = False
if 'current_episode' not in st.session_state:
    st.session_state.current_episode = ""
if 'generated_themes' not in st.session_state:
    st.session_state.generated_themes = []

# --- Branding/Header ---
st.markdown('<div class="brand-name"><span class="brand-sound">Sound</span><span class="brand-scape">Scape</span></div>', unsafe_allow_html=True)
# st.markdown('<div class="subtitle">Transform podcast into readable text</div>', unsafe_allow_html=True)
# Nothing else in this spot—no input widget or empty area!

# --- Input section ---
# st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown("### Enter Spotify Podcast URL")

col1, col2 = st.columns([4, 1])
with col1:
    spotify_url = st.text_input(
        "",
        placeholder="https://open.spotify.com/episode/...",
        label_visibility="collapsed"
    )
with col2:
    convert_button = st.button("Convert", use_container_width=True)

st.markdown("**Supported:** 30s to 1 minute spotify podcast text output")
st.markdown('</div>', unsafe_allow_html=True)

# --- CONVERSION LOGIC ---
if convert_button and spotify_url:
    with st.spinner("🔄 Fetching Episode..."):
        access_token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)
        preview_url, episode_name = get_episode_preview_url(spotify_url, access_token)
        if preview_url:
            st.success(f"✓ Found: {episode_name}")
            st.session_state.current_episode = episode_name
            with st.spinner("⬇️ Downloading audio..."):
                audio_file = download_audio(preview_url)
            if audio_file:
                with st.spinner("🎙️ Transcribing audio (this may take a moment)..."):
                    transcribed_text = transcribe_audio(audio_file)
                if transcribed_text:
                    st.session_state.transcribed_text = transcribed_text
                    st.session_state.chat_history = []
                    with st.spinner("📝 Generating summary..."):
                        st.session_state.summary = summarize_text(transcribed_text)
                    with st.spinner("💭 Analyzing sentiment..."):
                        st.session_state.sentiment_data = analyze_sentiment(transcribed_text)
                    with st.spinner("🌱 Extracting themes..."):
                        st.session_state.generated_themes = categorize_podcast_content(transcribed_text)
                    st.session_state.conversion_complete = True
                    st.rerun()
        else:
            st.error("❌ No preview audio available or invalid URL")

# --- RESULTS DISPLAY ---
if st.session_state.conversion_complete:
    st.markdown('<div class="success-message">✓ Conversion Complete<br>Your podcast has successfully been converted to text</div>', unsafe_allow_html=True)
    if st.session_state.current_episode:
        st.caption(f"📻 Currently viewing: {st.session_state.current_episode}")
    tab1, tab2, tab3, tab4 = st.tabs(["📝 TRANSCRIPT", "📊 SUMMARY", "😊 SENTIMENT", "💬 CHATBOT"])
    with tab1:
        st.markdown("### Full Transcript")
        if st.session_state.transcribed_text:
            #st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.write(st.session_state.transcribed_text)
            #st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No transcript available yet.")
    with tab2:
        st.markdown("### Episode Summary")
        if st.session_state.summary:
            #st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.write(st.session_state.summary)
            #st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No summary available yet.")
    with tab3:
        st.markdown("### OVERALL SENTIMENT")
        col1, col2, col3 = st.columns(3)
        if st.session_state.sentiment_data:
            with col1:
                st.markdown(f'<div class="sentiment-positive">{st.session_state.sentiment_data["positive"]}% Positive</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="sentiment-neutral">{st.session_state.sentiment_data["neutral"]}% Neutral</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="sentiment-negative">{st.session_state.sentiment_data["negative"]}% Negative</div>', unsafe_allow_html=True)
        else:
            st.info("Sentiment data is not available.")
        st.markdown("### CATEGORIZED THEMES")
        if st.session_state.generated_themes:
            cols = st.columns(5)
            for i, theme in enumerate(st.session_state.generated_themes):
                with cols[i % 5]:
                    st.markdown(f'<div class="sentiment-neutral">{theme}</div>', unsafe_allow_html=True)
        else:
            st.info("No common themes were extracted from this episode.")
    with tab4:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown("### Ask About This Episode")
        with col2:
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        st.markdown("Hi! Ask me anything about this podcast episode.")
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message">You: {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message">Chatbot: {message["content"]}</div>', unsafe_allow_html=True)
        with st.form(key="chat_form", clear_on_submit=True):
            user_question = st.text_input("Ask a question...", key="chat_input", label_visibility="collapsed")
            submit_button = st.form_submit_button("Send")
            if submit_button and user_question:
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                with st.spinner("Thinking..."):
                    response = chatbot_response(user_question, st.session_state.transcribed_text)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()








