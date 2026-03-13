"""
RAGnosis Models README
======================

This directory contains:

1. build_rag_index.py    - Script to build FAISS vector index (run once!)
2. faiss_index/          - Generated FAISS index (created by build_rag_index.py)
   ├── index.faiss       - Binary FAISS index file
   └── chunks.json       - Text chunks corresponding to each vector

## Quick Start

Build the RAG index (required before first run):

    cd e:\\Projects\\RAGnosis
    python models/build_rag_index.py

## Model Information

### Embedding Model (for RAG)
- Name: sentence-transformers/all-MiniLM-L6-v2
- Dimension: 384
- Downloads from HuggingFace on first use (~90MB)

### Summarization Model (BART)
- Name: facebook/bart-large-cnn
- Parameters: 406M
- Downloads from HuggingFace on first use (~1.6GB)
- First inference takes 30-60s; subsequent runs cached

### BioBERT (Entity Recognition)
- Name: dmis-lab/biobert-base-cased-v1.1
- Pretrained on PubMed + PMC biomedical literature
- Used for medical entity extraction

## Training Notebook
See: ../notebooks/train_bert_medical.ipynb
"""
