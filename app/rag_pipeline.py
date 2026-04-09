from typing import List, Tuple

from langchain_core.documents import Document
from langchain_ollama import ChatOllama

from app.prompts import RAG_PROMPT
from app.vectorstore import load_vectorstore


DEFAULT_MODEL_NAME = "qwen2.5:3b"


def get_llm(model_name: str = DEFAULT_MODEL_NAME) -> ChatOllama:
    """
    Return the local Ollama chat model.
    """
    return ChatOllama(model=model_name, temperature=0)


def retrieve_documents(question: str, k: int = 4) -> List[Document]:
    """
    Retrieve the top-k most relevant documents/chunks from the FAISS vector store.
    """
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(question)

def get_unique_source_names(documents: list[Document]) -> list[str]:
    seen = set()
    unique_sources = []

    for doc in documents:
        source = doc.metadata.get("file_name", "unknown_source")
        if source not in seen:
            seen.add(source)
            unique_sources.append(source)

    return unique_sources

def format_context(documents: List[Document]) -> str:
    """
    Format retrieved chunks into a readable context block for the prompt.
    """
    context_parts = []

    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get("file_name", "unknown_source")
        chunk_text = doc.page_content.strip()
        context_parts.append(f"[Source {i}: {source}]\n{chunk_text}")

    return "\n\n".join(context_parts)


def generate_rag_answer(
    question: str,
    model_name: str = DEFAULT_MODEL_NAME,
    k: int = 4,
) -> Tuple[str, List[Document]]:
    """
    Retrieve relevant chunks and generate a grounded answer.
    Returns the answer and the retrieved documents.
    """
    retrieved_docs = retrieve_documents(question, k=k)
    context = format_context(retrieved_docs)

    llm = get_llm(model_name=model_name)
    prompt = RAG_PROMPT.invoke(
        {
            "question": question,
            "context": context,
        }
    )
    response = llm.invoke(prompt)
    return response.content, retrieved_docs


if __name__ == "__main__":
    test_question = "How often should torque verification be performed?"
    answer, docs = generate_rag_answer(test_question)

    print("RAG answer:")
    print(answer)
    print("\nRetrieved sources:")
    for source in get_unique_source_names(docs):
        print("-", source)