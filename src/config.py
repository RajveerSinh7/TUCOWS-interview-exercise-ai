# src/config.py
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FAISS_DIR = os.path.join(DATA_DIR, "faiss_index")
DOCS_DIR = os.path.join(DATA_DIR, "docs")

# Mistral API (set MISTRAL_API_KEY env var for real usage)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "BQsO290WQ5VqmZr335Jpn99wzLiI5Du8")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai/v1")  # adjust if needed

# Embedding model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", "4"))