GLOBAL_PROMPT = """
Buat teks dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot', robot multifungsi dari EnriCorporation. Sertakan detail realistis, teknis, dan contoh penggunaan yang relevan. Jika sesuai dengan konteks, masukkan dan jelaskan kode error berikut: 
- TF-404 (Transformasi Gagal, modul transformasi macet),
- PT-502 (Pod Terbang Tidak Stabil, propulsi bermasalah),
- PR-101 (Pendamping Tidak Responsif, AI gagal),
- CL-303 (Pembersihan Berhenti, sensor debu error),
- BO-707 (Baterai Overheat, panas berlebih),
- NS-201 (Suara Berisik, motor bising),
- AP-301 (Koneksi Aplikasi Gagal, Bluetooth/WiFi error),
- CK-401 (Memasak Tidak Merata, modul panas gagal),
- NV-501 (Navigasi Terganggu, sensor 360 error),
- LI-601 (Lampu Indikator Mati, sistem listrik bermasalah).
Pastikan kode error dimasukkan di bagian yang relevan (misalnya, CL-303 di pembersihan, TF-404 di transformasi) dengan penjelasan singkat tentang penyebab dan solusi potensial.

Kalo misal ada instruksi kayak, [IMAGE: NAMAFILE.png], ITU WAJIB DITAMBAHIN YA! IKUTI INSTRUKSI
"""

MODEL = "gemma2-9b-it"
MAX_TOKENS = 8192
TEMPERATURE = 0.7