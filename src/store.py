# src/store.py
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from config import FAISS_DIR, EMBEDDING_MODEL, TOP_K

_model = None
_index = None
_meta = None

def load_store():
    global _model, _index, _meta
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    idx_path = os.path.join(FAISS_DIR, "index.faiss")
    meta_path = os.path.join(FAISS_DIR, "meta.json")
    if not os.path.exists(idx_path) or not os.path.exists(meta_path):
        raise FileNotFoundError("FAISS index or meta.json not found. Run src/index_builder.py first.")
    _index = faiss.read_index(idx_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        _meta = json.load(f)
    return True

def retrieve(ticket_text, top_k=TOP_K):
    global _model, _index, _meta
    if _index is None or _meta is None or _model is None:
        load_store()
    vec = _model.encode([ticket_text], convert_to_numpy=True)
    D, I = _index.search(vec, top_k)
    results = []
    for j, idx in enumerate(I[0]):
        if idx < len(_meta):
            item = _meta[idx].copy()
            item["score"] = float(D[0][j])
            results.append(item)
    return results