import os
import sys
import json

# ✅ Allow importing from /src directory even when running from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from prompting import build_prompt
from store import retrieve
from config import TOP_K


def test_prompting():
    print("🧠 Testing prompt builder...")
    
    # Sample ticket
    ticket = "Customer's domain is suspended due to missing WHOIS."
    
    # Get sample context (auto-loads store)
    context_docs = retrieve(ticket, top_k=TOP_K)
    if not context_docs:
        print("❌ No context—run index_builder.py first!")
        return
    
    # Build prompt
    prompt = build_prompt(context_docs, ticket)
    print(f"📝 Generated Prompt (first 500 chars):\n{prompt[:500]}...")
    print(f"\n(Full length: {len(prompt)} chars)")
    
    # Optional: Mock LLM response (in prod, call Mistral)
    mock_response = {
        "answer": "Update WHOIS details to reactivate the domain.",
        "references": [doc["title"] for doc in context_docs[:2]],
        "action_required": "request_user_info"
    }
    print(f"\n🤖 Mock JSON Response:\n{json.dumps(mock_response, indent=2)}")

if __name__ == "__main__":
    test_prompting()