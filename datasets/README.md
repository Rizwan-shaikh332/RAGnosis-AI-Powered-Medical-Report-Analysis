# Datasets — RAGnosis

## Files

### 1. `medical_knowledge_base.jsonl`
**Format**: JSON Lines (one JSON object per line)  
**Records**: 25 medical QA pairs  
**Fields**: `question`, `answer`, `category`, `source`  
**Categories**: Blood Tests, Diabetes, Cardiology, Kidney, Liver, Thyroid, Metabolic, Iron Studies, Vitamins, General  
**Source**: Adapted from MedQuAD (Medical Question Answering Dataset)  
**Usage**: Embedded using `sentence-transformers/all-MiniLM-L6-v2` → FAISS index for RAG retrieval

### 2. `blood_report_reference.csv`
**Format**: CSV  
**Records**: 34 lab parameters  
**Columns**: `test_name, abbreviation, normal_min, normal_max, unit, category, low_interpretation, high_interpretation`  
**Categories**: CBC, Diabetes, Lipids, Kidney, Liver, Thyroid, Metabolic, Iron Studies, Vitamins, Vitals  
**Source**: Standard clinical reference ranges (WHO / ICMR guidelines)  
**Usage**: Used by `bert_summarizer.py` to interpret patient metric values as Normal / High / Low

## How to Expand the Dataset

To add more QA pairs to the knowledge base:
1. Add new JSON lines to `medical_knowledge_base.jsonl`
2. Re-run: `python models/build_rag_index.py`
3. Restart the Flask backend

To add more lab parameters:
1. Add rows to `blood_report_reference.csv`
2. Update regex patterns in `backend/services/text_extractor.py`
