import streamlit as st
import requests

st.title("🏥 Hospital Policy Assistant")

# Upload file
uploaded_file = st.file_uploader("Upload Hospital Document", type=["pdf", "docx", "txt"])

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://127.0.0.1:8000/upload", files={"file": uploaded_file})
    st.success("File uploaded!")

# Ask question
query = st.text_input("Ask a question")

if st.button("Ask"):
    res = requests.get("http://127.0.0.1:8000/query", params={"q": query})
    st.write(res.json()["answer"])