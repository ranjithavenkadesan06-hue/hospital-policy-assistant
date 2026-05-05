import os
from langchain_google_genai import ChatGoogleGenerativeAI

def ask_question(vectorstore, question):

    if vectorstore is None:
        return "Vector database not initialized"

    docs = vectorstore.similarity_search(question, k=3)

    if docs is None or len(docs) == 0:
        return "No relevant information found"

    context = "\n\n".join([d.page_content for d in docs])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = f"""
You are a hospital policy assistant.

Context:
{context}

Question:
{question}

Answer briefly:
"""

    response = llm.invoke(prompt)

    return response.content