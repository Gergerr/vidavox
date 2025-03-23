# generate_pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
from graphviz import Digraph
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Setup PDF
doc = SimpleDocTemplate("Geraldo_synthetic_data.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

# Tambah style dengan Times New Roman, ukuran font, dan spacing 1.5
styles.add(ParagraphStyle(
    name='CustomTitle',
    fontName='Times-Roman',
    fontSize=18,
    leading=27,   # 18 * 1.5
    alignment=1,  # Center
    fontWeight='bold'
))
styles.add(ParagraphStyle(
    name='CustomHeading1',
    fontName='Times-Roman',
    fontSize=14,
    leading=21,   # 14 * 1.5
    fontWeight='bold'
))
styles.add(ParagraphStyle(
    name='CustomHeading2',
    fontName='Times-Roman',
    fontSize=12,
    leading=18,   # 12 * 1.5
    fontWeight='bold'
))
# Tambah style untuk Heading 3, 4, 5
styles.add(ParagraphStyle(
    name='CustomHeading3',
    fontName='Times-Roman',
    fontSize=11,
    leading=16.5, # 11 * 1.5
    fontWeight='bold'
))
styles.add(ParagraphStyle(
    name='CustomHeading4',
    fontName='Times-Roman',
    fontSize=10,
    leading=15,   # 10 * 1.5
    fontWeight='bold'
))
styles.add(ParagraphStyle(
    name='CustomHeading5',
    fontName='Times-Roman',
    fontSize=9,
    leading=13.5, # 9 * 1.5
    fontWeight='bold'
))
styles.add(ParagraphStyle(
    name='CustomNormal',
    fontName='Times-Roman',
    fontSize=10,
    leading=15    # 10 * 1.5
))
styles.add(ParagraphStyle(
    name='CustomBullet',
    fontName='Times-Roman',
    fontSize=10,
    leading=15,   # 10 * 1.5
    leftIndent=20,
    bulletIndent=10
))

# Fungsi buat parse Markdown dengan nomor otomatis dan gambar di tengah
def parse_markdown(file_path, heading_num):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Page break sebelum heading utama
    story.append(PageBreak())
    story.append(Paragraph(f"{heading_num}. {os.path.splitext(os.path.basename(file_path))[0].replace('_', ' ').title()}", styles["CustomHeading1"]))
    story.append(Spacer(1, 12))
    
    lines = text.split("\n")
    subheading_count = 0
    subsubheading_count = 0
    subsubsubheading_count = 0
    subsubsubsubheading_count = 0
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue
        # Heading 1
        if line.startswith("# "):
            subheading_count = 0
            subsubheading_count = 0
            subsubsubheading_count = 0
            subsubsubsubheading_count = 0
            story.append(Paragraph(f"{heading_num}. {line[2:]}", styles["CustomHeading1"]))
        # Heading 2
        elif line.startswith("## "):
            subheading_count += 1
            subsubheading_count = 0
            subsubsubheading_count = 0
            subsubsubsubheading_count = 0
            story.append(Paragraph(f"{heading_num}.{subheading_count} {line[3:]}", styles["CustomHeading2"]))
        # Heading 3
        elif line.startswith("### "):
            subsubheading_count += 1
            subsubsubheading_count = 0
            subsubsubsubheading_count = 0
            story.append(Paragraph(f"{heading_num}.{subheading_count}.{subsubheading_count} {line[4:]}", styles["CustomHeading3"]))
        # Heading 4
        elif line.startswith("#### "):
            subsubsubheading_count += 1
            subsubsubsubheading_count = 0
            story.append(Paragraph(f"{heading_num}.{subheading_count}.{subsubheading_count}.{subsubsubheading_count} {line[5:]}", styles["CustomHeading4"]))
        # Heading 5
        elif line.startswith("##### "):
            subsubsubsubheading_count += 1
            story.append(Paragraph(f"{heading_num}.{subheading_count}.{subsubheading_count}.{subsubsubheading_count}.{subsubsubsubheading_count} {line[6:]}", styles["CustomHeading5"]))
        # Bullet point dengan bold/italic
        elif line.startswith("* "):
            content = line[2:]
            content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
            content = re.sub(r'\*(.+?)\*', r'<i>\1</i>', content)
            story.append(Paragraph(f"• {content}", styles["CustomBullet"]))
        # Gambar di tengah paragraf
        elif "[IMAGE:" in line:
            match = re.search(r'\[IMAGE:\s*([^\]]+)\]', line, re.IGNORECASE)
            if match:
                image_name = match.group(1).strip()
                if not image_name.lower().endswith('.png'):
                    image_name += '.png'
                image_path = os.path.join("pictures", image_name)
                parts = re.split(r'\[IMAGE:\s*[^\]]+\]', line, flags=re.IGNORECASE)
                for i, part in enumerate(parts):
                    if i % 2 == 0:  # Teks biasa
                        if part.strip():
                            part = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', part)
                            part = re.sub(r'\*(.+?)\*', r'<i>\1</i>', part)
                            part = re.sub(r'<br\s*[^>]*>(.*?)</br>', r'<br/>\1', part)
                            part = re.sub(r'<br\s*[^>]*>', r'<br/>', part)
                            part = re.sub(r'</br>', r'<br/>', part)
                            story.append(Paragraph(part, styles["CustomNormal"]))
                    else:  # Nama file gambar
                        found = False
                        for f in os.listdir("pictures"):
                            if f.lower() == image_name.lower():
                                image_path = os.path.join("pictures", f)
                                found = True
                                break
                        if found:
                            logging.info(f"Found image: {image_path}")
                            story.append(Image(image_path, width=300, height=200))
                        else:
                            logging.warning(f"Image not found: {image_path}, using placeholder")
                            plt.figure(figsize=(5, 3))
                            plt.text(0.5, 0.5, f"Placeholder: {image_name}", ha='center', va='center')
                            plt.axis('off')
                            plt.savefig("pictures/placeholder.png", dpi=100)
                            plt.close()
                            story.append(Image("pictures/placeholder.png", width=300, height=200))
                        story.append(Spacer(1, 12))
            else:
                logging.warning(f"Invalid IMAGE tag in line: {line}")
                story.append(Paragraph(line, styles["CustomNormal"]))
        else:
            line = re.sub(r'<br\s*[^>]*>(.*?)</br>', r'<br/>\1', line)
            line = re.sub(r'<br\s*[^>]*>', r'<br/>', line)
            line = re.sub(r'</br>', r'<br/>', line)
            line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'\*(.+?)\*', r'<i>\1</i>', line)
            story.append(Paragraph(line, styles["CustomNormal"]))
    story.append(Spacer(1, 12))

