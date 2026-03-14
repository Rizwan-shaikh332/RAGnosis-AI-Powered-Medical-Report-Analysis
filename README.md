# 🩺 RAGnosis — AI-Powered Medical Report Analysis & Hospital Portal

> **PICT InC 2025** · Pune Institute of Computer Technology  
> An intelligent medical report analysis system powered by RAG + BERT + BART + Groq, with an integrated Hospital Management Portal for Doctors and Receptionists.

[![React](https://img.shields.io/badge/Frontend-React_Vite-61dafb?logo=react)](https://vitejs.dev)
[![Flask](https://img.shields.io/badge/Backend-Flask-000?logo=flask)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB_Atlas-47A248?logo=mongodb)](https://www.mongodb.com)
[![HuggingFace](https://img.shields.io/badge/AI-HuggingFace_Transformers-FCD34D?logo=huggingface)](https://huggingface.co)
[![Groq](https://img.shields.io/badge/LLM-Groq_LLaMA3-f97316?logo=meta)](https://groq.com)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [AI Pipeline — How It Works](#-ai-pipeline--how-it-works)
- [Hospital Portal](#-hospital-portal)
- [Tech Stack](#-tech-stack)
- [Pages & Features](#-pages--features)
- [Datasets](#-datasets)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [API Endpoints](#-api-endpoints)
- [Demo Credentials](#-demo-credentials)

---

## 🌟 Overview

RAGnosis is a full-stack AI medical platform with **two major system components**:

### 1. 🔬 AI Medical Report Analysis (Patient-facing)
Patients upload blood reports (PDF, JPG, PNG) and instantly receive:
- 🧠 **AI-generated summaries** — plain-language explanation of medical values via BART transformer
- 🔍 **RAG-powered Q&A** — retrieve relevant medical knowledge from a curated FAISS index
- 📊 **Health metrics visualization** — automatic extraction and charting of blood values
- 🤖 **Interactive AI chatbot** — ask any question about your report using Groq + LLaMA 3 + RAG
- 💊 **Prescription viewer** — see prescriptions written by your doctor

### 2. 🏥 Hospital Management Portal (Doctor + Receptionist)
A complete hospital workflow system:
- **Receptionist** registers patients, books appointments, uploads blood reports
- **Doctor** views today's appointments, writes prescriptions
- **Patient** sees both AI-analyzed reports AND their prescriptions in one dashboard

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          RAGnosis Frontend (React + Vite)           │
│                                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐   │
│  │Patient      │  │Doctor        │  │Receptionist             │   │
│  │Dashboard    │  │Dashboard     │  │Dashboard                │   │
│  │/dashboard   │  │/doctor       │  │/receptionist            │   │
│  └──────┬──────┘  └──────┬───────┘  └───────────┬─────────────┘   │
└─────────┼────────────────┼─────────────────────-─┼─────────────────┘
          │ JWT (user)     │ JWT (doctor)          │ JWT (receptionist)
          ▼                ▼                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Flask REST API (backend/)                       │
│                                                                     │
│  /api/auth/*      /api/reports/*      /api/hospital/*              │
│  /api/chat/*      /api/reminders/*                                  │
└────────┬────────────────┬──────────────────────┬────────────────────┘
         │                │                      │
         ▼                ▼                      ▼
  ┌──────────────┐  ┌─────────────┐   ┌──────────────────────┐
  │ MongoDB Atlas │  │   AI Models  │   │ Groq API (LLaMA 3)  │
  │               │  │ BART / BERT  │   │ 500+ tokens/sec     │
  │ Collections:  │  │ FAISS Index  │   └──────────────────────┘
  │ - users       │  │ Sentence-    │
  │ - reports     │  │ Transformers │
  │ - doctors     │  └─────────────┘
  │ - receptionists│
  │ - appointments │
  │ - prescriptions│
  │ - reminders   │
  └───────────────┘
```

---

## 🧠 AI Pipeline — How It Works

When a patient (or receptionist) uploads a blood report, the following pipeline executes automatically:

### Step 1 — Text Extraction (`text_extractor.py`)
```
PDF Report  → pdfplumber  → Raw Text
Image Report → pytesseract (OCR) → Raw Text
```
- PDFs are parsed page-by-page using `pdfplumber`
- Scanned images use `pytesseract` (Tesseract OCR engine)
- A regex pipeline extracts **numeric health metrics** (hemoglobin, glucose, cholesterol, WBC, RBC, TSH, creatinine, etc.) with their values and units
- Results: `raw_text`, `metrics_dict` (28+ parameters)

### Step 2 — Named Entity Recognition (`bert_summarizer.py`)
```
Raw Text → BioBERT Tokenizer → [MASK] Predictions → Medical Entities
```
- **Model**: `dmis-lab/biobert-base-cased-v1.1` (fine-tuned BERT on PubMed + PMC biomedical papers)
- **Architecture**: 12-layer bidirectional Transformer, 768-dim embeddings, 30,000 vocab
- **Task**: Token-level classification to detect medical entities (diseases, drugs, abnormal values)
- Each extracted metric is compared against the `blood_report_reference.csv` database to determine **NORMAL / HIGH / LOW** status

### Step 3 — Report Summarization (`bert_summarizer.py`)
```
Raw Text (truncated to 1024 tokens) → BART Encoder → BART Decoder → Patient-friendly Summary
```
- **Model**: `facebook/bart-large-cnn` — 406M parameter seq2seq transformer
- **Architecture**: 12-layer encoder, 12-layer decoder, cross-attention between them
- **Decoding**: Beam search (4 beams), max 300 tokens, no-repeat ngram size=3
- **Output**: Plain-language summary ("Your hemoglobin is slightly low at 11.2 g/dL, which may indicate...")

### Step 4 — RAG Context Retrieval (`rag_engine.py`)
```
Report Text → Sentence-BERT → 384-dim Vector → FAISS MIPS Search → Top-5 Medical QA pairs
```
- **Embedder**: `sentence-transformers/all-MiniLM-L6-v2` — maps sentences to 384-dimensional dense vectors
- **Index**: FAISS `IndexFlatIP` (Maximum Inner Product Search = cosine similarity on L2-normalized vectors)
- **Knowledge Base**: 25 medical QA pairs covering CBC, diabetes, thyroid, liver, kidney, cardiology (stored in `datasets/medical_knowledge_base.jsonl`)
- **At query time**: The patient's question + report excerpt is embedded → nearest 5 chunks retrieved → injected into LLM context

### Step 5 — LLM Chat (`groq_service.py`)
```
[System Prompt] + [RAG Context] + [Report Excerpt] + [Chat History] → Groq API → Response
```
- **Provider**: Groq Cloud (LPU hardware — Liquid Processing Unit)
- **Model**: `llama3-8b-8192` — 8B parameter instruction-tuned LLaMA 3 model
- **Context window**: 8192 tokens
- **Speed**: ~500 tokens/second (10× faster than GPU inference)
- **RAG injection**: Top-5 retrieved medical QA pairs prepended as system context
- **Safety**: System prompt enforces educational tone, recommends professional consultation

### Full Pipeline Flow Diagram
```
Upload Blood Report
        │
        ▼
Text Extraction (pdfplumber / pytesseract)
        │
        ├──► Regex Metric Extraction → hemoglobin=11.2, glucose=105...
        │
        ▼
BioBERT NER → medical entities identified
        │
        ▼
BART Summarization → plain-language report summary
        │
        ▼
Sentence-BERT Embedding → 384-dim vector
        │
        ▼
FAISS Search → top-5 relevant medical QA retrieved
        │
        ▼
MongoDB Storage → report saved with all metadata
        │
        ▼
Patient Dashboard → summary + charts + chatbot ready
```

---

## 🏥 Hospital Portal

The hospital portal is a separate role-based system layered on top of RAGnosis.

### Role-Based JWT Authentication

Each JWT token carries a `role` field:
- `role: "user"` — regular patient
- `role: "doctor"` — doctor (issued by `/api/hospital/doctor/login`)
- `role: "receptionist"` — receptionist

The `require_role()` decorator on Flask routes enforces access:
```python
@hospital_bp.route("/appointments/today")
@require_role("doctor")        # ← only doctor tokens pass
def today_appointments(): ...
```

### 👤 Receptionist Workflow

1. **Registration** → `/receptionist/login` → provide Name, Email, Password, and **Doctor ID** (links receptionist to one doctor permanently)
2. **Patient Search** → Live debounced search across all `users` collection by name/email/mobile
3. **Book Appointment** → Select patient → default date = today, default time = now+30min → saved to `appointments` collection with `doctor_id`, `patient_id`, date, time
4. **Upload Blood Report** → Select patient → upload PDF/image → **runs through the full AI pipeline** (same as patient self-upload) → saves to `reports` collection under the patient's user ID → automatically appears in patient's "My Reports" dashboard

### 🩺 Doctor Workflow

1. **Login** → `/doctor/login` → JWT with `role: "doctor"` stored in `localStorage`
2. **Today's Appointments** → Fetches appointments filtered by `doctor_id` AND today's date → displayed as a table (Patient Name, Mobile, Email, Time, Status)
3. **Write Prescription** → Click ✍️ Prescribe → modal opens:
   - Add multiple medicines (Name, Dosage, Frequency dropdown, Duration, Instructions)
   - Add doctor's notes
   - Save → stored in `prescriptions` collection
   - Button changes to ✅ Prescribed (disabled, prevents duplicate)
4. **All Patients** → View every unique patient who has ever had an appointment with this doctor → click "📋 View Prescriptions" to see full prescription history per patient

### 👤 Patient Sees Hospital Data

In the Patient Dashboard, two new sections appear:
- **My Reports** tab — blood reports uploaded by receptionist show here with full AI analysis (same as self-uploaded)
- **Prescriptions** tab — all prescriptions written by doctor displayed as cards (Doctor name, date, each medicine with dosage/frequency/duration)

---

## 🛠 Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18 + Vite, Framer Motion, Recharts, React Router v6, Axios |
| **Backend** | Python Flask, PyJWT, bcrypt, Flask-CORS, Werkzeug |
| **Database** | MongoDB Atlas (PyMongo) — 8 collections |
| **NER / Entity** | `dmis-lab/biobert-base-cased-v1.1` (HuggingFace Transformers) |
| **Summarization** | `facebook/bart-large-cnn` — 406M params seq2seq |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` — 384-dim vectors |
| **Vector Search** | FAISS `IndexFlatIP` (cosine similarity, top-K=5) |
| **LLM Chat** | Groq API → `llama3-8b-8192` (500+ tok/s on Groq LPU) |
| **OCR** | pdfplumber (PDF), pytesseract + Tesseract (images) |
| **Auth** | JWT (HS256) with role-based access control (`user / doctor / receptionist`) |
| **Design** | Dark Navy glassmorphism + Cyan/Purple gradients, Framer Motion animations |

---

## 📄 Pages & Features

### Patient-facing Pages

#### 1. 🏠 Landing Page (`/`)
- Hero with animated gradient + stats (10K+ reports, 98% accuracy)
- Features grid (BERT+BART Analysis, RAG, Health Charts, Chatbot, Security, Multi-format)
- 4-step process (Upload → Extract → Retrieve → Insights)
- **🏥 Hospital Portal section** — 3 login cards (Patient / Doctor / Receptionist) with Login + Register buttons
- **"⚡ Create Demo Accounts"** button — auto-seeds demo doctor + receptionist to MongoDB
- **🏥 Portals** navbar dropdown for quick access from any page

#### 2. ⚡ System Animation (`/system`) — _Demo/Jury Presentation_
- Auto-playing 7-step pipeline animation with moving data packets
- Steps: PDF Input → NLP Preprocessing → BioBERT NER → FAISS RAG → BART Summary → Groq LLM → Dashboard
- Each step has technical deep-dive toggle, model name, architecture badges
- Full tech stack summary grid at the bottom

#### 3. 📝 Register (`/register`) / 🔐 Login (`/login`)
- Full medical profile on registration (Name, Email, Mobile, Age, Height, Weight, Blood Group, BP, Gender)
- Login accepts email OR mobile number
- JWT stored in `localStorage`, set as Axios global header

#### 4. 📊 Patient Dashboard (`/dashboard`) — 8 tabs

| Tab | Description |
|-----|-------------|
| 🏠 **Overview** | Welcome banner, stats (reports count, monthly), latest report summary card |
| 📤 **Upload Report** | Drag-and-drop zone (PDF/JPG/PNG, 16MB), real-time progress, AI summary shown immediately |
| 📋 **My Reports** | Card grid of all reports. Includes reports uploaded by receptionist |
| 📊 **Health Metrics** | Metric cards (NORMAL/HIGH/LOW), Recharts BarChart + LineChart trends |
| 💊 **Medicine Reminders** | Add/manage daily medicine reminder notifications |
| 🩺 **Prescriptions** | Cards showing all doctor prescriptions: medicine name, dosage, frequency, duration |
| 🤖 **AI Chatbot** | Groq LLaMA 3 chat with RAG context + report context, quick suggestions |
| 👤 **My Profile** | Displays all registered medical profile fields |

---

### Hospital Portal Pages

#### 5. 🩺 Doctor Login + Dashboard (`/doctor/login`, `/doctor`)
**Login / Register** with Name, Specialization, Hospital, Email, Password → issues JWT with `role: "doctor"`

**Dashboard (2 tabs)**:
- **Today's Appointments** — table with Patient Name, Mobile, Email, Time, Status, ✍️ Prescribe button
  - Prescribe modal: add medicines (name, dosage, frequency dropdown, duration, notes)
  - Button becomes ✅ Prescribed after saving — prevents duplicate prescriptions
- **All Patients** — all unique patients ever seen, click to view full prescription history

**Sidebar** shows Doctor Name, Specialization, Hospital, and a **clickable Doctor ID** (copy-to-clipboard) to share with receptionist during setup.

#### 6. 🏥 Receptionist Login + Dashboard (`/receptionist/login`, `/receptionist`)
**Register** with Name, Email, Password, **Doctor ID** (links to a specific doctor)  
**Login** issues JWT with `role: "receptionist"`

**Dashboard (3 tabs)**:
- **Book Appointment** — live patient search (debounced), select patient, date=today, time=now+30min → book
- **Upload Report** — select patient from search, upload blood report → AI analysis runs → appears in patient's My Reports
- **All Appointments** — list of all appointments booked by this receptionist's linked doctor

---

## 📁 Datasets

Located in `datasets/` folder:

| File | Description | Records |
|------|-------------|---------|
| `medical_knowledge_base.jsonl` | Medical QA pairs for FAISS RAG retrieval | 25 QA pairs (CBC, diabetes, thyroid, liver, kidney, cardiology) |
| `blood_report_reference.csv` | Lab test reference ranges with clinical interpretations | 34 parameters (hemoglobin, glucose, TSH, creatinine, etc.) |

**Data Sources**: MedQuAD dataset (adapted), clinical reference ranges from standard medical guidelines.

---

## 📁 Project Structure

```
RAGnosis/
├── frontend/                    # React Vite application
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx      # Homepage + Hospital Portal cards
│   │   │   ├── SystemAnimation.jsx  # AI Pipeline demo animation
│   │   │   ├── RegisterPage.jsx     # Patient registration
│   │   │   ├── LoginPage.jsx        # Patient login
│   │   │   ├── Dashboard.jsx        # Patient dashboard (8 tabs incl. Prescriptions)
│   │   │   ├── DoctorLogin.jsx      # Doctor register/login
│   │   │   ├── DoctorDashboard.jsx  # Doctor dashboard (appointments + prescribe)
│   │   │   ├── ReceptionistLogin.jsx      # Receptionist register/login
│   │   │   └── ReceptionistDashboard.jsx  # Receptionist dashboard
│   │   ├── components/
│   │   │   └── Navbar.jsx       # Navbar with 🏥 Portals dropdown
│   │   ├── context/
│   │   │   └── AuthContext.jsx  # JWT auth state management
│   │   └── App.jsx              # Router with public + hospital routes
│
├── backend/                     # Flask API server
│   ├── app.py                   # App factory + blueprint registration
│   ├── config.py                # Configuration + env vars
│   ├── database.py              # MongoDB singleton
│   ├── routes/
│   │   ├── auth.py             # /api/auth/* — patient registration/login
│   │   ├── reports.py          # /api/reports/* — upload, list, retrieve
│   │   ├── chatbot.py          # /api/chat/* — Groq LLM conversation
│   │   ├── reminders.py        # /api/reminders/* — medicine reminders
│   │   └── hospital.py         # /api/hospital/* — doctor, receptionist, appointments, prescriptions
│   ├── models/
│   │   ├── user_model.py       # User CRUD
│   │   └── report_model.py     # Report CRUD
│   ├── services/
│   │   ├── text_extractor.py   # PDF + OCR + metric regex extraction
│   │   ├── bert_summarizer.py  # BioBERT NER + BART summarization + metric status
│   │   ├── rag_engine.py       # Sentence-BERT embedding + FAISS retrieval
│   │   └── groq_service.py     # Groq LLM chat with RAG context injection
│   └── utils/
│       └── jwt_helper.py       # JWT encode/decode + require_auth + require_role decorators
│
├── datasets/
│   ├── medical_knowledge_base.jsonl  # 25 medical QA pairs for RAG
│   └── blood_report_reference.csv    # 34 lab parameters with normal ranges
│
├── models/
│   ├── build_rag_index.py       # Build FAISS index (run ONCE)
│   └── faiss_index/             # Generated index files (vectors + metadata)
│
└── notebooks/
    └── train_bert_medical.ipynb # BERT fine-tuning notebook (Google Colab ready)
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB Atlas account
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Tesseract OCR (for image reports) — [Download](https://github.com/UB-Mannheim/tesseract/wiki)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env from template
copy .env.template .env
# Edit .env and set GROQ_API_KEY, MONGO_URI, JWT_SECRET

# Build FAISS RAG index (run ONCE before first start)
cd ..
python models/build_rag_index.py
cd backend

# Start Flask server
python app.py
```

Server: `http://localhost:5000`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App: `http://localhost:5173`

### 3. Environment Variables (backend/.env)

```env
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/ragnosis
JWT_SECRET=your-super-secret-key
GROQ_API_KEY=gsk_your_groq_api_key_here
JWT_EXPIRY_HOURS=24
UPLOAD_FOLDER=uploads
```

> ⚠️ **Important**: Flask runs with `use_reloader=False` (to prevent ML models loading twice). You must **manually restart** the backend after code changes.

---

## 🔌 API Endpoints

### Patient Auth & Reports
| Method | Route | Description | Auth |
|--------|-------|-------------|------|
| GET | `/api/health` | Health check | ❌ |
| POST | `/api/auth/register` | Patient registration | ❌ |
| POST | `/api/auth/login` | Patient login (email/mobile) | ❌ |
| GET | `/api/auth/me` | Get current patient profile | ✅ user |
| POST | `/api/reports/upload` | Upload & analyze report (AI pipeline) | ✅ user |
| GET | `/api/reports/` | List all patient's reports | ✅ user |
| GET | `/api/reports/<id>` | Get single report with full analysis | ✅ user |
| POST | `/api/chat/` | Chatbot message with RAG + report context | ✅ user |
| GET | `/api/chat/suggestions` | Default chat questions | ✅ user |

### Hospital Portal
| Method | Route | Description | Auth |
|--------|-------|-------------|------|
| POST | `/api/hospital/doctor/register` | Register doctor | ❌ |
| POST | `/api/hospital/doctor/login` | Doctor login | ❌ |
| GET | `/api/hospital/doctor/me` | Doctor profile | ✅ doctor |
| POST | `/api/hospital/receptionist/register` | Register receptionist | ❌ |
| POST | `/api/hospital/receptionist/login` | Receptionist login | ❌ |
| GET | `/api/hospital/patients/search?q=` | Search patients by name/email/mobile | ✅ receptionist |
| POST | `/api/hospital/appointments` | Book appointment | ✅ receptionist |
| GET | `/api/hospital/appointments/today` | Today's appointments for doctor | ✅ doctor |
| GET | `/api/hospital/appointments/all-patients` | All patients ever seen | ✅ doctor |
| POST | `/api/hospital/prescriptions` | Write prescription | ✅ doctor |
| GET | `/api/hospital/prescriptions/me` | Patient's own prescriptions | ✅ user |
| GET | `/api/hospital/prescriptions/patient/<id>` | Patient prescriptions (for doctor) | ✅ doctor |
| POST | `/api/hospital/reports/upload` | Upload report for a patient (AI pipeline) | ✅ receptionist |
| POST | `/api/hospital/demo/seed` | Seed demo doctor + receptionist accounts | ❌ |

---

## 🔑 Demo Credentials

Click the **"⚡ Create Demo Accounts"** button on the landing page homepage first, then:

| Portal | URL | Email | Password |
|--------|-----|-------|----------|
| 👤 Patient | `/register` | Create your own | — |
| 🩺 Doctor | `/doctor/login` | `demo.doctor@ragnosis.com` | `demo1234` |
| 🏥 Receptionist | `/receptionist/login` | `demo.receptionist@ragnosis.com` | `demo1234` |

The demo receptionist is pre-linked to the demo doctor — no manual setup needed.

### Full Demo Flow
1. Go to `/` → Click "⚡ Create Demo Accounts"
2. Register as a patient at `/register`
3. Login as Receptionist → "Book Appointment" → search your patient → book
4. Login as Receptionist → "Upload Report" → upload a blood test PDF for the patient
5. Login as Doctor → see the appointment today → click ✍️ Prescribe → submit
6. Login as Patient → see the report in "My Reports" + prescription in "Prescriptions" tab

---

## 🏫 Credits

**RAGnosis** — PICT InC 2025 Project  
Pune Institute of Computer Technology, Pune - 411043

Built with ❤️ using:
- [HuggingFace Transformers](https://huggingface.co) — BERT, BART models
- [FAISS](https://github.com/facebookresearch/faiss) by Meta AI — vector similarity search
- [Groq](https://groq.com) — ultra-fast LLaMA 3 inference at 500+ tok/s
- [React](https://react.dev) + [Vite](https://vitejs.dev) — frontend framework
- [MongoDB Atlas](https://www.mongodb.com/atlas) — cloud database
- [Framer Motion](https://www.framer.com/motion/) — animations
