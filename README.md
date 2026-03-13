# 🩺 RAGnosis — AI-Powered Medical Report Analysis

> **PICT InC 2025** · Pune Institute of Computer Technology  
> An intelligent medical report analysis system powered by RAG + BERT + BART + Groq

[![React](https://img.shields.io/badge/Frontend-React_Vite-61dafb?logo=react)](https://vitejs.dev)
[![Flask](https://img.shields.io/badge/Backend-Flask-000?logo=flask)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB_Atlas-47A248?logo=mongodb)](https://www.mongodb.com)
[![HuggingFace](https://img.shields.io/badge/AI-HuggingFace_Transformers-FCD34D?logo=huggingface)](https://huggingface.co)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Pages](#-pages)
- [Datasets](#-datasets)
- [AI Models](#-ai-models)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [API Endpoints](#-api-endpoints)

---

## 🌟 Overview

RAGnosis revolutionizes patient care by simplifying medical report analysis. Patients upload reports (PDF, JPG, PNG) and receive:
- 🧠 **AI-generated summaries** using BART transformer
- 🔍 **RAG-powered Q&A** with medical knowledge retrieval via FAISS
- 📊 **Health metrics visualization** (blood values, trends, charts)
- 🤖 **Interactive chatbot** powered by Groq + LLaMA 3 + RAG

---

## 🛠 Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18 + Vite, Framer Motion, Recharts, React Router v6, Axios |
| **Backend** | Python Flask, PyJWT, bcrypt, Flask-CORS |
| **Database** | MongoDB Atlas (PyMongo) |
| **AI Models** | `facebook/bart-large-cnn`, `dmis-lab/biobert-base-cased-v1.1`, `sentence-transformers/all-MiniLM-L6-v2` |
| **RAG** | FAISS vector index + sentence-transformers embeddings |
| **Chatbot** | Groq API → `llama3-8b-8192` model |
| **OCR** | pdfplumber (PDF), pytesseract (images) |
| **Design** | Dark Navy + Cyan glassmorphism UI |

---

## 📄 Pages

### 1. 🏠 Landing Page (`/`)
**Purpose**: Marketing homepage for RAGnosis.  
**Content**:
- Hero section with animated gradient text and stats (10K+ reports, 98% accuracy)
- Features grid (BERT+BART Analysis, RAG Knowledge Base, Health Charts, AI Chatbot, Security, Multi-format)
- 4-step process visualization (Upload → Extract → Retrieve → Insights)
- Call-to-action section
- Background grid pattern with floating orb effects (Framer Motion)

### 2. ⚡ System Animation (`/system`) — _For Presentation_
**Purpose**: Standalone animated visualization of the entire AI pipeline. **Perfect for jury/demo presentations.**  
**Content**:
- Auto-playing pipeline with 7 animated steps with moving data packets
- Steps: PDF Input → NLP Preprocessing → BioBERT → FAISS RAG → BART → Groq LLM → Dashboard Output
- Each step: icon, model name, description, tech badges, "Technical Deep Dive" toggle with detailed explanation
- Color-coded active node with pulsing border and glow
- Dot indicators + Play/Pause control
- Full Tech Stack summary grid (Frontend, Backend, AI Models, RAG, Database, Infrastructure)

### 3. 📝 Register (`/register`)
**Purpose**: User account creation with full medical profile.  
**Fields** (2-column grid):
- Full Name*, Email*, Mobile Number*, Password*
- Age*, Height (inches)*, Weight (kg)
- Blood Pressure (optional), Blood Group (optional), Gender*
- JWT token returned on success → auto-redirects to dashboard

### 4. 🔐 Login (`/login`)
**Purpose**: User authentication via email OR mobile number.  
**Features**:
- Single identifier field accepts either email or 10-digit mobile
- Password field with validation
- Login tip displayed below form
- JWT stored in localStorage, Axios header set globally

### 5. 📊 Dashboard (`/dashboard`)
**Purpose**: The main user workspace after login.  
**Sidebar navigation with 6 tabs**:

| Tab | Icon | Description |
|-----|------|-------------|
| **Overview** | 🏠 | Welcome banner, stats (reports count, this month, active sessions), latest report card with AI summary and metric chips |
| **Upload Report** | 📤 | Drag-and-drop zone (PDF/JPG/PNG/JPEG, 16MB max), real-time upload progress, AI summary + extracted health values displayed after processing |
| **My Reports** | 📋 | Card grid of all reports with type icon, filename, date, metric chips, summary preview |
| **Health Metrics** | 📊 | Metric cards (NORMAL/HIGH/LOW status), Recharts BarChart of latest values, LineChart trend over multiple reports |
| **AI Chatbot** | 🤖 | Chat interface with Groq + RAG, report context selector, quick suggestion chips, streaming responses |
| **My Profile** | 👤 | Display all user profile fields in a card grid |

---

## 📁 Datasets

Located in `datasets/` folder:

| File | Description | Records |
|------|-------------|---------|
| `medical_knowledge_base.jsonl` | Medical QA pairs for FAISS RAG retrieval | 25 QA pairs covering CBC, diabetes, thyroid, liver, kidney, cardiology |
| `blood_report_reference.csv` | Lab test reference ranges with clinical interpretations | 34 parameters (hemoglobin, glucose, TSH, creatinine, etc.) |
| `README.md` | Dataset descriptions and sources |

**Data Sources**: MedQuAD dataset (adapted), clinical reference ranges from standard medical guidelines.

---

## 🧠 AI Models

### BART (Summarization)
- **Model**: `facebook/bart-large-cnn` — 406M parameters
- **Task**: Medical report → patient-friendly summary
- **Architecture**: Seq2seq encoder-decoder with beam search (max 300 tokens)
- **Where**: `backend/services/bert_summarizer.py`

### BioBERT (Entity Recognition)
- **Model**: `dmis-lab/biobert-base-cased-v1.1` — BERT fine-tuned on PubMed+PMC
- **Task**: Medical named entity recognition (diseases, drugs, lab values)
- **Architecture**: Bidirectional Transformer, 768-dim embeddings, 30K vocab

### RAG (Retrieval-Augmented Generation)
- **Embedder**: `sentence-transformers/all-MiniLM-L6-v2` — 384-dim dense vectors
- **Index**: FAISS `IndexFlatIP` (cosine similarity, top-K=5 retrieval)
- **Knowledge Base**: 25 medical QA pairs → JSONL → embedded → FAISS index
- **Build index**: `python models/build_rag_index.py`
- **Where**: `backend/services/rag_engine.py`, `models/build_rag_index.py`

### Groq (LLM Chat)
- **Model**: `llama3-8b-8192` via Groq API
- **Task**: Answer patient questions with RAG context + report context
- **Speed**: 500+ tokens/sec on Groq LPU hardware
- **Where**: `backend/services/groq_service.py`

### BERT Training Notebook
- **Location**: `notebooks/train_bert_medical.ipynb`
- **Purpose**: Fine-tune BERT on medical text classification for presentation
- Ready for Google Colab GPU runtime

---

## 📁 Project Structure

```
RAGnosis/
├── frontend/                    # React Vite application
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx  # Homepage
│   │   │   ├── SystemAnimation.jsx  # Pipeline animation (for demos!)
│   │   │   ├── RegisterPage.jsx # Registration with medical profile
│   │   │   ├── LoginPage.jsx    # Email or mobile login
│   │   │   └── Dashboard.jsx    # Main user dashboard (6 tabs)
│   │   ├── components/
│   │   │   └── Navbar.jsx       # Navigation bar
│   │   ├── context/
│   │   │   └── AuthContext.jsx  # JWT auth state management
│   │   ├── App.jsx              # Router + protected routes
│   │   ├── main.jsx             # React entry point
│   │   └── index.css            # Global design system (dark navy theme)
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/                     # Flask API server
│   ├── app.py                   # App factory + blueprints
│   ├── config.py                # All configuration + env vars
│   ├── database.py              # MongoDB singleton connection
│   ├── routes/
│   │   ├── auth.py             # /api/auth/register, /api/auth/login
│   │   ├── reports.py          # /api/reports/upload, list, get
│   │   └── chatbot.py          # /api/chat/
│   ├── models/
│   │   ├── user_model.py       # User CRUD operations
│   │   └── report_model.py     # Report CRUD operations
│   ├── services/
│   │   ├── text_extractor.py   # PDF + OCR text extraction + metric regex
│   │   ├── bert_summarizer.py  # BART summarization + metric interpretation
│   │   ├── rag_engine.py       # FAISS retrieval + embedding
│   │   └── groq_service.py     # Groq LLM chat with RAG context
│   ├── utils/
│   │   └── jwt_helper.py       # JWT encode/decode + auth decorator
│   ├── uploads/                # Uploaded report files (auto-created)
│   ├── requirements.txt
│   └── .env.template
│
├── datasets/                    # Medical training & reference data
│   ├── medical_knowledge_base.jsonl  # 25 medical QA pairs for RAG
│   ├── blood_report_reference.csv    # 34 lab parameters with ranges
│   └── README.md
│
├── models/                      # ML model scripts
│   ├── build_rag_index.py       # Build FAISS index (run once!)
│   └── faiss_index/            # Generated FAISS index files (after build)
│
├── notebooks/                   # Jupyter training notebooks
│   └── train_bert_medical.ipynb # BERT fine-tuning (Google Colab ready)
│
└── README.md                    # This file
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB Atlas account (provided)
- Groq API key (free at [console.groq.com](https://console.groq.com))

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate    
.\venv\Scripts\Activate      # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.template .env
# Edit .env and add your GROQ_API_KEY

# Build RAG knowledge index (run ONCE)
cd ..
python models/build_rag_index.py
cd backend

# Start the Flask server
python app.py
```

Server runs at: `http://localhost:5000`

### 2. Frontend Setup

```bash
cd frontend

# Install packages
npm install

# Start development server
npm run dev
```

App runs at: `http://localhost:5173`

### 3. Install Tesseract OCR (for image reports)

**Windows**: Download from [github.com/UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)  
Add to PATH or set in pytesseract: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

---

## 🔌 API Endpoints

| Method | Route | Description | Auth |
|--------|-------|-------------|------|
| GET | `/api/health` | Health check | ❌ |
| POST | `/api/auth/register` | Register new user | ❌ |
| POST | `/api/auth/login` | Login (email/mobile) | ❌ |
| GET | `/api/auth/me` | Get current user | ✅ JWT |
| POST | `/api/reports/upload` | Upload & analyze report | ✅ JWT |
| GET | `/api/reports/` | List user's reports | ✅ JWT |
| GET | `/api/reports/<id>` | Get single report | ✅ JWT |
| POST | `/api/chat/` | Chatbot message + RAG | ✅ JWT |
| GET | `/api/chat/suggestions` | Default chat questions | ✅ JWT |

---

## 🏫 Credits

**RAGnosis** — PICT InC 2025 Project  
Pune Institute of Computer Technology, Pune - 411043

Built with ❤️ using:
- [HuggingFace Transformers](https://huggingface.co)
- [FAISS](https://github.com/facebookresearch/faiss) by Meta AI
- [Groq](https://groq.com) for ultra-fast LLM inference
- [React](https://react.dev) + [Vite](https://vitejs.dev)
- [MongoDB Atlas](https://www.mongodb.com/atlas)
