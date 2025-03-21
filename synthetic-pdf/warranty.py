# generate_warranty.py
from groq import Groq
import os
import config

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Warranty Information prompt
warranty_prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Informasi Garansi' 500-700 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Sertakan ketentuan imajiner seperti 'garansi 2 tahun untuk Modul Transformasi dan baterai NexPower 8000mAh', syarat klaim (misalnya 'kerusakan bukan akibat penggunaan di luar panduan'), dan prosedur kontak dukungan fiktif (misalnya 'hubungi 0800-GERALBOT atau email ke dukungan@nextech-inovasi.com'). Jelaskan proses klaim garansi secara singkat dan realistis, seperti pada panduan produk asli.
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": warranty_prompt}],
    max_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE
)
with open("warranty.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Warranty Information text generation complete!")