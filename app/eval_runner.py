import json
from pathlib import Path
from typing import Any, Dict, List

from app.baseline import generate_baseline_answer
from app.rag_pipeline import generate_rag_answer, get_unique_source_names


QUESTIONS_FILE = Path("eval/questions.json")
RESULTS_FILE = Path("eval/results.json")
DEFAULT_MODEL_NAME = "qwen2.5:3b"
DEFAULT_RAG_MODE = "strict"


def load_questions() -> List[str]:
    if not QUESTIONS_FILE.exists():
        raise FileNotFoundError(f"Questions file not found: {QUESTIONS_FILE}")

    with QUESTIONS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    questions = []
    for item in data:
        question = item.get("question", "").strip()
        if question:
            questions.append(question)

    if not questions:
        raise ValueError("No valid questions found in eval/questions.json")

    return questions


def run_evaluation(
    model_name: str = DEFAULT_MODEL_NAME,
    rag_mode: str = DEFAULT_RAG_MODE,
) -> List[Dict[str, Any]]:
    questions = load_questions()
    results: List[Dict[str, Any]] = []

    for idx, question in enumerate(questions, start=1):
        print(f"\n[{idx}/{len(questions)}] Evaluating question:")
        print(question)

        baseline_answer = generate_baseline_answer(question, model_name=model_name)
        rag_answer, retrieved_docs = generate_rag_answer(
            question,
            model_name=model_name,
            mode=rag_mode,
        )
        retrieved_sources = get_unique_source_names(retrieved_docs)

        result = {
            "question": question,
            "model_name": model_name,
            "rag_mode": rag_mode,
            "baseline_answer": baseline_answer,
            "rag_answer": rag_answer,
            "retrieved_sources": retrieved_sources,
            "retrieved_chunks": [
                {
                    "file_name": doc.metadata.get("file_name", "unknown_source"),
                    "source": doc.metadata.get("source", ""),
                    "content": doc.page_content,
                }
                for doc in retrieved_docs
            ],
        }
        results.append(result)

    return results


def save_results(results: List[Dict[str, Any]], rag_mode: str) -> None:
    output_file = RESULTS_FILE.with_name(f"results_{rag_mode}.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nSaved evaluation results to: {output_file}")


if __name__ == "__main__":
    model_name = input(f"Enter model name [{DEFAULT_MODEL_NAME}]: ").strip()
    if not model_name:
        model_name = DEFAULT_MODEL_NAME

    rag_mode = input(f"Enter RAG mode [strict/hybrid] [{DEFAULT_RAG_MODE}]: ").strip().lower()
    if not rag_mode:
        rag_mode = DEFAULT_RAG_MODE
    if rag_mode not in {"strict", "hybrid"}:
        rag_mode = DEFAULT_RAG_MODE

    results = run_evaluation(model_name=model_name, rag_mode=rag_mode)
    save_results(results, rag_mode=rag_mode)

    print("\nEvaluation complete.")