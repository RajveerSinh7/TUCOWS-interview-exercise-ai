import os
import sys
import json

# ✅ Ensure imports work even when run from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from store import load_store, retrieve
from config import FAISS_DIR, TOP_K


def test_store():
    print("🧠 Testing store load...")
    try:
        success = load_store()
        if success:
            print("✅ Store loaded successfully!")
            
            # Quick metadata peek
            index_path = os.path.join(FAISS_DIR, "index.faiss")
            meta_path = os.path.join(FAISS_DIR, "meta.json")
            with open(meta_path, "r") as f:
                docs = json.load(f)
            print(f"📄 Loaded {len(docs)} docs from meta.json:")
            for doc in docs:
                print(f"  - {doc['id']}: {doc['title'][:50]}...")
            
            # Test retrieval
            print("\n🔍 Testing retrieval...")
            query = "domain suspension policy"  # Sample ticket text
            results = retrieve(query, top_k=TOP_K)
            print(f"  Found {len(results)} matches for '{query}':")
            for i, doc in enumerate(results, 1):
                print(f"    {i}. {doc['id']} (score: {doc['score']:.4f}): {doc['title']}")
                print(f"       {doc['text'][:100]}...")
        else:
            print("❌ Load failed!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_store()