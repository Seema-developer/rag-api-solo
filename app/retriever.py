import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def retrieve_context(query: str, top_k: int = 4) -> list[str]:
    """Embed query and find top_k most similar chunks from Pinecone."""
    query_embedding = model.encode(query).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    chunks = [match["metadata"]["text"] for match in results["matches"]]
    return chunks