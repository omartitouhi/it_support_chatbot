import streamlit as st
import requests
import json
import os

st.title("IT Support Chatbot")
st.subheader("Ask about Windows troubleshooting (e.g., 'How do I fix a Blue Screen of Death?')")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Load history from file if exists
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r", encoding="utf-8") as f:
            st.session_state.messages = json.load(f)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box for user query
if query := st.chat_input("Type your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Call FastAPI endpoint with chat history
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"query": query, "chat_history": st.session_state.messages}
        )
        response.raise_for_status()
        answer = response.json().get("response", "Error: No response from server")
    except requests.RequestException as e:
        answer = f"Error connecting to backend: {str(e)}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Save chat history to file
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)