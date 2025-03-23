# generate_getting_started.py
from groq import Groq
import os
import config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Memulai' 5500 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Sertakan:
1. Membuka Kotak (1000 kata, detail isi paket, 5 tips unpacking, tambah [IMAGE: unboxing.png]),
2. Mengisi Daya (1000 kata, langkah detail, 5 masalah umum seperti BO-707, tambah [IMAGE: charging.png]),
3. Pengaturan Awal (1000 kata, 10 langkah setup, 5 tips konfigurasi, tambah [IMAGE: setup.png]).
Sertakan kode error (BO-707, AP-301) di konteks relevan.
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=config.MAX_TOKENS
)
with open("getting_started.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Getting Started text generation complete!")