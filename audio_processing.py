# audio_processing.py
import requests
from tempfile import NamedTemporaryFile
import streamlit as st
from models import load_whisper_model, load_summarizer, load_sentiment_analyzer

def download_audio(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        tmpfile = NamedTemporaryFile(delete=False, suffix=".mp3")
        with open(tmpfile.name, 'wb') as f:
            f.write(response.content)
        return tmpfile.name
    except Exception as e:
        st.error(f"Error downloading audio: {e}")
        return None

def transcribe_audio(file_path):
    try:
        model = load_whisper_model()
        transcription_result = model.transcribe(file_path)
        return transcription_result['text']
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None

def summarize_text(text, min_length=30, max_length=130):
    try:
        summarizer = load_summarizer()
        summary = summarizer(text, min_length=min_length, max_length=max_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return "Summary unavailable"

def analyze_sentiment(text):
    try:
        analyzer = load_sentiment_analyzer()
        sentences = text.split(". ")
        if not sentences or (len(sentences) == 1 and not sentences[0]):
            return {'positive': 0, 'negative': 0, 'neutral': 100}

        results = analyzer(sentences[:10])
        positive = sum(1 for r in results if r['label'] == 'POSITIVE')
        negative = sum(1 for r in results if r['label'] == 'NEGATIVE')
        neutral = len(results) - positive - negative
        total = len(results)
        if total == 0:
            return {'positive': 0, 'negative': 0, 'neutral': 100}
        return {
            'positive': int((positive / total) * 100),
            'negative': int((negative / total) * 100),
            'neutral': int((neutral / total) * 100)
        }
    except Exception as e:
        st.error(f"Error during sentiment analysis: {e}")
        return {'positive': 0, 'negative': 0, 'neutral': 100}

