import json
import os
from sentence_transformers import SentenceTransformer
import chromadb

pathp = r"C:\Users\titou\PycharmProjects\it_support_chatbot\data\processed"
def generate_and_store_embeddings(data_dir=pathp, model_name="BAAI/bge-small-en"):
    """Generate embeddings for document chunks and store in ChromaDB."""
    # Check if chunks.json exists
    chunks_file = os.path.join(data_dir, "chunks.json")
    if not os.path.exists(chunks_file):
        print(f"Error: {chunks_file} not found. Run ingest.py first.")
        return

    # Initialize persistent ChromaDB client
    try:
        client = chromadb.PersistentClient(path="C:/Users/titou/.chroma")
        collection_name = "it_support_docs"
        client.delete_collection(name=collection_name)  # Clear existing collection
        collection = client.get_or_create_collection(name=collection_name)
    except Exception as e:
        print(f"Error initializing ChromaDB client: {e}")
        return

    # Load chunks
    try:
        with open(chunks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        documents = data["documents"]
        metadata = data["metadata"]
    except Exception as e:
        print(f"Error loading {chunks_file}: {e}")
        return

    if not documents:
        print("No documents to process. Check data/processed/chunks.json.")
        return

    # Initialize embedding model
    try:
        model = SentenceTransformer(model_name)
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        return

    # Generate embeddings
    print(f"Generating embeddings for {len(documents)} chunks...")
    try:
        embeddings = model.encode(documents, batch_size=8, show_progress_bar=True)
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return

    # Store in ChromaDB
    try:
        collection.add(
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadata,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
        print(f"Stored {len(documents)} embeddings in ChromaDB.")
        print(f"Collection count after storage: {collection.count()}")
    except Exception as e:
        print(f"Error storing embeddings in ChromaDB: {e}")


def test_retrieval(query="How do I fix a DNS error?", model_name="BAAI/bge-small-en"):
    """Test retrieving relevant documents from ChromaDB."""
    try:
        model = SentenceTransformer(model_name)
        client = chromadb.PersistentClient(path="C:/Users/titou/.chroma")
        collection = client.get_or_create_collection(name="it_support_docs")

        count = collection.count()
        print(f"Collection count before retrieval: {count}")
        if count == 0:
            print("No documents in collection. Run generate_and_store_embeddings first.")
            return

        query_embedding = model.encode([query])[0]
        results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=3)

        print("Top 3 relevant documents:")
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            print(f"Result {i + 1}: {doc[:100]}... (Source: {meta['source']})")
    except Exception as e:
        print(f"Error during retrieval: {e}")


if __name__ == "__main__":
    generate_and_store_embeddings()
    test_retrieval()