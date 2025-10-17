import os
import requests
import json
from config import MISTRAL_API_KEY, MISTRAL_API_URL

def generate_with_mistral(prompt: str, max_tokens: int = 256, temperature: float = 0.0) -> str:
    """
    Minimal wrapper for Mistral-like HTTP API.
    If MISTRAL_API_KEY is not set, return a safe fallback (synthetic JSON) for dev/demo.
    """
    if not MISTRAL_API_KEY:
        
        fallback = {"answer": "", "references": [], "action_required": "request_user_info"}
        try:
            # crude extraction of first context title
            parts = prompt.split("CONTEXT:")[1].split("TICKET:")[0].strip()
            first_line = parts.split("\n\n")[0]
            if ":" in first_line:
                title = first_line.split(":")[0].strip()
                fallback["references"] = [title]
                fallback["answer"] = f"{title} suggests: Please check the referenced policy and contact support."
                fallback["action_required"] = "request_user_info"
            else:
                fallback["answer"] = "Please update WHOIS or contact support."
                fallback["references"] = ["Policy: Domain Suspension Guidelines, Section 4.2"]
                fallback["action_required"] = "request_user_info"
        except Exception:
            fallback = {
                "answer": "Please update WHOIS details or contact support.",
                "references": ["Policy: Domain Suspension Guidelines, Section 4.2"],
                "action_required": "request_user_info"
            }
        return json.dumps(fallback)
    
    # Real API call (Mistral chat completions format)
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-large-latest",  # Or "mistral-medium-latest" for speed/cost
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    url = f"{MISTRAL_API_URL}/chat/completions"
    resp = requests.post(url, json=payload, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    
    # Extract generated text (Mistral response format)
    if isinstance(data, dict) and "choices" in data:
        text = data["choices"][0]["message"]["content"]
        return text
    return str(data)  # Fallback if format unexpected