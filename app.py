import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Конфигурация: получаем URL бэкенда из переменной окружения
BACKEND_URL = os.getenv("BACKEND_URL")

def init_session():
    """Инициализирует сессию"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def process_files(pdf_docs):
    """Отправляет PDF на бэкенд для обработки"""
    if not pdf_docs:
        st.error("Please upload at least one PDF file")
        return
    
    files = [("files", (pdf.name, pdf.getvalue(), "application/pdf")) 
             for pdf in pdf_docs]
    
    try:
        with st.spinner("Processing PDFs..."):
            response = requests.post(
                f"{BACKEND_URL}/process",
                files=files,
                timeout=300  # Увеличиваем таймаут для обработки файлов
            )
            
        if response.status_code == 200:
            st.session_state.session_id = response.json()["session_id"]
            st.session_state.chat_history = []  # Сбрасываем историю чата
            st.success("PDFs processed successfully! You can now ask questions.")
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.Timeout:
        st.error("Processing timed out. Please try with smaller files.")
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")

def handle_question(user_question):
    """Отправляет вопрос на бэкенд и обрабатывает ответ"""
    if not st.session_state.session_id:
        st.error("Please upload and process PDFs first")
        return
    
    # Добавляем вопрос пользователя в историю и сразу отображаем его
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_question
    })
    
    # Создаем временный элемент для сообщения бота с индикатором загрузки
    bot_message_placeholder = st.empty()
    bot_message_placeholder.markdown("▌")
    
    try:
        # Отправляем запрос к бэкенду
        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={
                "session_id": st.session_state.session_id,
                "question": user_question
            },
            timeout=30
        )
        
        if response.status_code == 200:
            # Получаем ответ бота
            bot_response = response.json()["chat_history"][-1]["content"]
            
            # Добавляем ответ бота в историю
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": bot_response
            })
            
            # Обновляем элемент с сообщением бота
            bot_message_placeholder.markdown(bot_response)
        else:
            error_msg = f"Error: {response.json().get('detail', 'Unknown error')}"
            bot_message_placeholder.error(error_msg)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_msg
            })
            
    except requests.exceptions.Timeout:
        timeout_msg = "Request timed out. Please try again."
        bot_message_placeholder.error(timeout_msg)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": timeout_msg
        })
    except Exception as e:
        error_msg = f"Connection failed: {str(e)}"
        bot_message_placeholder.error(error_msg)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": error_msg
        })

def display_chat():
    """Отображает историю чата с помощью стандартных элементов Streamlit"""
    for message in st.session_state.chat_history:
        if message["role"] == "user":
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
    
    # Отображаем историю чата
    display_chat()
    
    # Поле ввода вопроса
    if user_question := st.chat_input("Ask a question about your documents..."):
        # Отображаем вопрос пользователя сразу
        with st.chat_message("user"):
            st.write(user_question)
        
        # Обрабатываем вопрос (ответ бота будет добавляться постепенно)
        handle_question(user_question)
    
    # Боковая панель для загрузки документов
    with st.sidebar:
        st.header("Document Management")
        st.subheader("Upload PDFs")
        
        pdf_docs = st.file_uploader(
            "Select PDF documents",
            accept_multiple_files=True,
            type="pdf",
            label_visibility="collapsed"
        )
        
        if st.button("Process Documents", use_container_width=True):
            process_files(pdf_docs)
        
        st.divider()
        
        # Показываем текущий BACKEND_URL для отладки
        st.caption(f"Backend URL: `{BACKEND_URL}`")
        
        if st.session_state.session_id:
            st.success("Documents are processed and ready for questions")
        else:
            st.info("Upload PDFs and click 'Process Documents' to start")
        
        st.divider()
        st.caption("Note: Processing may take several minutes for large files")

if __name__ == "__main__":
    main()