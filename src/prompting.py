# src/prompting.py
PROMPT_TEMPLATE = """SYSTEM:
You are a concise Knowledge Assistant for the support team. Follow the Model Context Protocol (MCP) exactly.

CONTEXT:
{context}

TICKET:
{ticket}

OUTPUT FORMAT:
Return only valid JSON with EXACT keys: answer, references, action_required.

Possible action_required values:
escalate_to_abuse_team, request_user_info, update_whois, reset_password, close_no_action, contact_billing, forward_to_engineering

RULES:
1) Use only CONTEXT for factual claims. 2) References must be titles present in CONTEXT. 3) Answer <= 2 sentences. 4) Return STRICT JSON only (no surrounding text).

Now produce the JSON.
"""

def build_prompt(context_docs, ticket):
    ctx = "\n\n".join([f"{d['title']}: {d['text']}" for d in context_docs])
    return PROMPT_TEMPLATE.format(context=ctx, ticket=ticket)