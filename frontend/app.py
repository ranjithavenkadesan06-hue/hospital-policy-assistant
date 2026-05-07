import streamlit as st
import requests

st.title("🏥 Hospital Policy Assistant")

UPLOAD_URL = "http://127.0.0.1:8000/upload"
QUERY_URL = "http://127.0.0.1:8000/query"

uploaded_file = st.file_uploader("Upload Document")

if uploaded_file:
    if st.button("Upload"):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        res = requests.post(UPLOAD_URL, files=files)
        st.success(res.text)

question = st.text_input("Ask question")

if st.button("Get Answer"):

    res = requests.get(QUERY_URL, params={"q": question})

    if "<<<>>>" in res.text:
        answer, citations = res.text.split("<<<>>>")

        st.write("### 🤖 Answer")
        st.write(answer)

        st.write("### 📌 Citations")

        if citations.strip():
            for c in citations.split("||"):
                st.info(c)
        else:
            st.write("No citations available")
    else:
        st.write(res.text)