import pytest
from unittest.mock import MagicMock
import streamlit as st
from app import main, process_files, handle_question, display_chat, init_session

def test_init_session():
    """Тест инициализации сессии"""
    if "session_id" in st.session_state:
        del st.session_state.session_id
    if "chat_history" in st.session_state:
        del st.session_state.chat_history
    
    init_session()
    assert "session_id" in st.session_state
    assert "chat_history" in st.session_state
    assert st.session_state.session_id is None
    assert st.session_state.chat_history == []

def test_process_files_success(mock_requests, sample_pdf, mock_session_state):
    """Тест успешной обработки файлов"""
    st.session_state.update(mock_session_state)
    
    # Настраиваем мок ответа
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"session_id": "test123"}
    mock_requests.return_value = mock_response
    
    # Вызываем функцию
    process_files([sample_pdf])
    
    # Проверяем результаты
    assert st.session_state.session_id == "test123"
    assert st.session_state.chat_history == []
    mock_requests.assert_called_once()

def test_handle_question_success(mock_requests, mock_session_state):
    """Тест обработки вопроса с успешным ответом"""
    st.session_state.update(mock_session_state)
    st.session_state.session_id = "test123"
    
    # Настраиваем мок ответа
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "chat_history": [{"content": "Test answer", "is_user": False}]
    }
    mock_requests.return_value = mock_response
    
    # Вызываем функцию
    handle_question("Test question")
    
    # Проверяем результаты
    assert len(st.session_state.chat_history) == 2
    assert st.session_state.chat_history[0]["content"] == "Test question"
    assert st.session_state.chat_history[1]["content"] == "Test answer"
    mock_requests.assert_called_once()

def test_display_chat(capsys, mock_session_state):
    """Тест отображения истории чата"""
    st.session_state.update(mock_session_state)
    st.session_state.chat_history = [
        {"role": "user", "content": "Question"},
        {"role": "assistant", "content": "Answer"}
    ]
    
    # Вызываем функцию
    display_chat()
    
    # Проверяем, что функция выполнилась без ошибок
    assert True  # Просто проверяем, что не было исключений