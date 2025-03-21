# generate_technical_specs.py
from groq import Groq
import os
import config

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Technical Specifications prompt
technical_specs_prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Spesifikasi Teknis' 1000-1500 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Sertakan detail imajiner seperti dimensi (misalnya '50cm x 30cm x 20cm di mode robot'), berat (misalnya '5 kg di mode robot, 15 kg di mode mobil'), kapasitas baterai (misalnya 'NexPower 8000mAh'), sensor (misalnya 'Sensor Debu Kuantum', 'Pemindai 360 Derajat'), dan algoritma (misalnya 'AI Transformasi V3.5', 'Algoritma Pendaratan Pod V2'). Jelaskan fungsi tiap komponen secara singkat dan realistis, seperti spesifikasi produk asli.
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": technical_specs_prompt}],
    max_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE
)
with open("technical_specs.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Technical Specifications text generation complete!")