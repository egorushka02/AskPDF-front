import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv


load_dotenv()
# configuration
BACKEND_URL = os.getenv("BACKEND_URL")

def init_session():
    """Initialize session"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def process_files(pdf_docs):
    """Send PDF to backend for processing"""
    if not pdf_docs:
        st.error("Please upload at least one pdf file")
        return
    
    files = [("files", (pdf.name, pdf.getvalue(), "application/pdf")) 
             for pdf in pdf_docs]
    
    try:
        with st.spinner("Processing PDFs ..."):
            response = requests.post(
                f"{BACKEND_URL}/process",
                files=files,
                timeout=300
            )

        if response.status_code == 200:
            st.session_state.session_id = response.json()["session_id"]
            st.session_state.chat_history = []
            st.success("PDFs processed succesfully! You can now ask questions.")
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.Timeout:
        st.error("Processing timed out. Please try with smaller files.")
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")


def handle_question(user_question):
    """Send question to the backend and process answer"""
    if not st.session_state.session_id:
        st.error("Please upload and process PDFs first.")
        return
    
    try:
        # show upload indicator
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={
                    "session_id": st.session_state.session_id,
                    "question": user_question
                },
                timeout=60
            )
        
        if response.status_code == 200:
            # add new question and answer in history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            # get last bot answer (last message in history)
            bot_response = response.json()["chat_history"][-1]["content"]

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": bot_response
            })

        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")

def display_chat():
    """Show chat history"""
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])


def main():
    st.set_page_config(
        page_title="Chat with your PDF",
        page_icon=":books:",
        layout="centered"
    )

    init_session()

    st.title("📚 Chat with your PDF")
    st.caption("Upload PDF documents and ask questions about their content")

    # show chat history
    display_chat()

    # Field for question input
    if user_question := st.chat_input("Ask a question about your documents..."):
        handle_question(user_question)

    
    # side panel for document uploading
    with st.sidebar:
        st.header("Document Management")
        st.subheader("Upload PDFs")

        pdf_docs = st.file_uploader(
            "Seelct PDF documents",
            accept_multiple_files=True,
            type="pdf",
            label_visibility="collapsed"
        )

        if st.button("Process Documents", use_container_width=True):
            process_files(pdf_docs)

        st.divider()

        # show URL for debugging
        st.caption(f"Backend URL: `{BACKEND_URL}`")

        if st.session_state.session_id:
            st.success("Documents are processed and ready for questions")
        else:
            st.info("Upload PDFs and click 'Process Documents' to start")

        st.divider()
        st.caption("Note: Processing may take several minutes for large files")

if __name__ == "__main__":
    main()