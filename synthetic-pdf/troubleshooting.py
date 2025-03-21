# generate_troubleshooting.py
from groq import Groq
import os
import config

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Troubleshooting prompt
troubleshooting_prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Pemecahan Masalah' 2500-3500 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Jelaskan lima masalah imajiner berikut: 'Transformasi Gagal' (misalnya modul macet), 'Pod Terbang Tidak Stabil' (misalnya propulsi bermasalah), 'Pendamping Tidak Responsif' (misalnya AI tidak bereaksi), 'Pembersihan Berhenti' (misalnya sensor debu error), dan 'Baterai Overheat' (misalnya panas berlebih saat mode kendaraan). Untuk setiap masalah, sertakan subjudul, deskripsi masalah, penyebab imajiner (misalnya 'Modul Transformasi kelebihan beban'), dan langkah-langkah perbaikan (misalnya 'restart sistem AI melalui aplikasi').
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": troubleshooting_prompt}],
    max_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE
)
with open("troubleshooting.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Troubleshooting text generation complete!")