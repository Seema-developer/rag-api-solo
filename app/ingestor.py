import os
import io
import pdfplumber
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

# extract text from PDF
def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from PDF bytes."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# text into chunks
def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks

def embed_and_store(chunks: list[str], doc_id: str) -> int:
    """Embed chunks and store in Pinecone. Returns number of chunks stored."""
    vectors = []
    
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()

        vector_id = f"{doc_id}_chunk_{i}"

        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": {"text": chunk, "doc_id": doc_id}
        })

    index.upsert(vectors=vectors)

    return len(vectors)


def ingest_pdf(file_bytes: bytes, doc_id: str) -> dict:
    """Full pipeline: extract → chunk → embed → store."""
    text = extract_text_from_pdf(file_bytes)

    if not text:
        raise ValueError("No text could be extracted from this PDF.")

    chunks = chunk_text(text)

    chunks_stored = embed_and_store(chunks, doc_id)

    return {
        "doc_id": doc_id,
        "chunks_stored": chunks_stored,
        "status": "success"
    }