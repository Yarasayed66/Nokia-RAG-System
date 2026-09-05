# Nokia 1830 PSS Technical RAG System

An end-to-end Retrieval-Augmented Generation (RAG) solution built to query and extract technical specification data from the **Nokia 1830 PSS** technical documentation. 

This system breaks down raw engineering documentation into indexed data chunks, vectorizes them using local embedding models, and leverages the **Google Gemini API** to generate accurate, context-bound answers with mandatory page and section citations.

---

## 🛠️ System Architecture & Workflow

1. **Document Ingestion & Chunking (`step1_chunking.py`)**:
   * Parses the PDF manual using `pypdf`.
   * Cleans text and splits content into logical chunks while preserving page numbers and section header metadata (`chunks.json`).

2. **Vector Indexing & Embeddings (`step2_indexing.py`)**:
   * Converts textual chunks into dense vector representations using the `sentence-transformers/all-MiniLM-L6-v2` model.
   * Stores vector representations locally in `embeddings.npy` for fast offline cosine similarity lookup.

3. **Contextual Retrieval & Generation (`step3_rag.py`)**:
   * Computes cosine similarity between user queries and stored chunk embeddings.
   * Retrieves top context matches (`top_k`) and injects them into a strict prompt guardrail.
   * Interfaces with `gemini-1.5-flash` to return verifiable answers with precise citations, or explicitly returns *"Not found in the provided document"* if out-of-context.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* A Google AI Studio Gemini API Key

### Installation

1. Clone this repository:
   ```bash
   git clone [https://github.com/Yarasayed66/Nokia-RAG-System.git](https://github.com/Yarasayed66/Nokia-RAG-System.git)
   cd Nokia-RAG-System