# Cover Page
story.append(Paragraph("Panduan Pengguna GeralBot", styles["CustomTitle"]))
story.append(Paragraph("NexTech Inovasi", styles["CustomNormal"]))
story.append(Paragraph("Model: GeralBot V3.5", styles["CustomNormal"]))
story.append(Paragraph("Versi Manual: 1.0, Maret 2025", styles["CustomNormal"]))
story.append(PageBreak())

# Tambah semua bagian teks dengan nomor heading
sections = [
    ("text/intro.txt", "Pengenalan"),
    ("text/safety.txt", "Petunjuk Keselamatan"),
    ("text/getting_started.txt", "Memulai"),
    ("text/operation.txt", "Pengoperasian"),
    ("text/troubleshooting.txt", "Pemecahan Masalah"),
    ("text/technical_specs.txt", "Spesifikasi Teknis"),
    ("text/warranty.txt", "Informasi Garansi"),
    ("text/appendices.txt", "Apendiks")
]
for i, (file_path, title) in enumerate(sections, start=1):
    if os.path.exists(file_path):
        parse_markdown(file_path, i)
    else:
        print(f"Warning: {file_path} not found, skipping...")


# Tabel: Log Penggunaan dari synthetic_data.csv
df = pd.read_csv("synthetic_data.csv").head(10)
table_data = [df.columns.values.tolist()] + df.values.tolist()
story.append(Paragraph("Log Penggunaan GeralBot (Sample)", styles["CustomHeading2"]))
story.append(Table(table_data, colWidths=[50] * 10, style=[
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman')
]))
story.append(Spacer(1, 12))


# Build PDF
doc.build(story)
print("PDF generation complete: Geraldo_synthetic_data.pdf")