# vidavox/app.py
import streamlit as st
import os
import pandas as pd
import sqlite3
import re
from rag.indexer import Indexer
from rag.rag_pipeline import RAGPipeline
from rag.data_loader import DataLoader
from rag.evaluate import Evaluator

# Streamlit app configuration
st.set_page_config(page_title="GeralBot Chatbot - RAG System", page_icon="🤖", layout="wide")

# Title and description
st.title("GeralBot Chatbot - RAG System")
st.markdown("""
Selamat datang di GeralBot Chatbot! Saya adalah asisten berbasis RAG yang dapat menjawab pertanyaan tentang GeralBot, robot multifungsi dari EnriCorporation.  
Sumber data saya berasal dari panduan pengguna GeralBot (PDF) dan log penggunaan (CSV).  
Masukkan pertanyaan Anda di bawah ini, dan saya akan menjawab dengan RAG dan membandingkannya dengan LLM tanpa RAG!
""")

# Input query and View Data Sample button
col_input, col_sample = st.columns([3, 1])
with col_input:
    query = st.text_input("Masukkan pertanyaan Anda:", placeholder="Contoh: Apa saja langkah untuk mengisi daya GeralBot?")
with col_sample:
    if st.button("View Data Sample (5)"):
        try:
            df = pd.read_csv("database/synthetic_data.csv")
            st.subheader("Sample Data (5 Baris)")
            st.dataframe(df.head(5))
        except Exception as e:
            st.error(f"Could not load data sample: {str(e)}")

# Separator
st.markdown("---")

# Process query and display results
if query:
    with st.spinner("Mencari jawaban..."):
        try:
            # Inisialisasi RAG Pipeline dan Evaluator
            indexer = Indexer(chunk_size=500, chunk_overlap=50, embedding_model="sentence-transformers/all-mpnet-base-v2")
            vector_store = indexer.load_index("rag/faiss_index")
            data_loader = DataLoader(pdf_file="synthetic-pdf/Geraldo_synthetic_data.pdf", csv_file="database/synthetic_data.csv")
            rag_pipeline = RAGPipeline(vector_store, data_loader, os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
            
            documents = data_loader.load_all_data()
            full_context = "\n".join([doc.page_content for doc in documents])
            evaluator = Evaluator(rag_pipeline, full_context, os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")

            # Dapatkan jawaban RAG dan LLM tanpa RAG
            rag_answer, llm_answer = evaluator.evaluate(query)

            # Create two columns for RAG and LLM without RAG results
            col_rag, col_llm = st.columns([1, 1])

            # RAG + LLM Result
            with col_rag:
                st.subheader("Hasil RAG + LLM")
                st.write(rag_answer)

            # LLM without RAG Result
            with col_llm:
                st.subheader("Hasil LLM tanpa RAG")
                st.write(llm_answer)

            # Separator
            st.markdown("---")

            # Check if query is related to CSV and display SQL query and result
            csv_result = data_loader.query_csv(query)
            if csv_result:
                st.subheader("SQL Query")
                # Generate SQL query based on the query type
                query_lower = query.lower()
                conn = sqlite3.connect("rag/geralbot_logs.db")
                cursor = conn.cursor()

                if "pada tanggal" in query_lower:
                    match_date = re.search(r'(?:pada tanggal|tanggal|di tanggal) (\d{4}-\d{2}-\d{2})', query_lower)
                    if match_date:
                        date = match_date.group(1)
                        if "siapa" in query_lower or "pengguna" in query_lower:
                            sql_query = f"SELECT Pengguna FROM logs WHERE Tanggal = '{date}'"
                        elif "mode" in query_lower:
                            sql_query = f"SELECT Mode FROM logs WHERE Tanggal = '{date}'"
                elif "berapa banyak" in query_lower or "jumlah orang" in query_lower or "berapa orang" in query_lower:
                    match_error = re.search(r'error ([\w-]+)', query_lower)
                    if match_error:
                        error_code = match_error.group(1).upper()
                        sql_query = f"SELECT COUNT(DISTINCT Pengguna) FROM logs WHERE Error_Kode = '{error_code}'"
                elif "berapa kali" in query_lower and "digunakan" in query_lower:
                    match_date = re.search(r'(?:pada tanggal|tanggal|di tanggal) (\d{4}-\d{2}-\d{2})', query_lower)
                    if match_date:
                        date = match_date.group(1)
                        sql_query = f"SELECT COUNT(*) FROM logs WHERE Tanggal = '{date}'"

                if sql_query:
                    st.code(sql_query, language="sql")
                    cursor.execute(sql_query)
                    result = cursor.fetchall()
                    st.subheader("Hasil SQL Query")
                    if "COUNT" in sql_query:
                        st.write(f"Jumlah: {result[0][0]}")
                    else:
                        st.write(", ".join([row[0] for row in result]))
                conn.close()