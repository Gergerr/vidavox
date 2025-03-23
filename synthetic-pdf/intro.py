# generate_intro.py
from groq import Groq
import os
import config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Pengenalan' 3500 hingga 5000 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Sertakan:
1. Deskripsi GeralBot (500 kata, sejarah imajiner, visi NexTech, tambah [IMAGE: geralbot_vision.png]),
2. Tujuan (500 kata, 5 peran utama, contoh penggunaan, tambah [IMAGE: goals.png]),
3. Fitur Utama (1000 kata, detail Pembersihan, Pendamping, Kendaraan, Memasak, 5 contoh fitur kecil, tambah [IMAGE: features.png] setelah Kendaraan).
Sertakan kode error (CL-303, PR-101, TF-404, PT-502, BO-707, NS-201, AP-301, CK-401, NV-501, LI-601) di konteks relevan.
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=config.MAX_TOKENS
)
with open("intro.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Intro text generation complete!")