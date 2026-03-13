"""
RAGnosis - Build FAISS Vector Index from Medical Knowledge Base
=================================================================
Run this script ONCE before starting the backend:
    cd e:\\Projects\\RAGnosis
    python models/build_rag_index.py

This creates models/faiss_index/index.faiss and chunks.json
"""

import json
import os
import sys
import numpy as np

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "medical_knowledge_base.jsonl")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "faiss_index")

def load_knowledge_base(path):
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                # Create a rich text chunk combining Q and A
                text = f"Q: {obj['question']}\nA: {obj['answer']}\nCategory: {obj.get('category', '')}"
                chunks.append({
                    "text": text,
                    "question": obj["question"],
                    "answer": obj["answer"],
                    "category": obj.get("category", "General")
                })
            except json.JSONDecodeError as e:
                print(f"Warning: skipping malformed line: {e}")
    return chunks

def build_index(chunks, embedder):
    import faiss
    print(f"⚙️  Encoding {len(chunks)} knowledge chunks...")
    texts = [c["text"] for c in chunks]
    embeddings = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    embeddings = embeddings.astype("float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    # Build flat index (best for small datasets)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print(f"✅ FAISS index built with {index.ntotal} vectors (dim={dim})")
    return index

def main():
    print("🏗️  RAGnosis - Building Medical Knowledge FAISS Index")
    print("=" * 50)

    try:
        from sentence_transformers import SentenceTransformer
        import faiss
    except ImportError:
        print("❌ Missing packages. Run: pip install sentence-transformers faiss-cpu")
        sys.exit(1)

    # Load knowledge base
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        print(f"❌ Knowledge base not found: {KNOWLEDGE_BASE_PATH}")
        sys.exit(1)

    chunks = load_knowledge_base(KNOWLEDGE_BASE_PATH)
    print(f"📚 Loaded {len(chunks)} knowledge chunks")

    # Load embedding model
    print("⏳ Loading sentence-transformers model (first time downloads ~90MB)...")
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("✅ Embedding model ready!")

    # Build FAISS index
    index = build_index(chunks, embedder)

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    faiss_path = os.path.join(OUTPUT_DIR, "index.faiss")
    chunks_path = os.path.join(OUTPUT_DIR, "chunks.json")

    faiss.write_index(index, faiss_path)
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Index saved to: {faiss_path}")
    print(f"✅ Chunks saved to: {chunks_path}")
    print(f"\n🚀 RAG index is ready! Start the backend now.")

if __name__ == "__main__":
    main()
