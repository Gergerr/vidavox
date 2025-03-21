# generate_appendices.py
from groq import Groq
import os
import config

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Appendices prompt
appendices_prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Apendiks' 1500-2000 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Sertakan informasi imajiner seperti daftar komponen (misalnya 'Sensor Emosi Kuantum', 'Propulsi Anti-Gravitasi V3.0'), penjelasan algoritma (misalnya 'Algoritma Pendaratan Pod V2', 'AI Transformasi V3.5'), dan glosarium istilah teknis fiktif (misalnya 'NexPower', 'Modul Transformasi'). Gunakan subjudul seperti 'Daftar Komponen', 'Penjelasan Algoritma', dan 'Glosarium' untuk mengorganisir informasi, dengan penjelasan singkat dan realistis untuk tiap entri.
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": appendices_prompt}],
    max_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE
)
with open("appendices.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Appendices text generation complete!")