# vidavox/csv_to_sql.py
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def csv_to_sql(csv_path="synthetic_data.csv", sql_path="synthetic_data.sql"):
    """
    Convert a CSV file to an SQL file with CREATE TABLE and INSERT statements.
    
    Args:
        csv_path (str): Path to the input CSV file.
        sql_path (str): Path to the output SQL file.
    """
    try:
        # Gunakan path absolut untuk file CSV
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        csv_path = os.path.join(BASE_DIR, csv_path)
        sql_path = os.path.join(BASE_DIR, sql_path)

        # Validasi keberadaan file CSV
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"File CSV tidak ditemukan di: {csv_path}")

        # Baca file CSV
        logger.info(f"Membaca file CSV dari: {csv_path}")
        df = pd.read_csv(csv_path)

        # Validasi bahwa DataFrame tidak kosong
        if df.empty:
            raise ValueError("File CSV kosong atau tidak dapat dibaca")

        logger.info(f"Berhasil membaca {len(df)} baris dari CSV")

        # Buat file .sql
        with open(sql_path, "w") as f:
            # Tulis header dan komentar
            f.write("-- File SQL untuk data log penggunaan GeralBot\n")
            f.write(f"-- Dibuat dari: {csv_path}\n")
            f.write(f"-- Jumlah baris: {len(df)}\n\n")

            # Tulis pernyataan CREATE TABLE
            f.write("CREATE TABLE logs (\n")
            f.write("    ID_Log INTEGER PRIMARY KEY,\n")
            f.write("    Tanggal TEXT,\n")
            f.write("    Waktu TEXT,\n")
            f.write("    Mode TEXT,\n")
            f.write("    Durasi_menit INTEGER,\n")
            f.write("    Lokasi TEXT,\n")
            f.write("    Status_Baterai INTEGER,\n")
            f.write("    Error_Kode TEXT,\n")
            f.write("    Pengguna TEXT,\n")
            f.write("    Konsumsi_Daya INTEGER\n")
            f.write(");\n\n")

            # Tulis pernyataan INSERT INTO
            for index, row in df.iterrows():
                # Tangani nilai NaN dan escape tanda kutip dalam string
                tanggal = str(row['Tanggal']).replace("'", "''") if pd.notna(row['Tanggal']) else ""
                waktu = str(row['Waktu']).replace("'", "''") if pd.notna(row['Waktu']) else ""
                mode = str(row['Mode']).replace("'", "''") if pd.notna(row['Mode']) else ""
                lokasi = str(row['Lokasi']).replace("'", "''") if pd.notna(row['Lokasi']) else ""
                error_kode = str(row['Error_Kode']).replace("'", "''") if pd.notna(row['Error_Kode']) else ""
                pengguna = str(row['Pengguna']).replace("'", "''") if pd.notna(row['Pengguna']) else ""

                # Tangani nilai numerik (ganti NaN dengan 0)
                id_log = int(row['ID_Log']) if pd.notna(row['ID_Log']) else 0
                durasi_menit = int(row['Durasi_menit']) if pd.notna(row['Durasi_menit']) else 0
                status_baterai = int(row['Status_Baterai']) if pd.notna(row['Status_Baterai']) else 0
                konsumsi_daya = int(row['Konsumsi_Daya']) if pd.notna(row['Konsumsi_Daya']) else 0

                # Tulis pernyataan INSERT
                f.write(f"INSERT INTO logs (ID_Log, Tanggal, Waktu, Mode, Durasi_menit, Lokasi, Status_Baterai, Error_Kode, Pengguna, Konsumsi_Daya) VALUES (")
                f.write(f"{id_log}, ")
                f.write(f"'{tanggal}', ")
                f.write(f"'{waktu}', ")
                f.write(f"'{mode}', ")
                f.write(f"{durasi_menit}, ")
                f.write(f"'{lokasi}', ")
                f.write(f"{status_baterai}, ")
                f.write(f"'{error_kode}', ")
                f.write(f"'{pengguna}', ")
                f.write(f"{konsumsi_daya}")
                f.write(");\n")

        logger.info(f"File SQL berhasil dibuat di: {sql_path}")

    except FileNotFoundError as e:
        logger.error(f"Error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Terjadi kesalahan saat mengonversi CSV ke SQL: {str(e)}")
        raise

if __name__ == "__main__":
    # Jalankan konversi
    csv_to_sql()