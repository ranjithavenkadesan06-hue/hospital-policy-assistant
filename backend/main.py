from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import os
import traceback

from backend.loader import load_file
from backend.vectorstore import create_vectorstore
from backend.rag_chain import ask_question

load_dotenv()

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

db = None  # global vector DB


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global db

    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        docs = load_file(file_path)

        if not docs:
            return {"error": "No content extracted from file"}

        db = create_vectorstore(docs)

        return {"message": "Upload successful"}

    except Exception as e:
        print(traceback.format_exc())
        return {"error": str(e)}


@app.get("/query")
def query(q: str):
    global db

    try:
        if db is None:
            return {"error": "Please upload a file first"}

        answer = ask_question(db, q)

        return {"answer": answer}

    except Exception as e:
        print(traceback.format_exc())
        return {"error": str(e)}