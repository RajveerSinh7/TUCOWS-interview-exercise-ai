import os
from dotenv import load_dotenv

# Load environment variables from .env in parent directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATA_DIR = os.path.join(BASE_DIR, "data")
FAISS_DIR = os.path.join(DATA_DIR, "faiss_index")
DOCS_DIR = os.path.join(DATA_DIR, "docs")

# Mistral API 
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai/v1")

# Embedding model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", "4"))