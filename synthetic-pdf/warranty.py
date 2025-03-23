# generate_warranty.py
from groq import Groq
import os
import config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Informasi Garansi' 2000 hingga 3000 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Sertakan:
1. Ketentuan Garansi (500 kata, masa garansi tiap komponen, tambah [IMAGE: warranty_terms.png]),
2. Syarat Klaim (500 kata, 5 syarat detail, tambah [IMAGE: claim_conditions.png]),
3. Prosedur Klaim (500 kata, 7 langkah klaim, tambah [IMAGE: claim_process.png]).
Sertakan kode error (TF-404, BO-707) di konteks relevan sebagai contoh kerusakan yang tercover.
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=config.MAX_TOKENS
)
with open("warranty.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Warranty text generation complete!")