# PDF Question Answering System

Ask questions about your PDF documents using an AI-powered backend (FastAPI) and a Streamlit web UI.

## 1. Prerequisites

- Python 3.10+ installed
- Git installed
- (Optional) A virtual environment tool such as `venv`

## 2. Clone the repository

git clone https://github.com/harsh110306/pdf_qa_gui.git
cd pdf_qa_gui

## 3. Create and activate virtual environment
python -m venv venv
# Windows (PowerShell)
venv\Scripts\Activate
# macOS / Linux
source venv/bin/activate

## 4. Install dependencies
pip install -r requirements.txt

-  Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

## 5. Set environment variables
OPENAI_API_KEY=your_openai_api_key_here
# add any other keys/configs required by the project

## 6. Run the backend (FastAPI)
From the backend folder:
cd backenduvicorn main:app --reload
This will start the API at http://127.0.0.1:8000.

## 7. Run the frontend (Streamlit)
Open a new terminal, activate the same virtualenv, go to the project root, and run:
cd pdf_qa_guistreamlit run app.py
The app will open in your browser (usually at http://localhost:8501).

## 8. Usage
Upload a PDF file in the Streamlit UI.
Click "Process Document" to extract text, chunk it, and create embeddings.
Ask questions in the chat box.
Optionally:
    Get a document summary
    Download the chat history as PDF
