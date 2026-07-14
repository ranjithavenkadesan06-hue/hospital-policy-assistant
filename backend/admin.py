import os

from backend.loader import load_file
from backend.vectorstore import create_vectorstore


def refresh_knowledge_base(upload_dir):

    all_docs = []

    for filename in os.listdir(upload_dir):

        file_path = os.path.join(upload_dir, filename)

        if os.path.isfile(file_path):

            docs = load_file(file_path)
            all_docs.extend(docs)

    return create_vectorstore(all_docs)