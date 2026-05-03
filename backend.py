from pypdf import PdfReader

# words to ignore
STOPWORDS = {"what", "are", "the", "is", "a", "an", "of", "for", "to", "in", "on"}

def load_and_split():
    reader = PdfReader("data/hospital.pdf")
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    # split line by line
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    return lines


def create_vector_store(texts):
    return texts


def ask_question(db, query):
    STOPWORDS = {"what", "are", "the", "is", "a", "an", "of", "for", "to", "in", "on"}

    query_words = [
        word for word in query.lower().split()
        if word not in STOPWORDS
    ]

    best_index = -1
    max_score = 0

    for i, line in enumerate(db):
        score = 0
        line_lower = line.lower()

        for word in query_words:
            if word in line_lower:
                score += 1

        if score > max_score:
            max_score = score
            best_index = i

    if max_score == 0:
        return "No relevant answer found."

    # 🔥 return current line + next line
    answer = db[best_index]

    if best_index + 1 < len(db):
        answer += " " + db[best_index + 1]

    return answer