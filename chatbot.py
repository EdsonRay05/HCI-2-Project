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

def categorize_podcast_content(text):
    prompt = (
        "You are an assistant. Analyze the following podcast transcript and categorize its content into up to 5 main themes or topics. "
        "For each category, estimate its proportional presence as a percentage of the overall content. "
        "Return ONLY a comma-separated list in the format: Category1: X%, Category2: Y%, etc. The total must be 100%. "
        "Example: Love: 10%, Science: 90%\n\n"
        f"Transcript: \"{text}\"\n\n"
        "Categories:"
    )
    try:
        theme_string = ollama_generate(prompt)
        categories_list = [cat.strip() for cat in theme_string.split(",") if cat.strip()]
        if not categories_list:
            return ["No categories found"]
        return categories_list
    except Exception as e:
        return [f"Categorization unavailable: {str(e)}"]


# Preprocessing function for chatbot responses
# Explore the transcript and generate a response based on user query
# Extract things
# Have prompt to chatbot response, because it doesnt have a prompt, therefore when the user ask a second time, 
# the chatbot didnt remember the first question
def chatbot_response(query, transcript, conversation_history=None):
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

        # Build conversation history string from previous Q&A pairs
        history_text = ""
        for q, a in conversation_history[-5:]:  # limit to last 5 exchanges to keep prompt size manageable
            history_text += f"Q: {q}\nA: {a}\n\n"

        # Construct the prompt including conversation history and transcript context
        prompt = (
            f"You are an assistant. Use the following conversation history and context to answer the question as accurately as possible. "
            f"If the answer is not available, say 'I don't know.'\n\n"
            f"Conversation history:\n{history_text}"
            f"Context: {relevant_chunks}\n\n"
            f"Question: {query}\n"
            f"Answer:"
        )

        answer = ollama_generate(prompt)

        # Optionally, append current QA pair to conversation_history externally in your calling code

        return answer
    except Exception as e:
        return f"Error generating response: {str(e)}"