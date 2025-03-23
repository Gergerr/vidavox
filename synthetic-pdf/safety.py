# generate_safety.py
from groq import Groq
import os
import config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Petunjuk Keselamatan' 4500 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Sertakan:
1. Penggunaan Aman (1000 kata, 10 aturan umum, 5 skenario bahaya, tambah [IMAGE: safety_rules.png]),
2. Pengoperasian (1000 kata, detail langkah aman tiap mode, tambah [IMAGE: safe_operation.png]),
3. Kode Error (1000 kata, jelaskan 10 kode error: TF-404, PT-502, PR-101, CL-303, BO-707, NS-201, AP-301, CK-401, NV-501, LI-601, dengan konteks keselamatan, tambah [IMAGE: error_codes.png]).
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=config.MAX_TOKENS
)
with open("safety.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Safety text generation complete!")