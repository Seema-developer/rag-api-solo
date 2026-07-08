from app.ingestor import ingest_pdf

with open(r'C:\Users\Seema\Desktop\Resume.pdf', 'rb') as f:
    file_bytes = f.read()

print("Starting test...")
try:
    result = ingest_pdf(file_bytes, "test_doc_001")
    print("SUCCESS:", result)
except Exception as e:
    import traceback
    traceback.print_exc()