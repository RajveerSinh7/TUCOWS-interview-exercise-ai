import os
import sys
import json
import re

# ✅ Ensure `src` is importable from anywhere
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from mistral_client import generate_with_mistral
from prompting import build_prompt
from store import retrieve
from config import TOP_K

def strip_markdown_json(text: str) -> str:
    text = re.sub(r'^```json\s*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?```$', '', text, flags=re.MULTILINE)
    return text.strip()

def test_client(sample_ticket="Domain suspended due to billing—help!"):
    print("🧠 Testing Mistral client...")
    
    # Get context
    context_docs = retrieve(sample_ticket, top_k=TOP_K)
    if not context_docs:
        print("❌ No context—run index_builder.py!")
        return
    
    # Build prompt
    prompt = build_prompt(context_docs, sample_ticket)
    print(f"📝 Prompt preview: {prompt[:200]}...")
    
    # Generate
    response = generate_with_mistral(prompt, max_tokens=200, temperature=0.0)
    print(f"\n🤖 Raw Response: {repr(response)[:300]}...")  # repr() shows escapes
    
    # Parse & show (with markdown strip)
    try:
        clean_response = strip_markdown_json(response)
        parsed = json.loads(clean_response)
        print(f"\n✅ Parsed JSON:")
        print(f"  Answer: {parsed.get('answer', 'N/A')}")
        print(f"  References: {parsed.get('references', [])}")
        print(f"  Action: {parsed.get('action_required', 'N/A')}")
    except json.JSONDecodeError as e:
        print(f"❌ Still invalid JSON: {e}")
        print("Raw for debug:", repr(clean_response))

if __name__ == "__main__":
    test_client()