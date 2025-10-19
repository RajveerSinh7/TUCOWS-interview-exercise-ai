# 🧠 Knowledge Assistant RAG System

A **minimal LLM-powered Retrieval-Augmented Generation (RAG)** system designed to assist support teams in responding to customer tickets efficiently. It retrieves relevant policy documentation, generates structured responses using **Mistral's LLM**, and adheres to the **Model Context Protocol (MCP)** for consistent, JSON-formatted outputs.

---

## 🚀 Overview

This Knowledge Assistant analyzes support queries (e.g., domain suspension issues) and delivers actionable insights by:

- **Retrieving top-relevant policy documents** via semantic vector search.  
- **Generating concise, policy-grounded answers** with Mistral's LLM.  
- **Including references** to source documents for transparency.  
- **Suggesting next actions** (e.g., escalation or info requests) for ticket routing.  

The system uses synthetic docs for demo purposes but is extensible to real policy FAQs. It ensures MCP-compliant outputs for seamless integration into support workflows. Fallback mode provides synthetic responses for offline/dev testing without an API key.

---

## 🏗️ System Architecture

```mermaid
graph TB
    A[Client Request] --> B[FastAPI Endpoint: /resolve-ticket]
    B --> C[Query Embedding (Sentence Transformers)]
    C --> D[Vector Search (FAISS IndexFlatL2)]
    D --> E[Top-K Context Retrieval (store.py)]
    E --> F[MCP Prompt Construction (prompting.py)]
    F --> G[LLM Generation (Mistral API or Fallback)]
    G --> H[JSON Parsing & Validation (main.py)]
    H --> I[Structured MCP Response]

    J[Index Build (index_builder.py)] --> D
    K[.env Config (config.py)] --> F
    K --> G
```

---

### Core Components

- **Config (`src/config.py`)** – Environment vars for API keys, models, and paths.  
- **Index Builder (`src/index_builder.py`)** – Embeds synthetic docs and builds FAISS index.  
- **Vector Store (`src/store.py`)** – Loads index and retrieves relevant docs with auto-build on missing files.  
- **Prompting Engine (`src/prompting.py`)** – Constructs MCP-structured prompts with role, context, and JSON schema.  
- **LLM Client (`src/mistral_client.py`)** – Mistral API wrapper with fallback for dev/demo.  
- **API Layer (`src/main.py`)** – FastAPI endpoints for single/batch resolution, with validation and error handling.  

---

## ⚙️ Technical Decisions

### Why Mistral Large?
- Strong instruction-following for MCP JSON outputs.  
- Cost-effective and fast for support-scale queries.  
- API simplicity aligns with structured prompting.  

### Why FAISS?
- Lightweight, in-memory vector search ideal for small-to-medium doc sets.  
- No external deps beyond NumPy; easy local/Docker deployment.  

### Why RAG over Pure LLM?
- Grounds responses in verifiable docs to reduce hallucinations.  
- Enables dynamic updates via re-indexing without retraining.  
- Provides citations for agent trust and auditability.  

### Why Sentence Transformers?
- Open-source and efficient for semantic embeddings without API costs.  
- `all-MiniLM-L6-v2` balances speed and quality for short policy texts.  

### Why FastAPI?
- Async-friendly for scalable endpoints.  
- Auto-generated Swagger docs for easy testing.  
- Pydantic validation ensures clean MCP JSON inputs/outputs.  

---

## 🔧 Installation & Setup

### Local Development (Python)

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/TUCOWS-interview-exercise-ai.git  # Replace with your forked repo
cd TUCOWS-interview-exercise-ai
```

#### 2️⃣ Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure Environment
Create a `.env` file in the project root:
```text
MISTRAL_API_KEY=your-mistral-key  # Optional: Leave blank for fallback
MISTRAL_API_URL=https://api.mistral.ai/v1
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=4
```

#### 5️⃣ Build Index (One-time; embeds synthetic docs)
```bash
python src/index_builder.py
```

#### 6️⃣ Start the Server
```bash
python src/main.py
```

Then open:  
- App: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs  

---

### 🐳 Docker Deployment (Recommended for Demo)

#### Prerequisites
- Docker & Docker Compose installed.

#### Run in Fallback Mode (no API key needed)
```bash
docker compose up --build
```

#### Or Build Manually
```bash
docker build -t knowledge-assistant .
docker run -p 8000:8000 knowledge-assistant
```

With API key:
```bash
docker run -p 8000:8000 -e MISTRAL_API_KEY=sk-your-key knowledge-assistant
```

Logs:
```bash
docker compose logs -f
```

Stop:
```bash
docker compose down
```

---

## 📡 Access

- **Main API:** http://localhost:8000  
- **Swagger Docs:** http://localhost:8000/docs  

### Docker Hub (Prebuilt Image)
```bash
docker pull yourusername/knowledge-assistant:latest  # Replace with yourusername
docker run -p 8000:8000 yourusername/knowledge-assistant
```

---

## 📋 API Endpoints

### 🎯 Resolve Single Ticket
Processes a support query and returns MCP JSON.

```bash
curl -X POST "http://localhost:8000/resolve-ticket"   -H "Content-Type: application/json"   -d '{
    "ticket_text": "My domain was suspended and I didn’t get any notice. How can I reactivate it?"
  }'
```

**Example Response:**
```json
{
  "answer": "Your domain may have been suspended due to missing WHOIS details, unpaid billing, or a policy violation. To reactivate, update your WHOIS information in the account dashboard or verify payment status via billing@example.com.",
  "references": [
    "Policy: Domain Suspension Guidelines, Section 4.2",
    "WHOIS Update Policy",
    "Billing & Payment FAQ"
  ],
  "action_required": "escalate_to_abuse_team"
}
```

---

### 🧩 Resolve Batch Tickets
```bash
curl -X POST "http://localhost:8000/resolve-tickets"   -H "Content-Type: application/json"   -d '[
    {"ticket_text": "My domain was suspended..."},
    {"ticket_text": "Billing issue with payment failure."}
  ]'
```

---

### 🔍 Root Endpoint (Health Check)
```bash
curl -X GET "http://localhost:8000/"
```
**Returns:**  
```json
{"message": "Tucows RAG API: POST to /resolve-ticket with {'ticket_text': 'your query'}"}
```

---
