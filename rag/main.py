# rag/main.py
import os
from data_loader import DataLoader
from indexer import Indexer
from rag_pipeline import RAGPipeline

PDF_FILE = "../synthetic-pdf/Geraldo_synthetic_data.pdf"
CSV_FILE = "../database/synthetic_data.csv"
INDEX_PATH = "faiss_index"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set")

# Langkah 1: Load data
print("Loading data...")
data_loader = DataLoader(pdf_file=PDF_FILE, csv_file=CSV_FILE)
documents = data_loader.load_all_data()

# Langkah 2: Buat indeks FAISS
print("Creating FAISS index...")
indexer = Indexer(chunk_size=500, chunk_overlap=50, embedding_model="sentence-transformers/all-mpnet-base-v2")
vector_store = indexer.create_index(documents, INDEX_PATH)

# Langkah 3: Setup pipeline RAG
print("Setting up RAG pipeline...")
rag_pipeline = RAGPipeline(vector_store, data_loader, GROQ_API_KEY, model_name="llama3-8b-8192")

print("Setup complete! You can now run test_rag.py for evaluation.")