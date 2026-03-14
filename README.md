# 📄 PDF Question Answering System

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![OpenAI](https://img.shields.io/badge/OpenAI-Embeddings-purple)

An AI-powered PDF Question Answering application that allows users to
upload PDF documents and ask questions about their content using LLMs
and semantic search.

------------------------------------------------------------------------

## 🚀 Features

-   Upload PDF documents
-   Ask questions about document content
-   AI-powered semantic search
-   Document summarization
-   Chat interface
-   Download chat history as PDF

------------------------------------------------------------------------

## 🛠️ Tech Stack

  Component             Technology
  --------------------- ------------
  Frontend              Streamlit
  Backend               FastAPI
  Language              Python
  LLM                   OpenAI
  Vector Store          FAISS
  Document Processing   LangChain

------------------------------------------------------------------------

## 📋 Prerequisites

Before running the project you need:

-   Python 3.10+
-   Git
-   OpenAI API Key

------------------------------------------------------------------------

## 📥 Clone Repository

``` bash
git clone https://github.com/harsh110306/pdf_qa_gui.git
cd pdf_qa_gui
```

------------------------------------------------------------------------

## 🧪 Create Virtual Environment

### Windows

``` bash
python -m venv venv
venv\Scripts\activate
```

### Mac / Linux

``` bash
python3 -m venv venv
source venv/bin/activate
```

------------------------------------------------------------------------

## 📦 Install Dependencies

Install main dependencies:

``` bash
pip install -r requirements.txt
```

Install backend dependencies:

``` bash
cd backend
pip install -r requirements.txt
cd ..
```

------------------------------------------------------------------------

## 🔑 Environment Variables

Create a `.env` file:

    OPENAI_API_KEY=your_openai_api_key_here

------------------------------------------------------------------------

## ▶️ Run Backend

``` bash
cd backend
uvicorn main:app --reload
```

Backend runs at:

    http://127.0.0.1:8000

------------------------------------------------------------------------

## 🖥️ Run Frontend

Open a new terminal:

``` bash
streamlit run app.py
```

App runs at:

    http://localhost:8501

------------------------------------------------------------------------

## 📚 Usage

1.  Upload a PDF
2.  Click **Process Document**
3.  Ask questions about the document

Optional:

-   Get document summary
-   Download chat history as PDF

------------------------------------------------------------------------

## 📂 Project Structure

    pdf_qa_gui
    │
    ├── backend
    │   ├── main.py
    │   └── requirements.txt
    │
    ├── app.py
    ├── requirements.txt
    ├── README.md

------------------------------------------------------------------------

## 👨‍💻 Author

Harsh Shah

GitHub: https://github.com/harsh110306
