IT Support Chatbot
A Retrieval-Augmented Generation (RAG) chatbot for Windows troubleshooting, built with FastAPI, Streamlit, ChromaDB, and Groq API. It provides structured, sourced responses and uses recent chat history for contextual answers.
Features

Processes Windows troubleshooting PDFs (e.g., CH19_PPT_CompTIAATroubleshootingWindows.pdf).
Generates embeddings with BAAI/bge-small-en and stores in ChromaDB.
Retrieves relevant documents and generates responses via Groq API (llama3-8b-8192).
Streamlit UI with persistent chat history (chat_history.json).
Responses consider last 3 interactions for context.

Setup
See docs/user_guide.md for installation and usage instructions.
Documentation

docs/technical_doc.md: System architecture and performance.
docs/user_guide.md: User instructions and troubleshooting.

Demo
Run uvicorn main:app --reload and streamlit run frontend.py to access the chatbot at http://localhost:8501.
Project Status
July 2025, by Omar Titouhi.