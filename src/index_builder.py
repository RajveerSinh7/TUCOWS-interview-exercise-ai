# src/index_builder.py
import os
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from config import FAISS_DIR, EMBEDDING_MODEL

os.makedirs(FAISS_DIR, exist_ok=True)

# Synthetic docs for demonstration.
DOCS = [
    {
        "id": "domain_suspension",
        "title": "Policy: Domain Suspension Guidelines, Section 4.2",
        "text": "Domains may be suspended for policy violations, missing WHOIS information, or unpaid billing. To reactivate, update WHOIS details, confirm payment, or contact support via abuse@example.com."
    },
    {
        "id": "whois_policy",
        "title": "WHOIS Update Policy",
        "text": "Whois must be up-to-date. Update your contact details in the account dashboard. Missing WHOIS can lead to suspension notices."
    },
    {
        "id": "billing_faq",
        "title": "Billing & Payment FAQ",
        "text": "Payment failures cause interruptions. Update card details or contact billing@example.com to resolve payment holds."
    },
    {
        "id": "abuse_escalation",
        "title": "Abuse Escalation SOP",
        "text": "If abuse is suspected escalate to the abuse team. Provide ticket ID, domain, and evidence when escalating."
    }
]

def build_index():
    print("Loading embedding model:", EMBEDDING_MODEL)
    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [d["text"] for d in DOCS]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, os.path.join(FAISS_DIR, "index.faiss"))

    with open(os.path.join(FAISS_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(DOCS, f, ensure_ascii=False, indent=2)

    print("Built FAISS index and saved metadata to", FAISS_DIR)

if __name__ == "__main__":
    build_index()