# generate_troubleshooting.py
from groq import Groq
import os
import config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Pemecahan Masalah' 6000 kata dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Jelaskan 10 masalah imajiner berikut dengan kode error spesifik:
1. 'Transformasi Gagal' (TF-404, Modul Transformasi macet),
2. 'Pod Terbang Tidak Stabil' (PT-502, propulsi bermasalah),
3. 'Pendamping Tidak Responsif' (PR-101, AI gagal),
4. 'Pembersihan Berhenti' (CL-303, sensor debu error),
5. 'Baterai Overheat' (BO-707, panas berlebih),
6. 'Suara Berisik' (NS-201, motor bising),
7. 'Koneksi Aplikasi Gagal' (AP-301, Bluetooth/WiFi error),
8. 'Memasak Tidak Merata' (CK-401, modul panas gagal),
9. 'Navigasi Terganggu' (NV-501, sensor 360 error),
10. 'Lampu Indikator Mati' (LI-601, sistem listrik bermasalah).
Untuk setiap masalah, sertakan subjudul, deskripsi 300-400 kata, 3-5 penyebab imajiner (misalnya 'debu menumpuk', 'suhu ekstrem'), 5-7 langkah perbaikan detail (misalnya 'restart via aplikasi', 'cek kabel'), dan 1 studi kasus singkat (~100 kata). Tambah [IMAGE: troubleshoot_TF-404.png], [IMAGE: troubleshoot_PT-502.png], [IMAGE: troubleshoot_PR-101.png], [IMAGE: troubleshoot_CL-303.png], [IMAGE: troubleshoot_BO-707.png], [IMAGE: troubleshoot_NS-201.png], [IMAGE: troubleshoot_AP-301.png], [IMAGE: troubleshoot_CK-401.png], [IMAGE: troubleshoot_NV-501.png], [IMAGE: troubleshoot_LI-601.png] setelah deskripsi tiap masalah sesuai kode error masing-masing.
"""

response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=config.MAX_TOKENS
)
with open("troubleshooting.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Troubleshooting text generation complete!")