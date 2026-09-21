# Basic RAG using FastAPI and ChromaDB

A basic Retrieval-Augmented Generation (RAG) application built with FastAPI, ChromaDB, LangChain, and Groq. The application allows users to upload PDF documents, process and store their contents in ChromaDB, and ask questions based on the uploaded documents.

## Features

- Upload PDF documents through a FastAPI endpoint
- Extract text from PDF files
- Split documents into smaller chunks using recursive text splitting
- Store document chunks in a persistent ChromaDB collection
- Retrieve relevant document chunks using similarity search
- Generate answers using the Groq API
- Restrict generated answers to the retrieved document context
- Return a fallback response when the answer is not found in the provided context

## Tech Stack

- Python
- FastAPI
- ChromaDB
- LangChain
- PyPDF
- Groq
- Pydantic

## Project Structure

```text
Basic-RAG-using-FastAPI/
├── chroma_db/
├── uploads/
├── venv/
├── .env
├── main.py
├── models.py
├── requirements.txt
└── README.md
````

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Hassan-908/Basic-RAG-using-FastAPI.git
cd Basic-RAG-using-FastAPI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with a valid Groq API key.

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation can be accessed at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Upload a PDF

**POST** `/upload`

Uploads a PDF and processes it for retrieval.

The document is:

1. Saved locally
2. Loaded using `PyPDFLoader`
3. Split into chunks using `RecursiveCharacterTextSplitter`
4. Stored in ChromaDB

Example response:

```json
{
    "filename": "document.pdf",
    "pages": 10,
    "chunks": 42
}
```

### Ask a Question

**POST** `/ask`

Accepts a question and retrieves the three most relevant chunks from ChromaDB before passing them to the Groq model.

Example request:

```json
{
    "question": "What is OSPF?"
}
```

The model generates an answer using the retrieved document context.

If the answer cannot be found in the retrieved context, the application returns:

```text
I don't know based on the provided context.
```

## RAG Pipeline

```text
PDF Upload
    ↓
PyPDFLoader
    ↓
Text Extraction
    ↓
Recursive Text Splitting
    ↓
Document Chunks
    ↓
ChromaDB
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
Groq LLM
    ↓
Generated Answer
```

## Configuration

Documents are split using:

```python
chunk_size = 1000
chunk_overlap = 200
```

The `/ask` endpoint retrieves the top 3 relevant chunks from ChromaDB for each question.

## Storage

* Uploaded PDF files are stored in the `uploads/` directory.
* ChromaDB data is persisted in the `chroma_db/` directory.
* All uploaded documents are stored in the same ChromaDB collection named `main`.
