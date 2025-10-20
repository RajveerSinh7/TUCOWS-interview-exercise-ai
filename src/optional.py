# src/index_builder.py
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import FAISS_DIR, EMBEDDING_MODEL

# Optional: Install PyMuPDF for PDF parsing
# pip install PyMuPDF
import fitz  # PyMuPDF

# Directory containing your support docs
DOCS_DIR = "support_docs"  # <-- put all your .txt/.pdf files here
os.makedirs(FAISS_DIR, exist_ok=True)

def load_docs():
    docs = []
    for filename in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, filename)
        if filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        elif filename.endswith(".pdf"):
            doc = fitz.open(path)
            text = " ".join([page.get_text() for page in doc])
        else:
            continue  # skip unsupported files

        docs.append({
            "id": filename.split(".")[0],
            "title": filename,
            "text": text.strip()
        })
    return docs

def build_index():
    docs = load_docs()
    if not docs:
        raise ValueError(f"No .txt or .pdf documents found in {DOCS_DIR}!")

    print("Loading embedding model:", EMBEDDING_MODEL)
    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [d["text"] for d in docs]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, os.path.join(FAISS_DIR, "index.faiss"))

    with open(os.path.join(FAISS_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    print(f"Built FAISS index with {len(docs)} documents and saved metadata to {FAISS_DIR}")

if __name__ == "__main__":
    build_index()