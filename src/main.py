from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List  
from store import retrieve
from prompting import build_prompt
from mistral_client import generate_with_mistral
import json
import uvicorn
import logging
import os
import re  

app = FastAPI(title="RAG Knowledge Assistant - MCP")
logger = logging.getLogger("uvicorn")

class TicketIn(BaseModel):
    ticket_text: str

def strip_markdown_json(text: str) -> str:
    text = re.sub(r'^```json\s*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?```$', '', text, flags=re.MULTILINE)
    return text.strip()

@app.get("/")
def root():
    return {"message": "Tucows RAG API: POST to /resolve-ticket with {'ticket_text': 'your query'} for policy-based resolutions. See /docs for Swagger."}

@app.post("/resolve-ticket")
def resolve_ticket(payload: TicketIn):
    ticket = payload.ticket_text
    # Retrieve relevant docs
    docs = retrieve(ticket)
    if not docs:
        raise HTTPException(status_code=404, detail="No relevant policies found for this ticket.")
    # Build prompt (MCP)
    prompt = build_prompt(docs, ticket)
    # Generate
    try:
        raw = generate_with_mistral(prompt, max_tokens=256)
    except Exception as e:
        logger.exception("LLM error")
        raise HTTPException(status_code=500, detail=str(e))
    # Parse JSON from model output
    try:
        # Strip markdown and load
        clean_raw = strip_markdown_json(raw)
        result = json.loads(clean_raw)
        # Validate keys
        if not all(k in result for k in ("answer", "references", "action_required")):
            raise ValueError("Missing keys in result")
    except Exception as e:
        # Return helpful error including raw LLM output for debugging
        raise HTTPException(status_code=500, detail=f"LLM output parse error: {e}\nRaw output:\n{raw}")
    return result

@app.post("/resolve-tickets")
def resolve_tickets(payload: List[TicketIn]):
    results = []
    for item in payload:
        result = resolve_ticket(item)  # No .dict() needed—returns dict
        results.append(result)
    return results

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=False)