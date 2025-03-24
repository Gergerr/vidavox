# vidavox/csv_to_sql.py
import pandas as pd

# Baca file CSV
df = pd.read_csv("synthetic_data.csv")

# Buat file .sql
with open("database/synthetic_data.sql", "w") as f:
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
        # Escape tanda kutip dalam string
        tanggal = str(row['Tanggal']).replace("'", "''")
        waktu = str(row['Waktu']).replace("'", "''")
        mode = str(row['Mode']).replace("'", "''")
        lokasi = str(row['Lokasi']).replace("'", "''")
        error_kode = str(row['Error_Kode']).replace("'", "''")
        pengguna = str(row['Pengguna']).replace("'", "''")

        # Tulis pernyataan INSERT
        f.write(f"INSERT INTO logs (ID_Log, Tanggal, Waktu, Mode, Durasi_menit, Lokasi, Status_Baterai, Error_Kode, Pengguna, Konsumsi_Daya) VALUES (")
        f.write(f"{row['ID_Log']}, ")
        f.write(f"'{tanggal}', ")
        f.write(f"'{waktu}', ")
        f.write(f"'{mode}', ")
        f.write(f"{row['Durasi_menit']}, ")
        f.write(f"'{lokasi}', ")
        f.write(f"{row['Status_Baterai']}, ")
        f.write(f"'{error_kode}', ")
        f.write(f"'{pengguna}', ")
        f.write(f"{row['Konsumsi_Daya']}")
        f.write(");\n")
