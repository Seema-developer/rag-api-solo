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

## Features
- Upload PDF documents
- Semantic search using vector embeddings
- Context-based question answering
- REST API endpoints
  
## Architecture
PDF → extract text → chunk (400 words, 50 overlap) → embed (384-dim) 
→ Pinecone upsert → query embedding → cosine similarity search 
→ top 4 chunks → Groq LLM → grounded answer

