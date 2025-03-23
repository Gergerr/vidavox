# rag/test_rag.py
import os
from indexer import Indexer
from rag_pipeline import RAGPipeline
from evaluate import Evaluator
from data_loader import DataLoader

# Konfigurasi
INDEX_PATH = "faiss_index"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set")

# Langkah 1: Load indeks FAISS
print("Loading FAISS index...")
indexer = Indexer(chunk_size=500, chunk_overlap=50, embedding_model="sentence-transformers/all-mpnet-base-v2")
vector_store = indexer.load_index(INDEX_PATH)

# Langkah 2: Setup pipeline RAG
print("Setting up RAG pipeline...")
data_loader = DataLoader(pdf_file="../synthetic-pdf/Geraldo_synthetic_data.pdf", csv_file="../database/synthetic_data.csv")
rag_pipeline = RAGPipeline(vector_store, data_loader, GROQ_API_KEY, model_name="llama3-8b-8192")

# Langkah 3: Load full context untuk evaluasi tanpa RAG
documents = data_loader.load_all_data()
full_context = "\n".join([doc.page_content for doc in documents])

# Langkah 4: Evaluasi
print("Starting evaluation...")
evaluator = Evaluator(rag_pipeline, full_context, GROQ_API_KEY, model_name="llama3-8b-8192")

# Sample query untuk tes
query = "Berapa banyak orang yang punya error AP-301?"
rag_answer, llm_answer = evaluator.evaluate(query)
print("-" * 50)