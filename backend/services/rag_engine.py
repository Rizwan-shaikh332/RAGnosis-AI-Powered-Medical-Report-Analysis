import json
import os
from config import Config

# Lazy load
_index = None
_chunks = []
_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        try:
            from sentence_transformers import SentenceTransformer
            print("⏳ Loading embedding model...")
            _embedder = SentenceTransformer(Config.EMBEDDING_MODEL)
            print("✅ Embedding model loaded!")
        except ImportError:
            print("⚠️  sentence-transformers not installed. RAG will use fallback context only.")
            _embedder = "fallback"
    return _embedder

def load_index():
    global _index, _chunks
    if _index is not None:
        return
    index_path = Config.FAISS_INDEX_PATH
    chunks_path = os.path.join(index_path, "chunks.json")
    faiss_path = os.path.join(index_path, "index.faiss")

    if os.path.exists(faiss_path) and os.path.exists(chunks_path):
        import faiss
        _index = faiss.read_index(faiss_path)
        with open(chunks_path, "r", encoding="utf-8") as f:
            _chunks = json.load(f)
        print(f"✅ FAISS index loaded with {len(_chunks)} chunks")
    else:
        print("⚠️  FAISS index not found. Run: python models/build_rag_index.py")
        _index = None
        _chunks = []

def retrieve_context(query: str, report_text: str = "", top_k: int = 5) -> str:
    """Retrieve relevant medical knowledge for a query."""
    load_index()
    embedder = get_embedder()

    # If embedder not available, use fallback immediately
    if embedder == "fallback":
        return get_fallback_context(query)

    combined_query = f"{query} {report_text[:500]}" if report_text else query

    if _index is None or len(_chunks) == 0:
        return get_fallback_context(query)

    try:
        import faiss
        query_vec = embedder.encode([combined_query], convert_to_numpy=True).astype("float32")
        faiss.normalize_L2(query_vec)
        distances, indices = _index.search(query_vec, top_k)
        retrieved = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(_chunks):
                retrieved.append(_chunks[idx]["text"])
        return "\n\n".join(retrieved)
    except Exception as e:
        print(f"RAG retrieval error: {e}")
        return get_fallback_context(query)


def get_fallback_context(query: str) -> str:
    """Return hardcoded fallback context when index is not available."""
    query_lower = query.lower()
    contexts = {
        "hemoglobin": "Hemoglobin normal range: Men 13.5–17.5 g/dL, Women 12.0–15.5 g/dL. Low levels indicate anemia; high levels may suggest polycythemia.",
        "glucose": "Fasting blood glucose normal: 70–100 mg/dL. 100–125 prediabetes. Above 126 mg/dL indicates diabetes.",
        "cholesterol": "Total cholesterol <200 mg/dL is desirable. 200–239 borderline high. >240 mg/dL is high risk.",
        "blood pressure": "Normal BP: <120/80 mmHg. Elevated: 120–129/<80. Stage 1 hypertension: 130–139/80–89. Stage 2: ≥140/≥90.",
        "tsh": "TSH normal range: 0.4–4.0 mIU/L. Low TSH suggests hyperthyroidism; high TSH suggests hypothyroidism.",
        "creatinine": "Serum creatinine normal: Men 0.7–1.2 mg/dL, Women 0.5–1.0 mg/dL. Elevated levels suggest kidney dysfunction.",
        "platelet": "Normal platelet count: 150,000–400,000 per µL. Low platelets (thrombocytopenia) increases bleeding risk.",
        "wbc": "Normal WBC count: 4,500–11,000 cells/µL. High WBC may indicate infection or inflammation."
    }
    for key, ctx in contexts.items():
        if key in query_lower:
            return ctx
    return "Please consult your doctor for specific medical advice. RAGnosis provides educational summaries only."
