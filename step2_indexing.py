import json
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. تحميل الـ Chunks التي استخرجناها في الخطوة الأولى
with open("chunks.json", "r", encoding="utf-8") as f:
  chunks = json.load(f)

texts = [c["text"] for c in chunks]

print("جاري تحويل النصوص إلى Embeddings (Vectors)...")

# 2. تحميل نموذج Sentence Transformers الموصى به في التاسك
model = SentenceTransformer("all-MiniLM-L6-v2")

# 3. حساب الـ Embeddings لجميع القطع النصية
embeddings = model.encode(texts, show_progress_bar=True)

# 4. حفظ المتجهات على القرص بصيغة npy لعدم إعادة الحساب
np.save("embeddings.npy", embeddings)

print(
    f"تم بنجاح! تم إنشاء وحفظ الفهرس لأبعاد: {embeddings.shape} في ملف embeddings.npy"
)