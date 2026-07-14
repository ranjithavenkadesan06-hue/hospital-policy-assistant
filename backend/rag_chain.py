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

    filtered_docs = vectorstore.max_marginal_relevance_search(
    question,
    k=3,
    fetch_k=10
    )
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
You are an AI Hospital Policy Assistant.

Rules:
1. Answer ONLY using the provided context.
2. Never use your own knowledge.
3. If the answer is not clearly present in the context, reply exactly:
   Information not found in hospital policy.
4. Keep the answer concise and professional.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    answer = response.content.strip()
    if "not found" in answer.lower():
     answer = "Information not found in hospital policy."
    print("Answer generated:", answer)
    

    # Better citations
    citations = []

    for d in filtered_docs:

      source = d.metadata.get("source", "Unknown File")
      page = d.metadata.get("page", "-")

      snippet = clean_text(d.page_content)[:150]

      citations.append(
        f"{os.path.basename(source)} | Page {page} | {snippet}..."
      )

    print("Citations:", citations)
    print("Returning from ask_question()")
    return answer, citations