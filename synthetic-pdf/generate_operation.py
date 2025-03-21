# generate_operation.py
from groq import Groq
import os
import config

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Operation prompt
operation_prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Pengoperasian' 5000-6000 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Jelaskan mode operasi berikut: 'Mode Pembersihan Cerdas' (pembersihan rumah dengan sensor debu dan vakum adaptif), 'Mode Pendamping' (interaksi emosional, percakapan, dan permainan), 'Mode Motor' (transformasi menjadi sepeda motor untuk perjalanan cepat), 'Mode Mobil' (transformasi menjadi mobil keluarga dengan kursi otomatis), dan 'Mode Pod Terbang' (terbang seperti drop pod Fortnite untuk transportasi udara). Untuk setiap mode, sertakan subjudul, tujuan, manfaat, dan langkah penggunaan (misalnya 'aktifkan melalui aplikasi', 'atur ketinggian penerbangan'). Tambahkan detail teknis imajiner seperti 'Modul Transformasi Adaptif V4.0' atau 'AI Pendamping Emosional V3.5'.
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": operation_prompt}],
    max_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE
)
with open("operation.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Operation text generation complete!")