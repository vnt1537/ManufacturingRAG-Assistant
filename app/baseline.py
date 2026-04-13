from langchain_ollama import ChatOllama

from app.prompts import BASELINE_PROMPT


DEFAULT_MODEL_NAME = "qwen2.5:3b"


def get_llm(model_name: str = DEFAULT_MODEL_NAME) -> ChatOllama:
    return ChatOllama(model=model_name, temperature=0)


def generate_baseline_answer(question: str, model_name: str = DEFAULT_MODEL_NAME) -> str:
    llm = get_llm(model_name=model_name)
    prompt = BASELINE_PROMPT.invoke({"question": question})
    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    question = input("Enter your question: ").strip()
    if not question:
        question = "What is the torque range for the housing cover screws?"

    answer = generate_baseline_answer(question)
    print("\nBaseline answer:")
    print(answer)