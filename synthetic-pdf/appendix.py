# generate_appendices.py
from groq import Groq
import os
import config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Apendiks' 5000 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Sertakan:
1. Daftar Komponen (10 komponen seperti Sensor Emosi, Modul Transformasi, Propulsi V3.0, Sistem Navigasi, Kamera 360, deskripsi 100-150 kata per komponen, tambah [IMAGE: component_1.png], [IMAGE: component_2.png], [IMAGE: component_3.png], [IMAGE: component_4.png], [IMAGE: component_5.png], [IMAGE: component_6.png], [IMAGE: component_7.png], [IMAGE: component_8.png], [IMAGE: component_9.png], [IMAGE: component_10.png] setelah deskripsi masing-masing komponen),
2. Penjelasan Algoritma (AI Pendamping V3.5, AI Transformasi, Algoritma Pendaratan, pseudocode 50-70 baris per algoritma, tambah [IMAGE: algo_ai_pendamping.png], [IMAGE: algo_ai_transformasi.png], [IMAGE: algo_pendaratan.png] per algoritma),
3. Glosarium (30 istilah teknis fiktif, definisi 50-70 kata per istilah, tambah [IMAGE: glossary.png] setelah 15 istilah pertama).
Sertakan kode error (TF-404, PT-502, PR-101, CL-303, BO-707, NS-201, AP-301, CK-401, NV-501, LI-601) di konteks relevan dengan detail teknis (misalnya, NV-501 di Sistem Navigasi, LI-601 di komponen listrik).
"""

response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=config.MAX_TOKENS
)
with open("appendices.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Appendices text generation complete!")