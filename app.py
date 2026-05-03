from backend import load_and_split, create_vector_store, ask_question

print("Hospital Policy Assistant Started")

texts = load_and_split()
db = create_vector_store(texts)

print("Total lines loaded:", len(db))

while True:
    query = input("\nAsk a question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    answer = ask_question(db, query)

    print("\nAnswer:", answer)
    print("-" * 40)