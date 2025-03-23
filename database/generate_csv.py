# generate_csv.py
import pandas as pd
import random
from datetime import datetime, timedelta
import os
from faker import Faker

# Inisialisasi Faker dengan locale Indonesia
faker = Faker('id_ID')

# Daftar opsi untuk data sintetik
modes = ["Pembersihan", "Pendamping", "Motor", "Mobil", "Pod Terbang"]
locations = ["Ruang Tamu", "Dapur", "Kamar Tidur", "Kamar Mandi", "Jalan Fiktif A", "Jalan Fiktif B", "Langit Fiktif"]
error_codes = ["Tidak Ada", "TF-404", "PT-502", "PR-101", "CL-303", "BO-707", "NS-201", "AP-301", "CK-401", "NV-501", "LI-601"]

# Fungsi untuk generate tanggal dan waktu acak
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def random_time():
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Generate data
data = []
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 2, 28)

for i in range(1, 1501):  # Generate 1000 baris data
    date = random_date(start_date, end_date).strftime("%Y-%m-%d")
    time = random_time()
    mode = random.choice(modes)
    duration = random.randint(10, 120)  # Durasi 10-120 menit
    location = random.choice(locations)
    battery_status = random.randint(10, 100)  # Persentase baterai 10-100%
    error_code = random.choice(error_codes)
    # Generate nama acak dengan Faker
    user = faker.name()
    power_usage = random.randint(100, 400)  # Konsumsi daya 100-400 Wh

    data.append({
        "ID_Log": i,
        "Tanggal": date,
        "Waktu": time,
        "Mode": mode,
        "Durasi_menit": duration,
        "Lokasi": location,
        "Status_Baterai": battery_status,
        "Error_Kode": error_code,
        "Pengguna": user,
        "Konsumsi_Daya": power_usage
    })

# Buat DataFrame dan simpan ke CSV
df = pd.DataFrame(data)
df.to_csv("synthetic_data.csv", index=False)
print("CSV generation complete: synthetic_data.csv")