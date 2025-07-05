from groq import Groq
import os
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv


def generate_response(query, chat_history=None, model_name="BAAI/bge-small-en", groq_model="llama3-8b-8192"):
    """Retrieve relevant documents and generate a response using Groq API, with optional chat history."""
    try:
        # Load environment variables
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        # Initialize persistent ChromaDB client
        client = chromadb.PersistentClient(path="C:/Users/titou/.chroma")
        collection = client.get_or_create_collection(name="it_support_docs")

        count = collection.count()
        print(f"Collection count: {count}")
        if count == 0:
            return "Error: No documents in ChromaDB. Run retrieve.py first to populate the collection."

        # Initialize embedding model
        embedding_model = SentenceTransformer(model_name)

        # Retrieve relevant documents
        query_embedding = embedding_model.encode([query])[0]
        results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=3)
        context = "\n".join(results["documents"][0])
        sources = [meta["source"] for meta in results["metadatas"][0]]

        # Format chat history for prompt (last 3 interactions)
        history_context = ""
        if chat_history:
            # Take last 3 interactions to avoid token limit
            recent_history = chat_history[-3:]
            history_context = "\nPrevious Interactions:\n"
            for msg in recent_history:
                history_context += f"{msg['role'].capitalize()}: {msg['content']}\n"

        # Generate response with Groq
        groq_client = Groq(api_key=groq_api_key)
        prompt = f"""
        You are an IT Technical Support Assistant specializing in Windows Troubleshooting.
        Using the provided context from technical documents and recent chat history, provide a clear, step-by-step solution to the user's query.
        Ensure the response considers previous interactions for consistency.
        Cite the source if available.
        Query: {query}
        Document Context: {context}
        {history_context}
        Response Format:
        1. Brief explanation.
        2. Step-by-step solution.
        3. Tips or warnings.
        4. Source: {sources[0] if sources else 'Unknown'}
        """
        response = groq_client.chat.completions.create(
            model=groq_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"


if __name__ == "__main__":
    test_query = "How do I fix a Blue Screen of Death?"
    response = generate_response(test_query)
    print(f"Query: {test_query}\nResponse:\n{response}")