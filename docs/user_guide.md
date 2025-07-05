User Guide: IT Support Chatbot
Introduction
The IT Support Chatbot is a Retrieval-Augmented Generation (RAG) system designed to assist users with Windows troubleshooting issues, such as Blue Screen of Death (BSOD), DNS errors, and printer problems. It provides clear, step-by-step solutions sourced from technical documents, with responses enhanced by recent chat history for contextual accuracy. The chatbot features a user-friendly Streamlit interface and persists conversation history across sessions.
Prerequisites

System: Windows 10/11 with Python 3.11 installed.
Dependencies: Install requirements from requirements.txt (pip install -r requirements.txt).
Groq API Key: Obtain from Groq and add to it_support_chatbot/.env.
PDFs: Place Windows troubleshooting PDFs (e.g., CH19_PPT_CompTIAATroubleshootingWindows.pdf) in data/raw/.

Running the Chatbot

Clone the Repository (if applicable): git clone <repo_url>.
Install Dependencies: Run pip install -r requirements.txt in a terminal.
Set Up Environment:
Create it_support_chatbot/.env with:GROQ_API_KEY=your_api_key_here




Process Data:
Run python rag/ingest.py to extract and chunk PDFs into data/processed/chunks.json.
Run python rag/retrieve.py to generate embeddings and store them in C:/Users/titou/.chroma.


Start the Backend:
Run uvicorn main:app --reload to launch the FastAPI server (http://localhost:8000).


Launch the Frontend:
Run streamlit run frontend.py in a new terminal.
Open http://localhost:8501 in a web browser.



Using the Chatbot

Enter Queries: Type a question (e.g., “How do I fix a Blue Screen of Death?”) in the chat input box at http://localhost:8501.
View Responses: Responses are structured as:
Brief explanation.
Step-by-step solution.
Tips or warnings.
Source (e.g., CH19_PPT_CompTIAATroubleshootingWindows.pdf).


Chat History:
Recent interactions (user queries and assistant responses) are displayed above the input box.
Responses consider the last 3 interactions for contextual accuracy (e.g., follow-up questions about BSOD).
History is saved to chat_history.json and persists across sessions.


Example Queries:
“Fix printer not detected”
“Resolve DNS server not responding”
“Application crashes on startup”
Follow-up: “Can you clarify the steps for Safe Mode?”



Troubleshooting

No Response: Ensure the FastAPI backend is running (http://localhost:8000). Check terminal for errors.
Chat History Issues: Verify write permissions for it_support_chatbot/ and check chat_history.json for corruption.
Database Errors: Confirm C:/Users/titou/.chroma exists and contains the it_support_docs collection (run retrieve.py if empty).
Vague Responses: Add more PDFs to data/raw/ and rerun ingest.py, retrieve.py.
Slow Performance: Reduce PDFs in data/raw/ or check system resources (Task Manager).

Support
For issues, consult docs/technical_doc.md or contact the project maintainer.