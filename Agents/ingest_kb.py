import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

KB_PATH = "../kb/raw"
DB_PATH = "../chroma_db"

def ingest_kb():
    print("Starting KB ingestion...")

    documents = []

    for filename in os.listdir(KB_PATH):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(KB_PATH, filename))
            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    db.persist()
    print("KB ingestion completed successfully!")

if __name__ == "__main__":
    ingest_kb()