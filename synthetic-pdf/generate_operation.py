# generate_operation.py
from groq import Groq
import os
import config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Run 1: Mode Pembersihan + Pendamping (~4000-5000 kata)
prompt_part1 = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Pengoperasian' bagian 1 (4500 kata) dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Fokus pada:
1. 'Mode Pembersihan Cerdas' (detailkan proses langkah demi langkah, 5 contoh kasus penggunaan seperti rumah berdebu atau apartemen kecil, 10 tips lanjutan seperti pembersihan malam atau karpet, variasi mode seperti Deep Clean, Quick Clean, Eco Mode, tambah [IMAGE: cleaning_mode.png] setelah contoh kasus ketiga),
2. 'Mode Pendamping' (10 contoh interaksi seperti percakapan santai atau motivasi pagi, 5 dialog sampel, fitur AI seperti Pembelajaran Emosi, Analisis Suasana Hati, tambah [IMAGE: companion_mode.png] setelah dialog kedua).
Sertakan kode error (CL-303: Sensor debu error, PR-101: AI gagal, NS-201: Suara berisik, AP-301: Koneksi aplikasi gagal, CK-401: Memasak tidak merata) di konteks relevan dengan penjelasan mendalam.
"""
response1 = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": prompt_part1}],
    max_tokens=config.MAX_TOKENS
)
part1 = response1.choices[0].message.content

# Run 2: Mode Kendaraan (~4000-5000 kata)
prompt_part2 = f"""
{config.GLOBAL_PROMPT}
Buat bagian 'Pengoperasian' bagian 2 (4500 kata) dalam Bahasa Indonesia untuk panduan pengguna 'GeralBot'. Fokus pada:
1. 'Mode Motor' (langkah detail 10 tahap, 5 skenario penggunaan seperti perjalanan kota atau hujan ringan, spesifikasi teknis seperti kecepatan, suspensi, tambah [IMAGE: motor_mode.png] setelah skenario kedua),
2. 'Mode Mobil' (langkah detail 10 tahap, 5 skenario seperti liburan keluarga atau belanja, spesifikasi seperti kapasitas, bagasi, tambah [IMAGE: car_mode.png] setelah skenario ketiga),
3. 'Mode Pod Terbang' (langkah detail 10 tahap, 5 skenario seperti perjalanan cepat atau darurat, spesifikasi seperti ketinggian, propulsi, tambah [IMAGE: pod_mode.png] setelah skenario pertama)).
Sertakan kode error (TF-404: Transformasi gagal, PT-502: Pod tidak stabil, BO-707: Baterai overheat, NV-501: Navigasi terganggu, LI-601: Lampu indikator mati) di konteks relevan dengan analisis mendalam.
"""
response2 = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": prompt_part2}],
    max_tokens=config.MAX_TOKENS
)
part2 = response2.choices[0].message.content

# Gabungin ke operation.txt
with open("operation.txt", "w", encoding="utf-8") as f:
    f.write("Pengoperasian\n\n" + part1 + "\n\n" + part2)

print("Operation text generation complete!")