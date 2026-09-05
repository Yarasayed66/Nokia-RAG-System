import json
import time
import google.generativeai as genai
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. وضع مفتاح API الجديد
GEMINI_API_KEY = "AQ.Ab8RN6L3nbIZ0ubo651nhgKBgPd_ZDVF27nu_Pdf3BxZd_rUtw"
genai.configure(api_key=GEMINI_API_KEY)
llm = genai.GenerativeModel("gemini-flash-latest")

# 2. تحميل البيانات والموديل
embeddings = np.load("embeddings.npy")
with open("chunks.json", "r", encoding="utf-8") as f:
  chunks = json.load(f)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# 3. دالة حساب التشابه (Cosine Similarity)
def cosine_similarity(query_vec, doc_vecs):
  dot_product = np.dot(doc_vecs, query_vec)
  norms = np.linalg.norm(doc_vecs, axis=1) * np.linalg.norm(query_vec)
  return dot_product / norms


# 4. دالة البحث وتوليد الإجابة
def answer_question(question, top_k=3):
  query_vec = embed_model.encode(question)
  scores = cosine_similarity(query_vec, embeddings)
  top_indices = np.argsort(scores)[::-1][:top_k]

  context = ""
  for idx in top_indices:
    c = chunks[idx]
    context += f"\n[Section: {c['section']}, Page: {c['page_number']}]\n{c['text']}\n"

  prompt = f"""You are a site-engineering assistant for the Nokia 1830 PSS system.
Answer the user's question STRICTLY using ONLY the context provided below.

STRICT RULES:
1. Cite the exact page number(s) and section heading used for your answer.
2. If the context does NOT contain the full answer, reply ONLY with: "Not found in the provided document." Do NOT guess or use outside knowledge.

Context:
{context}

Question: {question}
Answer:"""

  response = llm.generate_content(prompt)
  return response.text


# 5. قائمة الأسئلة الثمانية
questions = [
    (
        "1. How many slots does the 1830 PSS-8 shelf provide, and what is its"
        " rack-unit (RU) footprint?"
    ),
    (
        "2. What rack-unit footprint does the 1830 PSS-32 shelf have, and how"
        " many slots does it provide?"
    ),
    (
        "3. What are the two software load-lines supported by the 1830 PSS"
        " system?"
    ),
    "4. Which fan units are supported on the 1830 PSS-32 shelf?",
    "5. Which fan unit(s) are used on the 1830 PSS-16II shelf?",
    "6. Name the power filter cards supported on the 1830 PSS-8 shelf.",
    (
        "7. What is the required horizontal rack aperture for mounting a 1830"
        " PSS-8 shelf, and which common aperture size is explicitly NOT"
        " supported?"
    ),
    (
        "8. What is the maximum optical reach, in kilometers, of the 1830 PSS-8"
        " shelf without amplification?"
    ),
]

for q in questions:
  print(f"\n==========================================")
  print(q)
  print(f"------------------------------------------")
  try:
    print(answer_question(q))
  except Exception as e:
    print(f"حدث خطأ مؤقت، جاري إعادة المحاولة: {e}")
    time.sleep(35)
    print(answer_question(q))
  time.sleep(12)