import os
import sys
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ✅ Add src folder to sys.path dynamically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from index_builder import build_index
from config import FAISS_DIR, EMBEDDING_MODEL

def test_build():
    print("Running index build...")
    build_index()  # This will load model, embed, save index & meta
    
    # Verify outputs
    index_path = os.path.join(FAISS_DIR, "index.faiss")
    meta_path = os.path.join(FAISS_DIR, "meta.json")
    
    if os.path.exists(index_path) and os.path.exists(meta_path):
        print("✅ Files created successfully!")
        
        # Quick metadata check
        with open(meta_path, "r") as f:
            docs = json.load(f)
        print(f"📄 Loaded {len(docs)} docs from meta.json:")
        for doc in docs:
            print(f"  - {doc['id']}: {doc['title'][:50]}...")
        
        # Quick index check (load & dummy search)
        print("\n🔍 Testing index load & search...")
        model = SentenceTransformer(EMBEDDING_MODEL)
        index = faiss.read_index(index_path)
        query = "domain suspension"  # Sample query
        query_emb = model.encode([query]).astype('float32')
        distances, indices = index.search(query_emb, k=2)
        print(f"  Top matches for '{query}':")
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx != -1:
                doc = docs[idx]
                print(f"    {i+1}. {doc['id']} (dist: {dist:.4f}): {doc['text'][:100]}...")
    else:
        print("❌ Files not found—build failed!")

if __name__ == "__main__":
    test_build()