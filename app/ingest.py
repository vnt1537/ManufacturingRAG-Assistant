from pathlib import Path
from typing import List

from langchain_core.documents import Document


def load_markdown_documents(data_dir: str = "data/raw_docs") -> List[Document]:
    """
    Load all markdown files from the given directory and return them as LangChain Documents.
    """
    docs_path = Path(data_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    documents: List[Document] = []

    for file_path in docs_path.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        document = Document(
            page_content=text,
            metadata={
                "source": str(file_path),
                "file_name": file_path.name,
            },
        )
        documents.append(document)

    if not documents:
        raise ValueError(f"No markdown files found in: {data_dir}")

    return documents


if __name__ == "__main__":
    docs = load_markdown_documents()
    print(f"Loaded {len(docs)} documents.")
    for doc in docs:
        print(f"- {doc.metadata['file_name']}")