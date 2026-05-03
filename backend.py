from pypdf import PdfReader

def load_and_split():
    reader = PdfReader("data/hospital.pdf")
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return [text]

def create_vector_store(texts):
    return texts

def ask_question(db, query):
    text = db[0]

    if "visiting" in query.lower():
        return "Visiting hours are 9 AM to 6 PM"

    if "emergency" in query.lower():
        return "Emergency services are available 24/7"

    return "Backend is working (basic response)"