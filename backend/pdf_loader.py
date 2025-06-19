import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdfs(directory="uploads"):
    docs = []
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(directory, file))
            docs.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)