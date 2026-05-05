import streamlit as st
import requests

st.set_page_config(page_title="Hospital Policy Assistant", layout="centered")

st.title("🏥 Hospital Policy Assistant (RAG)")
st.write("Upload hospital documents and ask questions")

# Backend URL
UPLOAD_URL = "http://127.0.0.1:8000/upload"
QUERY_URL = "http://127.0.0.1:8000/query"


# -------------------------
# 📂 FILE UPLOAD SECTION
# -------------------------
st.header("📂 Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF / DOCX / TXT",
    type=["pdf", "docx", "txt"]
)

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

    if st.button("Upload to Backend"):
        with st.spinner("Uploading and processing..."):
            response = requests.post(UPLOAD_URL, files=files)

        if response.status_code == 200:
            st.success("File uploaded successfully ✅")
        else:
            st.error(f"Upload failed ❌: {response.text}")


# -------------------------
# ❓ QUESTION SECTION
# -------------------------
st.header("❓ Ask Questions")

question = st.text_input("Enter your question")

if st.button("Get Answer"):
    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Getting answer..."):
            response = requests.get(QUERY_URL, params={"q": question})

        if response.status_code == 200:
            data = response.json()
            st.success("Answer:")
            st.write(data["answer"])
        else:
            st.error("Error getting response from backend")