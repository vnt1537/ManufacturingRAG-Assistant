import json
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.baseline import generate_baseline_answer
from app.rag_pipeline import generate_rag_answer, get_unique_source_names


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
QUESTIONS_FILE = Path("eval/questions.json")

app = FastAPI(title="Manufacturing RAG Assistant")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def load_sample_questions() -> List[str]:
    if not QUESTIONS_FILE.exists():
        return []

    with QUESTIONS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    questions = []
    for item in data:
        question = item.get("question")
        if question:
            questions.append(question)

    return questions


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "sample_questions": load_sample_questions(),
            "selected_question": "",
            "custom_question": "",
            "model_name": "qwen2.5:3b",
            "rag_mode": "strict",
            "baseline_answer": None,
            "rag_answer": None,
            "retrieved_sources": [],
            "retrieved_docs": [],
            "final_question": "",
            "error_message": None,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def compare_answers(
    request: Request,
    sample_question: Optional[str] = Form(default=""),
    custom_question: Optional[str] = Form(default=""),
    model_name: str = Form(default="qwen2.5:3b"),
    rag_mode: str = Form(default="strict"),
):
    sample_question = (sample_question or "").strip()
    custom_question = (custom_question or "").strip()
    model_name = (model_name or "").strip() or "qwen2.5:3b"
    rag_mode = (rag_mode or "strict").strip().lower()

    if rag_mode not in {"strict", "hybrid"}:
        rag_mode = "strict"

    final_question = custom_question if custom_question else sample_question

    if not final_question:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "sample_questions": load_sample_questions(),
                "selected_question": sample_question,
                "custom_question": custom_question,
                "model_name": model_name,
                "rag_mode": rag_mode,
                "baseline_answer": None,
                "rag_answer": None,
                "retrieved_sources": [],
                "retrieved_docs": [],
                "final_question": "",
                "error_message": "Please enter a custom question or select a sample question.",
            },
        )

    try:
        baseline_answer = generate_baseline_answer(final_question, model_name=model_name)
        rag_answer, retrieved_docs = generate_rag_answer(
            final_question,
            model_name=model_name,
            mode=rag_mode,
        )
        retrieved_sources = get_unique_source_names(retrieved_docs)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "sample_questions": load_sample_questions(),
                "selected_question": sample_question,
                "custom_question": custom_question,
                "model_name": model_name,
                "rag_mode": rag_mode,
                "baseline_answer": baseline_answer,
                "rag_answer": rag_answer,
                "retrieved_sources": retrieved_sources,
                "retrieved_docs": retrieved_docs,
                "final_question": final_question,
                "error_message": None,
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "sample_questions": load_sample_questions(),
                "selected_question": sample_question,
                "custom_question": custom_question,
                "model_name": model_name,
                "rag_mode": rag_mode,
                "baseline_answer": None,
                "rag_answer": None,
                "retrieved_sources": [],
                "retrieved_docs": [],
                "final_question": final_question,
                "error_message": f"An error occurred: {str(exc)}",
            },
        )