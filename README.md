# AI-Powered Academic Support System (RAG API)

FastAPI service that ingests PDF course material into a Qdrant vector database and generates syllabus-aligned notes using a retriever + LLM.

## Features
- PDF ingestion: extract text, chunk, embed, and upsert into Qdrant collections.
- Retrieval: similarity search with optional metadata filters.
- Notes generation: chapter-level or topic-level notes via an LLM provider.

## Tech Stack
- API: FastAPI + Uvicorn
- Vector DB: Qdrant
- Embeddings: `sentence-transformers` (default) or OpenAI embeddings
- LLM: Google Gemini (default) or local model adapter

## Project Layout
- `app/main.py`: FastAPI app + router registration
- `app/routers/ingestion.py`: `/api/v1/*` ingestion endpoints
- `app/routers/inference.py`: `/api/v1/*` notes generation endpoint
- `app/services/*`: ingestion, retrieval, and generation orchestration
- `app/adapters/*`: pluggable vector DB / embeddings / LLM providers

## Setup

### 1) Create a virtual environment + install deps
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run Qdrant
If you don’t already have Qdrant running locally:
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 3) Configure environment variables
This project reads settings from `.env` (see `app/config.py`).

Minimal `.env` examples:
```bash
# Vector DB
QDRANT_URL=http://localhost:6333

# Embeddings (default: sentence_transformers)
EMBEDDING_PROVIDER=sentence_transformers
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# LLM (default: gemini)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
```

If you switch embeddings to OpenAI:
```bash
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```

## Run the API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Open docs at `http://localhost:8000/docs`.

## API Usage

### Ingest a PDF
Ingests a PDF into a Qdrant collection. Use `subject_id` to route documents into per-subject collections.

```bash
curl -X POST "http://localhost:8000/api/v1/ingest-documents" \
  -F "subject_id=ai-tu-001" \
  -F "document_id=ai-chapter-2" \
  -F "file=@./path/to/document.pdf" \
  -F 'metadata={"title":"Chapter 2 - Intelligent Agents"}'
```

### Generate notes
```bash
curl -X POST "http://localhost:8000/api/v1/generate-notes" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id":"ai-tu-001",
    "document_id":"ai-chapter-2",
    "university":"Tribhuvan University",
    "program":"BSc CSIT",
    "subject":"Artificial Intelligence",
    "learning_outcomes":["Explain intelligent agent types"],
    "chapter":"2. Intelligent Agents",
    "chapter_credit_hours":4,
    "level":"topic",
    "topic_title":"Environment Types",
    "topics":["Deterministic","Stochastic"],
    "subtopics":["Deterministic","Stochastic"]
  }'
```
OR
```bash
curl -X POST "http://localhost:8000/api/v1/generate-notes" \
  -H "Content-Type: application/json" \
  -d '{
  {
  "chapter": "1. Introduction to Neural Network",
  "chapter_credit_hours": 4,
  "document_id": "123",
  "learning_outcomes": [
    "The course objective is to demonstrate the concept of supervised learning, unsupervised learning in conjunction with different architectures of Neural Network."
  ],
  "level": "topic",
  "program": "BSc CSIT",
  "subject": "Neural Network",
  "subject_id": "csc383",
  "subtopics": ["Basics of neural networks and human brain",
    "Models of a neuron",
    "Neural Network viewed as Directed Graphs",
    "Feedback",
    "Network Architectures"],
  "topic_title": "1.1. Neural Network Fundamentals",
  "topics": [
    "Neural Network Fundamentals"
  ],
  "university": "Tribhuvan University"
  }'
```

## Development

### Logs
Application logs are written under `logs/` (see `app/utils/logging_config.py`).

### Unit tests (stdlib)
This repo includes a small regression test for the Qdrant adapter.
```bash
python3 -m unittest discover -s tests -v
```
