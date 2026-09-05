import json
import pypdf

# 1. استخراج الصفحات من 47 إلى 166 (توازي index 46 إلى 166 في pypdf)
pdf_path = "1830_Technical_Description.pdf"
reader = pypdf.PdfReader(pdf_path)

extracted_pages = []
for page_num in range(46, 166):
  text = reader.pages[page_num].extract_text()
  extracted_pages.append({"page_number": page_num + 1, "text": text})

# 2. تقطيع النصوص لـ Chunks بحجم مناسب (100-300 كلمة) مع حفظ رقم الصفحة
chunks = []
for page in extracted_pages:
  page_num = page["page_number"]
  paragraphs = page["text"].split("\n\n")

  current_chunk = ""
  for para in paragraphs:
    clean_para = para.strip().replace("\n", " ")
    if not clean_para:
      continue

    if len((current_chunk + " " + clean_para).split()) <= 250:
      current_chunk += " " + clean_para
    else:
      if len(current_chunk.split()) >= 50:
        chunks.append({
            "text": current_chunk.strip(),
            "page_number": page_num,
            "section": f"Page {page_num} Description",
        })
      current_chunk = clean_para

  if current_chunk.strip():
    chunks.append({
        "text": current_chunk.strip(),
        "page_number": page_num,
        "section": f"Page {page_num} Description",
    })

# 3. حفظ الناتج في ملف JSON
with open("chunks.json", "w", encoding="utf-8") as f:
  json.dump(chunks, f, ensure_ascii=False, indent=4)

print(f"تم بنجاح! تم استخراج وحفظ {len(chunks)} قطعة نصية (Chunk).")
