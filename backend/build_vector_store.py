from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from pdf_loader import load_pdfs

import os

def build_vector_store():
    # Load Dharashiv website text
    with open("docs/dharashiv_all.txt", "r", encoding="utf-8") as f:
        website_text = f.read()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    website_chunks = splitter.create_documents([website_text])

    # Load any PDFs in the uploads/ folder
    pdf_chunks = load_pdfs()
    all_docs = website_chunks + pdf_chunks

    print(f"📄 Total chunks before embedding: {len(all_docs)}")

    # TEMP: Use only 10 chunks for quick testing
    all_docs = all_docs[:10]
    print(f"⚡ Using {len(all_docs)} chunks for fast embedding...")

    # Create embeddings and vector store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(documents=all_docs, embedding=embeddings, persist_directory="vector_store")

    # Save to disk
    vectorstore.persist()
    print("✅ Vector store built and saved to vector_store/")

if __name__ == "__main__":
    build_vector_store()
