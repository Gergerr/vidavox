# generate_synthetic_data.py
import pandas as pd
import random
from datetime import datetime, timedelta

modes = ["Pembersihan", "Pendamping", "Motor", "Mobil", "Pod Terbang"]
locations = ["Ruang Tamu", "Dapur", "Kamar Tidur", "Jalan Fiktif A", "Langit Fiktif"]
errors = ["TF-404", "PT-502", "PR-101", "CL-303", "BO-707"]  # 5 error codes
users = ["Budi Santoso", "Ani Wijaya", "Rudi Hartono", "Siti Aminah", "Joko Susilo"]

data = {
    "ID_Log": range(1, 1001),
    "Tanggal": [(datetime(2025, 3, 1) + timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d") for _ in range(1000)],
    "Waktu": [f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00" for _ in range(1000)],
    "Mode": [random.choice(modes) for _ in range(1000)],
    "Durasi_menit": [random.randint(10, 120) for _ in range(1000)],
    "Lokasi": [random.choice(locations) for _ in range(1000)],
    "Status_Baterai": [random.randint(20, 100) for _ in range(1000)],
    "Error_Kode": [random.choice(errors + ["Tidak Ada"] * 5) for _ in range(1000)],  # 5x lebih sering "Tidak Ada"
    "Pengguna": [random.choice(users) for _ in range(1000)],
    "Konsumsi_Daya": [random.randint(50, 400) for _ in range(1000)]
}
df = pd.DataFrame(data)
df.to_csv("synthetic_data.csv", index=False)
print("Synthetic database generated: synthetic_data.csv")