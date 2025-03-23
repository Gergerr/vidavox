# generate_technical_specs.py
from groq import Groq
import os
import config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Spesifikasi Teknis' 5000 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Sertakan detail imajiner:
1. Dimensi dan Berat (detail tiap mode, perbandingan, tambah [IMAGE: dimensions.png]),
2. Performa (kecepatan, jarak tempuh, efisiensi energi tiap mode, 3 contoh penggunaan, tambah [IMAGE: performance.png]),
3. Baterai (teknologi NexPower, siklus hidup, waktu charging, 5 tips perawatan, tambah [IMAGE: battery.png]),
4. Sensor dan Perangkat (Sensor Debu Kuantum, Pemindai 360, Sensor Emosi, cara kerja, sensitivitas, tambah [IMAGE: sensors.png]),
5. Algoritma (AI Pendamping V3.5, AI Transformasi, Algoritma Pendaratan, pseudocode singkat, tambah [IMAGE: algorithms.png]),
6. Konektivitas (WiFi, Bluetooth, USB, spesifikasi teknis, tambah [IMAGE: connectivity.png]).
Sertakan kode error (TF-404, PT-502, PR-101, CL-303, BO-707, NS-201, AP-301, CK-401, NV-501, LI-601) di konteks relevan dengan analisis teknis mendalam (misalnya, NS-201 terkait motor, CK-401 terkait modul memasak).
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=config.MAX_TOKENS
)
with open("technical_specs.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Technical Specs text generation complete!")