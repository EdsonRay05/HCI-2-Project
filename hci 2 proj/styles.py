# styles.py
CUSTOM_CSS = """
<style>
    /* Main background */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }

    /* Header styling */
    h1 {
        color: #ffffff;
        font-size: 3.5rem !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .brand-name {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .brand-sound {
        color: #ffffff;
    }

    .brand-scape {
        color: #00d66f;
    }

    .subtitle {
        color: #ffffff;
        font-size: 1.2rem;
        margin-bottom: 0rem;
        padding-bottom: 0rem;
    }

    /* Input container */
    .input-container {
        background-color: #2a2a2a;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
    }

    /* Button styling */
    .stButton > button {
        background-color: #00d66f;
        color: #000000;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background-color: #00ff80;
        transform: translateY(-2px);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #2a2a2a;
        color: #ffffff;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: #00d66f;
        color: #000000;
    }

    /* Sentiment badges */
    .sentiment-positive {
        background-color: #00d66f;
        color: #000000;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
        margin: 0.25rem;
    }

    .sentiment-neutral {
        background-color: #666666;
        color: #ffffff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
        margin: 0.25rem;
    }

    .sentiment-negative {
        background-color: #dc143c;
        color: #ffffff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
        margin: 0.25rem;
    }

    /* Chat messages */
    .chat-message {
        background-color: #2a2a2a;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    /* Content boxes */
    .content-box {
        background-color: #2a2a2a;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    /* Success message */
    .success-message {
        background-color: #00d66f;
        color: #000000;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0;
    }
</style>
"""
