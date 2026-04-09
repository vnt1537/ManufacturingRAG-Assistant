import streamlit as st

from app.baseline import generate_baseline_answer
from app.rag_pipeline import generate_rag_answer


st.set_page_config(page_title="Manufacturing RAG Assistant", layout="wide")

st.title("Manufacturing RAG Assistant")
st.write("Compare a plain local LLM against the same model with RAG on manufacturing documents.")

question = st.text_area(
    "Enter your manufacturing question:",
    placeholder="Example: How often should torque verification be performed?",
    height=100,
)

model_name = st.text_input("Ollama model name:", value="qwen2.5:3b")

if st.button("Run comparison"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answers..."):
            baseline_answer = generate_baseline_answer(question, model_name=model_name)
            rag_answer, retrieved_docs = generate_rag_answer(question, model_name=model_name)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Baseline LLM Answer")
            st.write(baseline_answer)

        with col2:
            st.subheader("RAG Answer")
            st.write(rag_answer)

        st.subheader("Retrieved Source Chunks")
        for i, doc in enumerate(retrieved_docs, start=1):
            source_name = doc.metadata.get("file_name", "unknown_source")
            with st.expander(f"Source {i}: {source_name}"):
                st.write(doc.page_content)