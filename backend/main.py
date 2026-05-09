from fastapi import FastAPI, UploadFile, File
import os

from backend.loader import load_file
from backend.vectorstore import create_vectorstore
from backend.rag_chain import ask_question

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

db = None


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    global db

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    docs = load_file(file_path)
    db = create_vectorstore(docs)

    return "Upload successful"

@app.get("/query")
def query(q: str):

    global db

    answer, citations = ask_question(db, q)

    citation_text = "|||".join(citations)

    return f"{answer}<<<>>>{citation_text}"