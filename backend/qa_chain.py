# qa_chain.py (Updated with chat memory support)

import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


def get_chain(model_name):
    vectorstore = Chroma(
        persist_directory="vector_store",
        embedding_function=OllamaEmbeddings(model="nomic-embed-text")
    )
    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(
        model_name=model_name,
        temperature=0,
        openai_api_base=os.environ["OPENAI_API_BASE"],
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
        verbose=False
    )

    return qa_chain
