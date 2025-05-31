import pytest
from unittest.mock import MagicMock, patch
import streamlit as st
import io

@pytest.fixture
def mock_requests():
    with patch('requests.post') as mock_post:
        yield mock_post

@pytest.fixture
def mock_session_state():
    return {
        "session_id": None,
        "chat_history": []
    }

@pytest.fixture
def sample_pdf():
    pdf = io.BytesIO()
    pdf.name = "test.pdf"
    return pdf