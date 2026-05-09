import streamlit as st
import requests

st.set_page_config(
    page_title="Hospital Policy Assistant",
    layout="centered"
)

st.title("🏥 Hospital Policy Assistant")

UPLOAD_URL = "http://127.0.0.1:8000/upload"
QUERY_URL = "http://127.0.0.1:8000/query"

# ====================================
# Upload Section
# ====================================

uploaded_file = st.file_uploader(
    "Upload PDF / DOCX / TXT"
)

if uploaded_file is not None:

    if st.button("Upload"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type
            )
        }

        try:

            response = requests.post(
                UPLOAD_URL,
                files=files
            )

            st.success("File uploaded successfully ✅")

        except Exception as e:

            st.error(f"Upload failed: {e}")

# ====================================
# Question Section
# ====================================

st.subheader("Ask Question")

question = st.text_input(
    "Enter your question"
)

if st.button("Get Answer"):

    if question.strip() == "":

        st.warning("Please enter a question")

    else:

        try:

            with st.spinner("Generating answer..."):

                response = requests.get(
                    QUERY_URL,
                    params={"q": question}
                )

            result = response.text

            # ====================================
            # Split answer and citations
            # ====================================

            if "<<<>>>" in result:

                answer, citations = result.split("<<<>>>")

                if citations.strip() == "":
                    citations = []

                else:
                    citations = citations.split("|||")

            else:

                answer = result
                citations = []

            # ====================================
            # Display Answer
            # ====================================

            st.write("## 🤖 Answer")
            st.write(answer)

            # ====================================
            # Display Citations
            # ====================================

            if citations and "not found" not in answer.lower():

                st.write("## 📌 Source")

                for c in citations:

                    cleaned = c.replace("\\n", " ")

                    st.info(cleaned)

        except Exception as e:

            st.error(f"Error: {e}")