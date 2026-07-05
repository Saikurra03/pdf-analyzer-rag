import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# ===========================================
# Load Environment Variables
# ===========================================

load_dotenv()

try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", None)
except Exception:
    GROQ_API_KEY = None

if not GROQ_API_KEY:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===========================================
# Configure Groq Client
# ===========================================

groq_client = Groq(api_key=GROQ_API_KEY)

GROQ_MODEL = "llama-3.3-70b-versatile"

# ===========================================
# Load Embedding Model
# ===========================================

print("\nLoading Embedding Model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding Model Loaded Successfully!")
