from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Global prompt
global_prompt = """
Langsung buat teksnya. Jangan tulis kalimat seperti: "Berikut adalah 10-20 kata untuk blablabla" atau sejenisnya.  
Robot ini bernama 'GeralBot', sebuah robot multifungsi dari NexTech Inovasi. GeralBot dirancang sebagai pembantu rumah, pendamping emosional, dan kendaraan transformasi (motor, mobil, pod terbang seperti drop pod Fortnite). Fitur utamanya meliputi pembersihan rumah cerdas, interaksi emosional, transformasi kendaraan, memasak otomatis, dan segala fungsi untuk membantu manusia atau pemiliknya. Gunakan gaya realistis seperti panduan produk asli, tapi pastikan semua detail imajiner dan tidak berdasarkan fakta nyata.  
Sertakan judul bagian yang relevan di awal teks (misalnya 'Pengenalan', 'Petunjuk Keselamatan') dan tambahkan subjudul jika sesuai (misalnya 'Mode Motor' di bawah 'Pengoperasian'). Gunakan format teks sederhana yang mudah dibaca.
"""

# Introduction
intro_prompt = f"""
{global_prompt}
Buat pengenalan 2500 hingga 3500 kata dalam Bahasa Indonesia untuk panduan pengguna robot multifungsi 'GeralBot'. Jelaskan tujuan robot sebagai pembantu rumah, pendamping, dan kendaraan transformasi (motor, mobil, pod terbang seperti drop pod Fortnite). Highlight fitur utama secara umum (pembersihan rumah, interaksi emosional, transformasi kendaraan, memasak, dan segalanya terkait membantu manusia atau pemiliknya) dan manfaatnya bagi pengguna.
"""
response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[{"role": "user", "content": intro_prompt}],
    max_tokens=1600,
    temperature=0.7
)
with open("intro.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Intro text generation complete!")