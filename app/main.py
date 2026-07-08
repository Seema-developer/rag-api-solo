import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.ingestor import ingest_pdf
from app.retriever import retrieve_context
from app.llm import generate_answer

app = FastAPI(title="RAG API Solo")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted.")

    file_bytes = await file.read()
    doc_id = str(uuid.uuid4())

    try:
        result = ingest_pdf(file_bytes, doc_id)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query_document(payload: dict):
    question = payload.get("question", "").strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        chunks = retrieve_context(question)
        answer = generate_answer(question, chunks)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))