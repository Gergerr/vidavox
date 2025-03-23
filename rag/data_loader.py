# rag/data_loader.py
import os
import re
import pandas as pd
import pdfplumber
import sqlite3
from langchain.docstore.document import Document

class DataLoader:
    def __init__(self, pdf_file="../synthetic-pdf/Geraldo_synthetic_data.pdf", csv_file="../database/synthetic_data.csv"):
        self.pdf_file = pdf_file
        self.csv_file = csv_file
        self.db_file = "geralbot_logs.db"
        self._setup_db()

    def _setup_db(self):
        # Baca CSV dan simpan ke SQLite
        df = pd.read_csv(self.csv_file)
        conn = sqlite3.connect(self.db_file)
        df.to_sql("logs", conn, if_exists="replace", index=False)
        conn.close()

    def load_pdf(self):
        documents = []
        with pdfplumber.open(self.pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    # Bersihin teks: hapus nomor halaman, header/footer, dan teks dari grafik/tabel
                    text = re.sub(r'Page \d+', '', text)  # Hapus "Page X"
                    text = re.sub(r'Panduan Pengguna GeralBot.*?\n', '', text)  # Hapus header
                    text = re.sub(r'NexTech Inovasi.*?\n', '', text)  # Hapus header
                    text = re.sub(r'Model: GeralBot V3\.5.*?\n', '', text)  # Hapus header
                    text = re.sub(r'Versi Manual: 1\.0, Maret 2025.*?\n', '', text)  # Hapus header
                    text = re.sub(r'Grafik:.*?\n', '', text)  # Hapus teks grafik
                    text = re.sub(r'Log Penggunaan GeralBot.*?\n.*?\n.*?\n', '', text)  # Hapus tabel
                    text = re.sub(r'\(cid:127\)', '', text)  # Hapus karakter aneh
                    text = re.sub(r'\n\s*\n+', '\n', text)  # Hapus baris kosong berlebih

                    # Normalisasi teks (contoh: ubah "pengisian daya" jadi "mengisi daya")
                    text = text.replace("pengisian daya", "mengisi daya")

                    # Pisah berdasarkan heading (nomor section atau teks heading biasa)
                    sections = re.split(
                        r'(\d+\.\s.*?\n|\d+\.\d+\s.*?\n|\d+\.\d+\.\d+\s.*?\n|[A-Z][a-zA-Z\s]+:?\n|[A-Z][a-zA-Z\s]+\n|Mengisi Daya\n|Mode Pembersihan Cerdas\n)',
                        text
                    )
                    for i in range(0, len(sections), 2):
                        if i + 1 < len(sections):
                            heading = sections[i].strip() if sections[i] else "No Heading"
                            section_content = sections[i + 1].strip()
                            if section_content:
                                doc = Document(
                                    page_content=section_content,
                                    metadata={"source": f"PDF Page {page_num + 1}", "heading": heading}
                                )
                                documents.append(doc)
                        else:
                            if sections[i].strip():
                                doc = Document(
                                    page_content=sections[i].strip(),
                                    metadata={"source": f"PDF Page {page_num + 1}", "heading": "No Heading"}
                                )
                                documents.append(doc)
        return documents

    def load_csv_data(self):
        df = pd.read_csv(self.csv_file)
        documents = []
        for _, row in df.iterrows():
            # Format teks CSV supaya lebih mudah ditemukan oleh retrieval
            content = f"Tanggal: {row['Tanggal']}, Log ID: {row['ID_Log']}, Time: {row['Waktu']}, Mode: {row['Mode']}, Duration: {row['Durasi_menit']} minutes, Location: {row['Lokasi']}, Battery: {row['Status_Baterai']}%, Error: {row['Error_Kode']}, User: {row['Pengguna']}, Power Usage: {row['Konsumsi_Daya']} Wh"
            doc = Document(
                page_content=content,
                metadata={"source": "synthetic_data.csv", "log_id": row['ID_Log']}
            )
            documents.append(doc)
        return documents

    def load_all_data(self):
        pdf_docs = self.load_pdf()
        csv_docs = self.load_csv_data()
        return pdf_docs + csv_docs

    def query_csv(self, query):
        query_lower = query.lower()
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Deteksi intent query
        # 1. Agregasi (misalnya, "berapa banyak", "jumlah orang")
        if "berapa banyak" in query_lower or "jumlah orang" in query_lower or "berapa orang" in query_lower:
            # Ekstrak kode error
            match_error = re.search(r'error ([\w-]+)', query_lower)
            if match_error:
                error_code = match_error.group(1).upper()
                cursor.execute("SELECT COUNT(DISTINCT Pengguna) FROM logs WHERE Error_Kode = ?", (error_code,))
                count = cursor.fetchone()[0]
                cursor.execute("SELECT Pengguna FROM logs WHERE Error_Kode = ?", (error_code,))
                result = cursor.fetchall()
                conn.close()
                if result:
                    users = list(set([row[0] for row in result]))  # Distinct users
                    user_list = "\n".join([f"{user} (Log ID: {row[0]})" for user, row in enumerate(result, 1)])
                    return f"Berikut adalah daftar orang yang memiliki error {error_code}:\n{user_list}\nJumlah orang yang memiliki error {error_code} adalah {count} orang."

        # 2. Filter berdasarkan tanggal
        match_date = re.search(r'(?:pada tanggal|tanggal|di tanggal) (\d{4}-\d{2}-\d{2})', query_lower)
        if match_date:
            date = match_date.group(1)
            # Deteksi apakah query meminta pengguna
            if "siapa" in query_lower or "pengguna" in query_lower:
                cursor.execute("SELECT Pengguna FROM logs WHERE Tanggal = ?", (date,))
                result = cursor.fetchall()
                conn.close()
                if result:
                    users = ", ".join([row[0] for row in result])
                    return f"Pengguna: {users}"
            # Deteksi apakah query meminta mode
            elif "mode" in query_lower:
                cursor.execute("SELECT Mode FROM logs WHERE Tanggal = ?", (date,))
                result = cursor.fetchall()
                conn.close()
                if result:
                    modes = ", ".join([row[0] for row in result])
                    return f"Mode: {modes}"

        # 3. Filter berdasarkan error (tanpa agregasi)
        match_error = re.search(r'error ([\w-]+)', query_lower)
        if match_error and ("siapa" in query_lower or "pengguna" in query_lower):
            error_code = match_error.group(1).upper()
            cursor.execute("SELECT Pengguna FROM logs WHERE Error_Kode = ?", (error_code,))
            result = cursor.fetchall()
            conn.close()
            if result:
                users = ", ".join([row[0] for row in result])
                return f"Pengguna: {users}"

        conn.close()
        return None