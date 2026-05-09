import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def ask_question(vectorstore, question):

    if vectorstore is None:
        return "Please upload a document first.", []

    # Retrieve docs
    results = vectorstore.similarity_search_with_score(question, k=3)

    filtered_docs = []

    for doc, score in results:

        # Less strict filtering
        if score < 2.0:
            filtered_docs.append(doc)

    # Fallback
    if len(filtered_docs) == 0:
        return "Information not found in hospital policy.", []

    # Context creation
    context = "\n\n".join(
        [d.page_content for d in filtered_docs]
    )

    # Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=API_KEY
    )

    # Prompt
    prompt = f"""
You are a professional Hospital Policy Assistant.

Instructions:
- Answer ONLY from the provided context.
- Keep answers concise and professional.
- If the answer is not available in context,
  say:
  "Information not found in hospital policy."
- Do not hallucinate.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    answer = response.content.strip()

    # Clean citations
    citations = []

    for d in filtered_docs[:1]:

        cleaned = clean_text(d.page_content)

        citations.append(
            cleaned[:150] + "..."
        )

    return answer, citations