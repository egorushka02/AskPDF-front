# AskPDF - Chat with Your PDF Documents

AskPDF is a web application that allows users to upload PDF documents and interact with them through a chat interface. The application uses natural language processing to understand and answer questions about the content of your PDF documents.

## Features

- 📄 Upload multiple PDF documents
- 💬 Interactive chat interface
- 🤖 AI-powered question answering
- 📱 Responsive and user-friendly design
- 🔄 Real-time processing and response

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A running backend service (URL configured in environment variables)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd AskPDF-front
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your backend URL:
```
BACKEND_URL=http://your-backend-url
```
