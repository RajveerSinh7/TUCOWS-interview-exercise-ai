import os
import sys

# ✅ Add src directory to path dynamically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# ✅ Import configuration
from config import *

print("Config loaded successfully!")
print(f"BASE_DIR: {BASE_DIR}")
print(f"DATA_DIR: {DATA_DIR}")
print(f"FAISS_DIR: {FAISS_DIR}")
print(f"DOCS_DIR: {DOCS_DIR}")
print(f"MISTRAL_API_KEY: {MISTRAL_API_KEY[:5]}...{MISTRAL_API_KEY[-4:]}")  # Partial for security
print(f"MISTRAL_API_URL: {MISTRAL_API_URL}")
print(f"EMBEDDING_MODEL: {EMBEDDING_MODEL}")
print(f"TOP_K: {TOP_K}")