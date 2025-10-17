import os
import sys

# Add src folder to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import requests
from config import MISTRAL_API_KEY, MISTRAL_API_URL

if not MISTRAL_API_KEY or MISTRAL_API_KEY == "":  # Or check if it's the dummy
    print("Warning: Set a real MISTRAL_API_KEY env var first!")
    exit(1)

url = f"{MISTRAL_API_URL}/models"
headers = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    models = response.json().get("data", [])
    print(f"Success! Available models ({len(models)}):")
    for model in models[:5]:  # Top 5
        print(f"- {model['id']}")
else:
    print(f"API Error: {response.status_code} - {response.text}")