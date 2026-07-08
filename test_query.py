from app.retriever import retrieve_context
from app.llm import generate_answer

question = "What is Seema's CGPA?"

print(f"Question: {question}")
print("Retrieving context...")
chunks = retrieve_context(question)
print(f"Retrieved {len(chunks)} chunks")
print("Generating answer...")
answer = generate_answer(question, chunks)
print(f"\nAnswer: {answer}")