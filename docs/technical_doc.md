Technical Documentation: IT Support Chatbot
Overview
The IT Support Chatbot is a Retrieval-Augmented Generation (RAG) system for Windows Troubleshooting, built using modern technologies to provide accurate, sourced responses to user queries, with context from recent chat history.
System Architecture

Data Ingestion (rag/ingest.py):
Extracts text from PDFs (e.g., CH19_PPT_CompTIAATroubleshootingWindows.pdf) using PyPDF2.
Chunks documents into ~1000-character segments with 100-character overlap using LangChain’s RecursiveCharacterTextSplitter.
Saves chunks and metadata (source, topic) to data/processed/chunks.json.


Embedding Generation (rag/retrieve.py):
Generates embeddings for chunks using BAAI/bge-small-en from Sentence Transformers.
Stores embeddings in ChromaDB (C:/Users/titou/.chroma, collection it_support_docs) for semantic search.


Response Generation (rag/generate.py):
Retrieves top 3 relevant documents from ChromaDB using query embeddings.
Incorporates recent chat history (last 3 interactions) into the Groq API prompt for contextual responses.
Uses Groq API (llama3-8b-8192) to generate structured responses with explanation, steps, tips, and source citation.


Backend (main.py):
FastAPI server with /chat endpoint to handle user queries and chat history, returning RAG responses.


Frontend (frontend.py):
Streamlit interface for user interaction, displaying chat history and sending queries/history to the FastAPI backend.
Saves chat history to chat_history.json for persistence across sessions.


Data:
Input: PDFs in data/raw/ (e.g., 56 chunks from one PDF).
Processed: data/processed/chunks.json.
Database: ChromaDB at C:/Users/titou/.chroma.
Chat History: chat_history.json.



Technologies

Python 3.11
FastAPI 0.111.0
Streamlit 1.36.0
ChromaDB 0.5.0
Sentence Transformers 2.7.0
Groq API 0.9.0
PyPDF2 3.0.1
python-dotenv 1.0.1

Setup Instructions

Clone the repository: git clone <repo_url>.
Install dependencies: pip install -r requirements.txt.
Set up .env with GROQ_API_KEY.
Run ingest.py to process PDFs.
Run retrieve.py to generate embeddings.
Start FastAPI: uvicorn main:app --reload.
Launch Streamlit: streamlit run frontend.py.

Performance

Embedding generation: ~5-15 seconds for 56 chunks.
Query response: ~1-2 seconds (retrieval + Groq API).
Chat history integration: Adds negligible overhead (<0.1 seconds) by including last 3 interactions in the prompt.

Fixes

Resolved embedings typo in retrieve.py.
Ensured ChromaDB persistence with C:/Users/titou/.chroma path and collection cleanup.
Fixed Streamlit subtitle to subheader.
Added chat history context to response generation, using last 3 interactions for prompt consistency.

Testing

Tested with 5-10 queries (e.g., BSOD, DNS errors, printer issues).
Verified responses are structured, sourced, and use chat history for context.
Confirmed chat history persists in chat_history.json across sessions.
