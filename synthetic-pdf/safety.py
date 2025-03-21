from groq import Groq
import os

# Safety Instructions prompt
safety_prompt = f"""
{global_prompt}
Buat panduan keselamatan 4000-5000 kata dalam Bahasa Indonesia untuk robot fiktif 'GeralBot'. Sertakan peringatan imajiner seperti 'jangan aktifkan mode terbang di dalam ruangan', 'hindari transformasi motor saat baterai di bawah 20%', 'jaga jarak saat mode pendamping aktif', dan 'matikan daya sebelum membersihkan Modul Memasak'. Tambahkan instruksi penyimpanan (misalnya 'simpan di dok pengisian saat tidak digunakan') dan tips penggunaan aman untuk semua mode (pembersihan, pendamping, kendaraan, memasak).
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": safety_prompt}],
    max_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE
)
with open("safety.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Safety Instructions text generation complete!")