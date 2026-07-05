import os

from utils.pdf_reader import read_pdf
from utils.chunking import create_chunks
from utils.embeddings import generate_embeddings
from utils.vector_db import store_in_chromadb
from utils.vector_db import show_database
from utils.retriever import semantic_search
from utils.prompt_builder import build_prompt
from utils.gemini_llm import generate_answer


def main():

    print("=" * 60)
    print("     AI PDF CHATBOT USING MANUAL RAG")
    print("=" * 60)

    pdf_path = "data/sample.pdf"

    if not os.path.exists(pdf_path):

        print("PDF Not Found!")

        return

    # Step 1
    text = read_pdf(pdf_path)

    # Step 2
    chunks = create_chunks(text)

    # Step 3
    embeddings = generate_embeddings(chunks)

    # Step 4
    collection = store_in_chromadb(chunks, embeddings)

    # Step 5
    show_database(collection)

    while True:

        print("\n" + "=" * 60)

        question = input("\nAsk Question (exit to quit): ")

        if question.lower() == "exit":
            break

        # Step 6
        retrieved_chunks = semantic_search(collection, question)

        # Step 7
        prompt = build_prompt(question, retrieved_chunks)

        # Step 8
        generate_answer(prompt)


if __name__ == "__main__":
    main()