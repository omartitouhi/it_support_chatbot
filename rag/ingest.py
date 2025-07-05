import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

path = r"C:\Users\titou\PycharmProjects\it_support_chatbot\data\raw"
pathp = r"C:\Users\titou\PycharmProjects\it_support_chatbot\data\processed"
pathj = r"C:\Users\titou\PycharmProjects\it_support_chatbot\data\processed/chunks.json"
def load_pdf(file_path):
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def chunk_documents(data_dir=path, chunk_size=1000, chunk_overlap=100):
    """Load and chunk documents from the raw data directory."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    documents = []
    metadata = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_dir, filename)
            text = load_pdf(file_path)
            chunks = text_splitter.split_text(text)
            documents.extend(chunks)
            # Add metadata for each chunk
            metadata.extend([{"source": filename, "topic": "Windows Troubleshooting"}] * len(chunks))

    os.makedirs(pathp, exist_ok=True)
    with open(pathj, "w") as f:
        json.dump({"documents": documents, "metadata": metadata}, f)
        print("document saved to data/processed/chunks.json")
    return documents, metadata



if __name__ == "__main__":
    docs, meta = chunk_documents()
    print(f"Extracted {len(docs)} chunks from documents.")
    for i, (doc, m) in enumerate(zip(docs[:2], meta[:2])):
        print(f"Chunk {i + 1}: {doc[:100]}... (Source: {m['source']})")