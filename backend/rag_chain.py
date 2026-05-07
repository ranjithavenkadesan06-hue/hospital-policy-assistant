import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

def ask_question(vectorstore, question):

    docs = vectorstore.similarity_search(question, k=3)

    if not docs:
        return "Not found in hospital policy.", ""

    context = "\n\n".join([d.page_content for d in docs])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = f"""
You are a hospital assistant.

Answer using context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    # clean citations
    citations = " || ".join([d.page_content[:120] for d in docs])

    return response.content, citations