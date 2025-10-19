# Dockerfile for Knowledge Assistant RAG System
# Builds a containerized FastAPI app with FAISS index auto-build support.

# Use official Python slim image for smaller footprint and security
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for sentence-transformers and FAISS
# (build-essential for compiling native extensions; g++ for FAISS)
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first for better Docker layer caching during pip install
COPY requirements.txt .

# Install Python dependencies without caching to keep image lean
RUN pip install --no-cache-dir -r requirements.txt

# NEW: Add /app/src to PYTHONPATH so absolute imports like 'from store import' resolve to src/store.py
ENV PYTHONPATH=/app/src

# Copy the entire src/ directory (contains all Python modules: main.py, store.py, etc.)
COPY src/ ./src/

# Create data directory for FAISS index (will be populated at runtime if missing)
RUN mkdir -p data/faiss_index

# Expose the port the app runs on
EXPOSE 8000

# Optional: Add a health check to verify the API is responsive
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the FastAPI app with Uvicorn (API remains unchanged in code)
# --reload for dev; remove in prod for performance
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]