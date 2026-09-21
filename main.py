#Project imports
from fastapi import FastAPI, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import shutil
from models import Questions

#Environment variables imports
import os
from dotenv import load_dotenv

#LLM/API imports
from groq import Groq

#Chroma DB
import chromadb
import uuid

#APP
app = FastAPI()

#CHROMA SETUP
client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection(name="main")



#ENV LOADING
load_dotenv()
api_key = os.getenv("API_KEY")

client = Groq(api_key=api_key)

def send_questions(question, context):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": f"""
                    Answer the question using ONLY the provided context.
                    If the answer cannot be found in the context, say:
                    "I don't know based on the provided context."

                    Context:
                    {context}

                    Question:
                    {question}
                """
            }
        ]
    )
    return response.choices[0].message.content

@app.post("/ask")
def ask(question: Questions):
    ask = question.question
    relevant_texts = collection.query(query_texts=[ask], n_results=3)
    context = relevant_texts["documents"]
    answer = send_questions(ask, context)
    return answer


@app.post("/upload")
def upload_document(file: UploadFile= File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    loader = PyPDFLoader(file_path)
    document = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    chunks = splitter.split_documents(document)

    collection.add(
        documents = [chunk.page_content for chunk in chunks],
        ids = [f"{file.filename}_{uuid.uuid4().hex[:8]}_{i}" for i in range(len(chunks))]
    )

    return {
        "filename": file.filename,
        "pages": len(document),
        "chunks": len(chunks)
    }