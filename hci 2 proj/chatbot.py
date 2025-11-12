# chatbot.py
from models import load_embedding_model
from sentence_transformers import util
import requests
import json

def ollama_generate(prompt, model_name="deepseek-r1:1.5b-qwen-distill-q8_0"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "options": {"temperature": 0.8, "top_p": 0.95, "max_tokens": 200}
            },
            stream=True,
            timeout=30
        )
        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        output += data["response"]
                except:
                    continue
        return output.strip()
    except Exception as e:
        return f"Error: {str(e)}. Make sure Ollama is running locally."

def extract_themes(text):
    prompt = f"""You are an assistant. Analyze the following transcript and identify the top 5-7 main themes. 
        Return ONLY a comma-separated list of these themes. Do not add any other text, intro, or explanation.
        Example: Personal Growth, Career Advice, Tech Trends

        Transcript: "{text}"

        Themes: """
    try:
        theme_string = ollama_generate(prompt)
        themes_list = [theme.strip() for theme in theme_string.split(",") if theme.strip()]
        if not themes_list:
            return ["No themes found"]
        return themes_list
    except Exception as e:
        return ["Themes unavailable"]

# Preprocessing function for chatbot responses
# Explore the transcript and generate a response based on user query
# Extract things
# Have prompt to chatbot response, because it doesnt have a prompt, therefore when the user ask a second time, 
# the chatbot didnt remember the first question
def chatbot_response(query, transcript):
    if not transcript:
        return "Please convert a podcast first before asking questions."
    try:
        embedding_model = load_embedding_model()
        transcript_chunks = transcript.split(". ")
        chunk_embeddings = embedding_model.encode(transcript_chunks, convert_to_tensor=True)
        query_embedding = embedding_model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, chunk_embeddings, top_k=3)
        relevant_chunks = " ".join([transcript_chunks[hit['corpus_id']] for hit in hits[0]])
        prompt = f"Context: {relevant_chunks}\n\nQuestion: {query}\nAnswer:"
        return ollama_generate(prompt)
    except Exception as e:
        return f"Error generating response: {str(e)}"