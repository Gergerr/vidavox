from groq import Groq
import os
import config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Introduction
intro_prompt = f"""
{config.GLOBAL_PROMPT}
Buat pengenalan 2500 hingga 3500 kata dalam Bahasa Indonesia untuk panduan pengguna robot multifungsi 'GeralBot'. Jelaskan tujuan robot sebagai pembantu rumah, pendamping, dan kendaraan transformasi (motor, mobil, pod terbang seperti drop pod Fortnite). Highlight fitur utama secara umum (pembersihan rumah, interaksi emosional, transformasi kendaraan, memasak, dan segalanya terkait membantu manusia atau pemiliknya) dan manfaatnya bagi pengguna.
"""
response = client.chat.completions.create(
    model=config.MODEL,
    messages=[{"role": "user", "content": intro_prompt}],
    max_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE
)
with open("intro.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

print("Intro text generation complete!")