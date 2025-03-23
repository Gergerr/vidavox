# rag/evaluate.py
from langchain_groq import ChatGroq
import time

class Evaluator:
    def __init__(self, rag_pipeline, full_context, groq_api_key, model_name="llama3-8b-8192"):
        self.rag_pipeline = rag_pipeline
        # Batasi full_context jadi maksimal 4000 karakter (~2000 token)
        self.full_context = full_context[:4000]
        self.llm = ChatGroq(
            model_name=model_name,
            api_key=groq_api_key
        )

    def evaluate(self, query):
        # RAG
        print(f"\nQuery: {query}")
        print("=== RAG Answer ===")
        rag_answer, rag_sources = self.rag_pipeline.query(query)
        print(f"Answer: {rag_answer}")
        print("Sources:", rag_sources)

        # LLM tanpa RAG (full context)
        print("\n=== LLM without RAG ===")
        prompt = f"Berikut adalah dokumen lengkap tentang GeralBot:\n\n{self.full_context}\n\nPertanyaan: {query}\nJawab dalam bahasa Indonesia:"
        max_retries = 3
        for attempt in range(max_retries):
            try:
                llm_answer = self.llm.invoke(prompt)
                print(f"Answer: {llm_answer.content}")
                return rag_answer, llm_answer.content
            except Exception as e:
                if "Connection reset by peer" in str(e) or "APIConnectionError" in str(e):
                    print(f"Connection error on attempt {attempt + 1}/{max_retries}, retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    raise e
        raise Exception("Failed to get response from LLM without RAG after maximum retries")