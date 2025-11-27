import streamlit as st
from groq import Groq  # Import Groq
from models import load_embedding_model
from sentence_transformers import util
import requests
import json

# This is our new function that calls the Groq API
def groq_generate(prompt, model_name="llama-3.3-70b-versatile"):
    """Calls the Groq API to generate a response."""
    try:
        # Get the API key from Streamlit secrets
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=model_name,
            temperature=0.7,
            max_tokens=250,
            top_p=1,
            stream=False,
        )
        
        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        # This print statement is for debugging in your terminal
        print(f"FULL GROQ ERROR: {e}") 
        
        # Display a user-friendly error in the Streamlit app
        st.error(f"Error communicating with Groq API: {e}")
        return "Sorry, I couldn't get a response from the AI model."

# chatbot.py

def categorize_podcast_content(text):
    # This prompt now asks the AI to return percentages
    prompt = (
        "You are an assistant. Analyze the following podcast transcript and categorize its content "
        "into up to 5 main themes or topics. "
        "For each category, estimate its proportional presence as a percentage. "
        "Return ONLY a comma-separated list in the format: Category1: X%, Category2: Y% "
        "Example: Habits: 40%, Psychology: 30%, Self-Improvement: 30%\n\n"
        f"Transcript: \"{text}\"\n\n"
        "Categories:"
    )
    try:
        # Call the groq_generate function
        theme_string = groq_generate(prompt)
        categories_list = [cat.strip() for cat in theme_string.split(",") if cat.strip()]
        if not categories_list:
            return ["No categories found"]
        return categories_list
    except Exception as e:
        return [f"CategorVization unavailable: {str(e)}"]

def chatbot_response(query, transcript, summary, conversation_history=None):
    if not transcript:
        return "Please convert a podcast first before asking questions."
    if conversation_history is None:
        conversation_history = []
        
    try:
        embedding_model = load_embedding_model()
        transcript_chunks = transcript.split(". ")
        chunk_embeddings = embedding_model.encode(transcript_chunks, convert_to_tensor=True)
        query_embedding = embedding_model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, chunk_embeddings, top_k=3)
        relevant_chunks = " ".join([transcript_chunks[hit['corpus_id']] for hit in hits[0]])

        # Build conversation history string
        history_text = ""
        for msg in conversation_history[-5:]: # Get last 5 messages
            if msg['role'] == 'user':
                history_text += f"Q: {msg['content']}\n"
            else:
                history_text += f"A: {msg['content']}\n"

        # **FIXED**: The prompt now includes the summary
        prompt = (
            f"You are an assistant. Use the following conversation history, episode summary, and specific context to answer the question. "
            f"If the answer is not in the provided information, say 'I don't know.'\n\n"
            f"Conversation history:\n{history_text}\n"
            f"Episode Summary: {summary}\n"  # <-- THIS IS THE FIX
            f"Specific Context (from transcript): {relevant_chunks}\n\n"
            f"Question: {query}\n"
            f"Answer:"
        )

        # Call the new groq_generate function
        answer = groq_generate(prompt)
        return answer
        
    except Exception as e:
        return f"Error generating response: {str(e)}"
