# 🧠 Knowledge Assistant RAG System

A **minimal LLM-powered Retrieval-Augmented Generation (RAG)** system
designed to assist support teams in responding to customer tickets
efficiently. It retrieves relevant policy documentation, generates
structured responses using **Mistral's LLM**, and adheres to the **Model
Context Protocol (MCP)** for consistent, JSON-formatted outputs.

------------------------------------------------------------------------

## 🚀 Overview

This Knowledge Assistant analyzes support queries (e.g., domain
suspension issues) and delivers actionable insights by:

-   **Retrieving top-relevant policy documents** via semantic vector
    search.
-   **Generating concise, policy-grounded answers** with Mistral's LLM.
-   **Including references** to source documents for transparency.
-   **Suggesting next actions** (e.g., escalation or info requests) for
    ticket routing.

The system supports two approaches for knowledge base documents:

1.  **Hardcoded synthetic docs** (for quick demo purposes).
2.  **User-uploaded docs** via `optional.py` (placed in `support_docs/`
    folder), which are converted into the proper JSON format
    automatically and indexed.

Both approaches ensure MCP-compliant outputs for seamless integration
into support workflows.

------------------------------------------------------------------------

## 🏗️ System Architecture

``` mermaid
graph TB
    A[Client Request] --> B[FastAPI Endpoint: /resolve-ticket]
    B --> C[Query Embedding - Sentence Transformers]
    C --> D[Vector Search - FAISS IndexFlatL2]
    D --> E[Top-K Context Retrieval - store.py]
    E --> F[MCP Prompt Construction - prompting.py]
    F --> G[LLM Generation - Mistral API or Fallback]
    G --> H[JSON Parsing & Validation - main.py]
    H --> I[Structured MCP Response]

    J[Index Build - index_builder.py / optional.py] --> D
    K[.env Config - config.py] --> F
    K --> G
```

------------------------------------------------------------------------

### Core Components

-   **Config (`config.py`)** -- Environment vars for API keys, models,
    and paths.
-   **Index Builder (`index_builder.py`)** -- Embeds hardcoded docs and
    builds FAISS index.
-   **Optional Doc Uploader (`optional.py`)** -- Converts user-uploaded
    `.txt` files in `support_docs/` into JSON format and builds index.
-   **Vector Store (`store.py`)** -- Loads index and retrieves relevant
    docs.
-   **Prompting Engine (`prompting.py`)** -- Constructs MCP-structured
    prompts.
-   **LLM Client (`mistral_client.py`)** -- Mistral API wrapper with
    fallback for demo.
-   **API Layer (`main.py`)** -- FastAPI endpoints for single/batch
    resolution.

------------------------------------------------------------------------

## ⚙️ Technical Decisions

### Why Mistral Large?

-   Strong instruction-following for JSON outputs.
-   Cost-effective and fast for support-scale queries.

### Why FAISS?

-   Lightweight, in-memory vector search ideal for small-to-medium doc
    sets.

### Why RAG over Pure LLM?

-   Grounds responses in verifiable docs to reduce hallucinations.

### Why Sentence Transformers?

-   Open-source and efficient for semantic embeddings.

### Why FastAPI?

-   Async-friendly with built-in docs and schema validation.

------------------------------------------------------------------------

## 🔧 Installation & Setup

### Local Development (Python)

#### 1️⃣ Clone the Repository

``` bash
git clone https://github.com/RajveerSinh7/TUCOWS-interview-exercise-ai.git
cd TUCOWS-interview-exercise-ai
```

#### 2️⃣ Set Up Virtual Environment

``` bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

#### 4️⃣ Configure Environment

Create a `.env` file:

``` text
MISTRAL_API_KEY=your-mistral-key
MISTRAL_API_URL=https://api.mistral.ai/v1
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=4
```

#### 5️⃣ Build Index

-   **Option 1:** Hardcoded docs

``` bash
python src/index_builder.py
```

-   **Option 2:** User-uploaded docs

``` bash
python src/optional.py
```

#### 6️⃣ Start the Server

``` bash
python src/main.py
```

Then open: - App: <http://localhost:8000> - Swagger:
<http://localhost:8000/docs>

#### 7️⃣ Test Endpoint

``` bash
curl -X POST "http://localhost:8000/resolve-tickets" -H "Content-Type: application/json" -d '[{"ticket_text": "My domain was suspended..."}, {"ticket_text": "Billing issue with payment failure."}]'
```

------------------------------------------------------------------------

## 🐳 Docker Deployment

### 1️⃣ Build Image

``` bash
docker build -t knowledge-assistant .
```

### 2️⃣ Run Container

``` bash
docker run -p 8000:8000 knowledge-assistant
```

### 3️⃣ Test API

``` bash
curl -X POST "http://localhost:8000/resolve-tickets" -H "Content-Type: application/json" -d '[{"ticket_text": "My domain was suspended..."}, {"ticket_text": "Billing issue with payment failure."}]'
```

------------------------------------------------------------------------

## 📡 Access

-   API: <http://localhost:8000>
-   Docs: <http://localhost:8000/docs>

------------------------------------------------------------------------

## 📋 Example Response

``` json
{
  "answer": "Your domain may have been suspended due to missing WHOIS details or unpaid billing. To reactivate, update your WHOIS information or verify payment status.",
  "references": [
    "Policy: Domain Suspension Guidelines, Section 4.2",
    "WHOIS Update Policy",
    "Billing & Payment FAQ"
  ],
  "action_required": "escalate_to_abuse_team"
}
```
