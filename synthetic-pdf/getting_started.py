# generate_getting_started.py
from groq import Groq
import os
import config

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Getting Started prompt
getting_started_prompt = f"""
{config.GLOBAL_PROMPT}
Buat panduan 'Memulai' 5000 hingga 7000 kata dalam Bahasa Indonesia untuk robot fiktif 'GeralBot'. Jelaskan langkah imajiner seperti membuka kotak (unboxing) dengan detail komponen yang disertakan, mengisi daya dengan 'Port Energi Magnetik', dan pengaturan awal seperti menyinkronkan dengan aplikasi 'GeralBot Control'. Sertakan instruksi realistis seperti 'tekan tombol inisiasi selama 5 detik untuk mengaktifkan sistem' dan manfaat setiap langkah. Tambahkan subjudul seperti 'Membuka Kotak', 'Mengisi Daya', dan 'Pengaturan Awal' untuk memandu pengguna.
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": getting_started_prompt}],
    max_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE
)
with open("getting_started.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Getting Started text generation complete!")