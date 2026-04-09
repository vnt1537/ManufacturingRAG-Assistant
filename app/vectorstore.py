from pathlib import Path
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from app.ingest import load_markdown_documents


EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_DIR = "data/faiss_index"


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Create and return the embedding model.
    """
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def split_documents(
    documents: List[Document],
    chunk_size: int = 700,
    chunk_overlap: int = 120,
) -> List[Document]:
    """
    Split documents into overlapping chunks for better retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


def build_and_save_vectorstore() -> FAISS:
    """
    Load documents, split them into chunks, build a FAISS vectorstore, and save it locally.
    """
    raw_docs = load_markdown_documents()
    split_docs = split_documents(raw_docs)

    embeddings = get_embedding_model()
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    Path(INDEX_DIR).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(INDEX_DIR)

    print(f"Built and saved FAISS index with {len(split_docs)} chunks to '{INDEX_DIR}'.")
    return vectorstore


def load_vectorstore() -> FAISS:
    """
    Load the saved FAISS vectorstore from disk.
    """
    index_path = Path(INDEX_DIR)

    if not index_path.exists():
        raise FileNotFoundError(
            f"FAISS index not found at '{INDEX_DIR}'. Run build_and_save_vectorstore() first."
        )

    embeddings = get_embedding_model()
    return FAISS.load_local(
        INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )


if __name__ == "__main__":
    build_and_save_vectorstore()