# rag/indexer.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class Indexer:
    def __init__(self, chunk_size=500, chunk_overlap=50, embedding_model="all-MiniLM-L6-v2"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)

    def create_index(self, documents, index_path):
        # Split dokumen jadi chunk
        docs = self.text_splitter.split_documents(documents)
        print(f"Total chunks: {len(docs)}")

        # Buat indeks FAISS
        vector_store = FAISS.from_documents(docs, self.embeddings)
        vector_store.save_local(index_path)
        print(f"FAISS index saved to {index_path}")
        return vector_store

    def load_index(self, index_path):
        return FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)