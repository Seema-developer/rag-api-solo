# RAG API Solo

A production-structured REST API for PDF question-answering using RAG 
(Retrieval-Augmented Generation). Upload a PDF, ask questions, get 
answers grounded in your document.

Built without LangChain — every pipeline component written from scratch.

## Stack
- **FastAPI** — REST API layer
- **pdfplumber** — PDF text extraction
- **SentenceTransformers** — local text embeddings (all-MiniLM-L6-v2)
- **Pinecone** — cloud vector database
- **Groq** — LLM inference

## Endpoints
- `GET /health` — health check
- `POST /upload` — upload a PDF for indexing
- `POST /query` — ask a question about uploaded content

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows)
4. Install: `pip install -r requirements.txt`
5. Create `.env` with your keys:

GROQ_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_INDEX_NAME=rag-api-solo

6. Run: `uvicorn app.main:app --reload`
7. Visit: `http://127.0.0.1:8000/docs`

## Architecture

PDF → extract text → chunk (400 words, 50 overlap) → embed (384-dim) 
→ Pinecone upsert → query embedding → cosine similarity search 
→ top 4 chunks → Groq LLM → grounded answer

