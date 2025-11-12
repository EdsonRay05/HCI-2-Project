# models.py
import whisper
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

@st.cache_resource
def load_sentiment_analyzer():
    return pipeline("sentiment-analysis")

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')