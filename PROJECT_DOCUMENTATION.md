# 🩺 RAGnosis: Complete Project Documentation

**An AI-Powered Medical Report Analysis System**  
**Built with React, React Native, Flask, MongoDB, and Advanced NLP Models**

---

## 📑 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Overview](#architecture-overview)
3. [System Architecture Diagram](#system-architecture-diagram)
4. [Technology Stack](#technology-stack)
5. [Database Schema](#database-schema)
6. [User Workflows](#user-workflows)
7. [API Endpoints](#api-endpoints)
8. [How the System Works](#how-the-system-works)
9. [Setup & Installation](#setup--installation)
10. [Main Features Explained](#main-features-explained)
11. [Troubleshooting Guide](#troubleshooting-guide)

---

## 🌍 Project Overview

### What is RAGnosis?

RAGnosis is a comprehensive medical report analysis platform that leverages artificial intelligence and the Retrieval-Augmented Generation (RAG) paradigm to help healthcare providers, patients, and medical professionals:

- **Upload** medical reports (PDF, JPG, PNG) from labs or hospitals
- **Extract** text using OCR (Tesseract) from images and PDFs
- **Analyze** medical metrics using BioBERT (BERT model fine-tuned for biomedical text)
- **Summarize** reports using BART (denoising autoencoder for abstractive summarization)
- **Query** using RAG (Retrieval-Augmented Generation) powered by FAISS vector indexing
- **Chat** with an AI-powered Groq LLaMA 3 chatbot about their medical data
- **Track** medicine reminders with daily notifications
- **Monitor** health metrics over time with interactive charts and trend analysis

### Key Objectives

✅ **Accessibility**: Make medical report interpretation accessible to non-medical professionals  
✅ **Accuracy**: Provide data-driven, AI-generated health insights  
✅ **Privacy**: Secure, encrypted storage of sensitive medical data  
✅ **User Experience**: Intuitive, accessible interface across web and mobile  
✅ **Real-time Sync**: Seamless data synchronization between web and mobile apps  

---

## 🏗️ Architecture Overview

RAGnosis follows a **modern 3-tier architecture**:

### Tier 1: Frontend Layer
- **Web**: React 18 + Vite + React Router (Dashboard, Report Analysis, Chatbot, Medicine Reminders)
- **Mobile**: React Native + Expo SDK 54+ (Android & iOS support)
- Both platforms share the same backend API

### Tier 2: Backend Layer
- **Framework**: Flask (Python)
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: MongoDB Atlas (cloud NoSQL database)
- **Core Services**:
  - Text Extraction (OCR via Tesseract, PDF parsing via pdfplumber)
  - Medical Metric Extraction (Regex-based, human-validated rules)
  - BERT Summarization (facebook/bart-large-cnn model)
  - RAG Engine (FAISS vector indexing)
  - Groq AI Chatbot (LLaMA 3 model)
  - Reminder Management
  - **Doctor Suggestion Service** (report-type → specialist mapping + MongoDB queries)
  - **Critical Detection Engine** (threshold-based flagging for abnormal values)

### Tier 3: AI/ML Layer
- **Text Extraction**: Tesseract OCR + pdfplumber
- **Medical NLP**: dmis-lab/biobert-base-cased-v1.1
- **Summarization**: facebook/bart-large-cnn
- **Vector Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Search**: FAISS (Facebook AI Similarity Search)
- **Chatbot LLM**: Groq API → LLaMA 3 8B model

---

## 📊 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER DEVICES                                   │
├─────────────────────┬───────────────────────────────────────┬───────────┤
│   WEB BROWSER       │      MOBILE DEVICE (Android/iOS)      │  Desktop  │
│   (React + Vite)    │    (React Native + Expo SDK 54)       │  client   │
│                     │                                       │           │
│ • Dashboard         │ • Dashboard                           │ • Reports │
│ • Upload Report     │ • Upload Report                       │ • Charts  │
│ • View Reports      │ • View Reports                        │           │
│ • Health Metrics    │ • Health Metrics                      │           │
│ • Medicine          │ • Medicine Reminders (with push       │           │
│   Reminders         │   notifications)                      │           │
│ • AI Chatbot        │ • AI Chatbot                         │           │
│ • User Profile      │ • User Profile                        │           │
└─────────────────────┴───────────────────────────────────────┴───────────┘
                              │
                    HTTP/HTTPS over REST API
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      FLASK BACKEND SERVER                              │
│                    (Python 3.10+ on port 5000)                         │
│                                                                         │
│  API Endpoints:                            Core Services:              │
│  ├── /api/auth/* (login, register, profile) │ • JWT Auth              │
│  ├── /api/reports/* (upload, list, detail)  │ • File Upload           │
│  ├── /api/reminders/* (CRUD operations)     │ • Notification Sched    │
│  └── /api/chat/* (chatbot interactions)     │ • AI Orchestration      │
│                                              │                         │
│  Microservices Layer:                                                   │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ Text Extraction              │ Medical Analysis               │    │
│  │ ├─ Tesseract OCR             │ ├─ Metric Extraction (Regex)  │    │
│  │ ├─ PDF text extraction       │ ├─ Report Type Detection      │    │
│  │ └─ Image preprocessing       │ └─ Validation & Normalization │    │
│  ├────────────────────────────────────────────────────────────────┤    │
│  │ AI Models Layer              │ RAG Engine                     │    │
│  │ ├─ BART (Summarization)      │ ├─ FAISS Vector Index         │    │
│  │ ├─ BioBERT (Understanding)   │ ├─ Sentence Transformers      │    │
│  │ └─ Named Entity Recognition  │ └─ Knowledge Base Search       │    │
│  ├────────────────────────────────────────────────────────────────┤    │
│  │ Groq Chatbot Service                                           │    │
│  │ ├─ LLaMA 3 8B Model (via Groq API)                             │    │
│  │ ├─ Context Injection (User Reports)                            │    │
│  │ └─ Streaming Responses                                         │    │
│  └────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                    ▼─────────┴─────────▼
┌──────────────────────────────┐    ┌──────────────────────────────┐
│   MONGODB ATLAS              │    │  EXTERNAL AI SERVICES         │
│   Database Store             │    │                              │
│                              │    │  • Groq API (LLaMA 3)       │
│ Collections:                 │    │  • HuggingFace Models       │
│ ├── users                    │    │  • TensorFlow Models        │
│ ├── reports                  │    │                              │
│ ├── reminders                │    │  Model Storage:              │
│ ├── suggested_doctors        │    │  ├── FAISS Index (/models)  │
│ └── (future) notifications   │    │  ├── Medical KB (JSONL)     │
│                              │    │                              │
└──────────────────────────────┘    └──────────────────────────────┘

┌──────────────────────────────┐
│  FILE STORAGE                │
│                              │
│ Upload Folder: /backend/     │
│   uploads/                   │
│  ├── [uuid].pdf              │
│  └── [uuid].jpg              │
└──────────────────────────────┘
```

---

## 💻 Technology Stack

### Frontend (Web)
- **React 18.2** – UI component library
- **Vite** – Lightning-fast build tool
- **React Router v6** – Client-side navigation
- **Axios** – HTTP client for API calls
- **Framer Motion** – Smooth animations
- **Recharts** – Interactive charts & visualizations
- **React Hot Toast** – Toast notifications
- **TailwindCSS / Custom CSS** – Styling (dark navy + cyan theme)

### Mobile (Android & iOS)
- **React Native 0.83** – Cross-platform mobile framework
- **Expo SDK 54** – Managed React Native development
- **React Navigation 7** – Native navigation
- **Expo Notifications** – Push notifications for reminders
- **Expo Document Picker** – File selection
- **Expo Image Picker** – Camera & gallery access
- **Expo Secure Store** – Secure token storage
- **Axios** – API communication

### Backend
- **Python 3.10+** – Programming language
- **Flask** – Web framework
- **PyMongo 4.7** – MongoDB driver
- **PyJWT** – JWT token generation & validation
- **bcrypt** – Password hashing
- **Flask-CORS** – Cross-origin request handling

### AI/ML & Text Processing
- **Tesseract OCR 5.x** – Optical character recognition
- **pdfplumber** – PDF text extraction
- **Transformers (HuggingFace 4.41)** – Pre-trained NLP models
- **torch/PyTorch 2.3** – Deep learning framework
- **sentence-transformers 3.0** – Text embeddings
- **FAISS 1.8** – Vector similarity search
- **Groq API** – LLaMA 3 8B hosted inference
- **sklearn** – Machine learning utilities

### Database
- **MongoDB Atlas** – Cloud NoSQL database
  - Replica set (High availability)
  - Automatic backups
  - Security groups & encryption

### Deployment & Infrastructure
- **Gunicorn** – WSGI server for Flask
- **Docker** (optional) – Containerization
- **GitHub** – Version control

---

## 📦 Database Schema

### Collection: `users`
Stores user account information and health profile.

```json
{
  "_id": ObjectId,
  "name": String,
  "email": String (unique),
  "mobile": String (unique, 10-digit),
  "password": String (bcrypt hashed),
  "age": Integer,
  "height_inches": Float,
  "weight_kg": Float (optional),
  "blood_pressure": String (optional, e.g., "120/80"),
  "blood_group": String (optional, e.g., "O+"),
  "gender": String (M/F/Other),
  "created_at": DateTime,
  "updated_at": DateTime
}
```

### Collection: `reports`
Stores uploaded medical reports and extracted data.

```json
{
  "_id": ObjectId,
  "user_id": ObjectId (ref: users),
  "original_name": String (original filename),
  "file_path": String (server storage path),
  "file_type": String (pdf/jpg/png),
  "raw_text": String (extracted OCR text),
  "report_type": String (CBC/Lipid/LFT/Diabetes/Thyroid/Urine/Vitamin/Bone/Skin/Cardiac/Pulmonary/etc.),
  "summary": String (AI-generated summary),
  "metrics": {
    "hemoglobin": Float,
    "glucose": Float,
    "cholesterol": Float,
    "triglycerides": Float,
    ... (up to 30+ medical metrics)
  },
  "is_critical": Boolean (true if any metric exceeds critical thresholds),
  "suggested_doctors": [
    {
      "name": "Dr. Abhijeet Palshikar",
      "specialization": "Cardiologist",
      "hospital": "Sahyadri Hospital, Bibwewadi",
      "contact": "+91 8806252525",
      ...
    }
  ],
  "specialist_advice": String (e.g., "Your CBC report indicates you should consult a Hematologist..."),
  "uploaded_at": DateTime,
  "processed_at": DateTime,
  "status": String (processing/completed/failed)
}
```

### Collection: `suggested_doctors`
Stores verified specialist doctors for recommendation.
Seeded on application startup with 28 real doctors across 12 specializations near Katraj, Pune.

```json
{
  "_id": ObjectId,
  "name": "Dr. Chandrakant Lahane",
  "specialization": "Hematologist",
  "qualification": "MD, DM (Clinical Hematology)",
  "hospital": "Sahyadri Hospital, Bibwewadi",
  "location": "Bibwewadi",
  "city": "Pune",
  "contact": "+91 8806252525",
  "experience": "15+ years",
  "rating": 4.5,
  "consultation_fee": "₹800",
  "available_days": "Mon–Sat"
}
```

**Specializations covered**: Hematologist, Endocrinologist, Diabetologist, Cardiologist, Nephrologist, Hepatologist, Gastroenterologist, Radiologist, Urologist, Orthopedic Surgeon, Dermatologist, Pulmonologist, General Physician

### Collection: `reminders`
Stores medicine reminder schedules.

```json
{
  "_id": ObjectId,
  "user_id": ObjectId (ref: users),
  "medicine_name": String (e.g., "Metformin"),
  "dosage": String (e.g., "500mg, 2x daily"),
  "times": [
    {
      "hour": Integer (0-23),
      "minute": Integer (0-59),
      "label": String (e.g., "08:00 AM")
    }
  ],
  "frequency": String (daily/weekly/monthly),
  "notes": String (e.g., "Take with food"),
  "active": Boolean (true = notifications enabled),
  "created_at": DateTime,
  "updated_at": DateTime,
  "notification_ids": [String] (Expo notification IDs)
}
```

### Supporting Collections (Future)
```
notifications {
  _id, user_id, type, title, body, read, created_at
}

chat_history {
  _id, user_id, report_id, messages[...], created_at
}
```

---

## 👥 User Workflows

### Workflow 1: User Registration & Authentication

```
┌─────────────┐
│ New User    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 1. Opens RAGnosis App               │
│    (Web: ragnosis.local/register)   │
│    (Mobile: RegisterScreen)         │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 2. Fills Registration Form:         │
│    • Name, Email, Mobile            │
│    • Password (min 6 chars)         │
│    • Age, Height, Weight            │
│    • Blood Group, Blood Pressure    │
│    • Gender                         │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 3. POST /api/auth/register          │
│    → Backend validates input        │
│    → Hashes password with bcrypt    │
│    → Creates user document in DB    │
│    → Generates JWT token            │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 4. Response:                        │
│    {                                │
│      "token": "eyJhbG...",          │
│      "user": { id, name, email }    │
│    }                                │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 5. Token stored securely:           │
│    • Web: localStorage              │
│    • Mobile: Expo SecureStore       │
│    • Sent in Authorization header   │
│      for all subsequent requests    │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 6. Redirect to Dashboard            │
│    (Authenticated access granted)   │
└─────────────────────────────────────┘
```

### Workflow 2: Upload & Analyze Medical Report

```
┌──────────────────┐
│ User on Dashboard│
└────────┬─────────┘
         │
         ▼
┌────────────────────────────┐
│ 1. Click "Upload Report"   │
│    (Mobile: UploadScreen)  │
│    (Web: Upload Tab)       │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ 2. Select File Source:             │
│    • Choose from device files      │
│    • Or capture with camera        │
│    • Supported: PDF, JPG, PNG      │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ 3. POST /api/reports/upload        │
│    (multipart/form-data)           │
│                                    │
│    Backend Processing:             │
│    a) Save file to /uploads/       │
│    b) Extract text (Tesseract OCR) │
│    c) Validate medical content     │
│    d) Extract metrics (regex)      │
│    e) Detect report type (scoring) │
│    f) Summarize (BART model)       │
│    g) Check critical thresholds    │
│    h) Query suggested_doctors DB   │
│    i) Generate specialist advice   │
│    j) Store in MongoDB             │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ 4. Response (JSON):                │
│    {                               │
│      "_id": "...",                 │
│      "report_type": "Diabetes",    │
│      "summary": "...",             │
│      "metrics": { ... },           │
│      "is_critical": true/false,    │
│      "suggested_doctors": [...],   │
│      "specialist_advice": "..."    │
│    }                               │
└────────┬───────────────────────────┘
         │
         ▼
┌───────────────────────────────────────┐
│ 5. Display Results to User:           │
│    • AI-generated summary             │
│    • Extracted health metrics         │
│    • Visual status indicators         │
│      (✓ NORMAL, ↑ HIGH, ↓ LOW)       │
│    • Health recommendations           │
│    • If CRITICAL:                     │
│      - Red "CRITICAL CONDITION" alert │
│      - Specialist advice text         │
│      - Doctor suggestion table        │
│        (name, hospital, fee, contact) │
│      - Click-to-call buttons          │
│                                      │
│    Report now synced:                │
│    • Visible on web dashboard        │
│    • Visible on mobile dashboard     │
│    • Available for RAG chatbot       │
└───────────────────────────────────────┘
```

### Workflow 3: Chat with AI Chatbot

```
┌─────────────────────┐
│ User views reports  │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│ 1. Click "AI Chatbot" tab    │
│    (Web or Mobile app)       │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 2. See suggested questions:          │
│    • "What does my hemoglobin mean?" │
│    • "Is my blood sugar normal?"     │
│    • "Explain cholesterol results"   │
│    etc.                              │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 3. Type custom question or           │
│    select suggested question         │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 4. POST /api/chat/                   │
│    {                                 │
│      "message": "What's my glucose", │
│      "report_id": "...", (optional)  │
│      "history": [...]  (for context) │
│    }                                 │
│                                      │
│    Backend:                          │
│    a) Retrieve report context (if ID)│
│    b) Call Groq API (LLaMA 3)        │
│    c) Inject report text as context  │
│    d) Generate response              │
│    e) Maintain conversation memory   │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 5. Streaming Response:               │
│    "Your glucose level is 95 mg/dL. │
│     This is within the normal range  │
│     of 70–100 mg/dL. Keep up good   │
│     dietary habits..."               │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 6. User can ask follow-up questions  │
│    (Chat history maintained)         │
└──────────────────────────────────────┘
```

### Workflow 4: Create & Manage Medicine Reminders

```
┌──────────────────────────┐
│ User on Dashboard/Mobile │
└──────────┬───────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ 1. Click "Medicine Reminders"   │
│    (Web: New tab)               │
│    (Mobile: Reminders tab)      │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 2. Click "+ Add Medicine"            │
│    Opens Modal/Bottom Sheet          │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 3. Fill Medicine Details:            │
│    • Medicine Name (e.g., Metformin) │
│    • Dosage (e.g., 500mg 2x daily)   │
│    • Reminder Time(s) - can be       │
│      multiple times per day          │
│    • Notes (take with food, etc.)    │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 4. POST /api/reminders/              │
│    {                                 │
│      "medicine_name": "Metformin",   │
│      "dosage": "500mg",              │
│      "times": [                      │
│        { "hour": 8, "minute": 0 },   │
│        { "hour": 20, "minute": 0 }   │
│      ],                              │
│      "frequency": "daily"            │
│    }                                 │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 5. Backend:                          │
│    a) Validate time format           │
│    b) Store reminder in MongoDB      │
│    c) Return reminder_id             │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 6. Mobile App:                       │
│    a) Receive reminder_id            │
│    b) Schedule OS notifications      │
│    c) Trigger at specified times     │
│                                      │
│    Desktop/Web:                      │
│    Reminder appears in list,         │
│    user can toggle/delete it         │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ 7. At Scheduled Time (Mobile):       │
│    📱 Notification appears:          │
│    "💊 Time to take Metformin        │
│     500mg · 08:00 AM"                │
│                                      │
│    User can:                         │
│    a) Tap to view medicine details   │
│    b) Dismiss notification           │
│    c) Mark as taken                  │
└──────────────────────────────────────┘
```

---

## 🔌 API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/register` | ❌ | Create new user account |
| POST | `/login` | ❌ | Login via email or mobile |
| GET | `/me` | ✅ | Get current user profile |

### Reports (`/api/reports`)

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/upload` | ✅ | Upload medical report (multipart/form-data) |
| GET | `/` | ✅ | Get all user's reports |
| GET | `/<report_id>` | ✅ | Get specific report details |
| PUT | `/<report_id>` | ✅ | Update report metadata |
| DELETE | `/<report_id>` | ✅ | Delete a report |

### Medicine Reminders (`/api/reminders`)

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/` | ✅ | Get all user's medicine reminders |
| POST | `/` | ✅ | Create new medicine reminder |
| PUT | `/<reminder_id>` | ✅ | Update reminder (toggle active, change time) |
| DELETE | `/<reminder_id>` | ✅ | Delete a reminder |

### Chatbot (`/api/chat`)

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/` | ✅ | Send message to AI chatbot |
| GET | `/suggestions` | ✅ | Get suggested questions |

### Doctor Directory (`/api/doctors`)

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/` | ❌ | List all doctors (filter by `?city=Pune&specialization=Cardiologist`) |
| GET | `/<id>` | ❌ | Get single doctor by ID |
| POST | `/` | ❌ | Add a new doctor (admin use) |
| DELETE | `/<id>` | ❌ | Remove a doctor |

### Health Check (`/api`)

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/health` | ❌ | Server health status |

---

## 🧠 How the System Works: Detailed Explanation

### 1. Document Upload & OCR Processing

**User Action**: Uploads a PDF or image of medical report

**Backend Process**:
```
File Received
    ↓
File Validation (type, size ≤ 16MB)
    ↓
Save to /uploads/ folder with UUID
    ↓
┌─ If PDF: Use pdfplumber to extract text
├─ If JPG/PNG: Use Tesseract OCR to recognize text
└─ Combine both for maximum accuracy
    ↓
Text Preprocessing (cleanup, formatting)
    ↓
Length validation (must be ≥ 20 characters)
    ↓
Medical content validation (must contain medical keywords)
    ↓
Return extracted text to next stage
```

### 2. Medical Metrics Extraction

Uses **regex patterns** to find specific medical values from extracted text.

**Examples**:
- `hemoglobin: [0-9,]+\.?[0-9]*` → Finds "Hemoglobin: 13.5 g/dL"
- `glucose[:\s]+([0-9]+)` → Finds "Glucose: 95 mg/dL"
- `WBC[:\s]+([0-9,]+)` → Finds "WBC Count: 7.2 k/µL"

**Process**:
```
Raw Text
    ↓
Apply 30+ medical metric regex patterns
    ↓
Extract matched values
    ↓
Unit Normalization (convert lakhs to k/µL, etc.)
    ↓
Validation against normal range
    ↓
Calculate status (NORMAL/LOW/HIGH)
    ↓
Store in report.metrics object
```

### 3. Report Summarization (BART Model)

Generates a **natural language summary** of the medical report.

**Architecture**:
```
Extracted Medical Text
    ↓
BART Model Input
├─ Model: facebook/bart-large-cnn (139M parameters)
├─ Token limit: 1024 tokens max input
└─ Max summary length: 150 tokens
    ↓
Attention Layers (learn importance)
    ↓
Decoder (generates summary)
    ↓
Example Output:
"Your CBC report shows:
 • Hemoglobin: 13.5 (normal)
 • WBC: 7.2 (normal)
 • Platelets: 280 (low)
 Consider iron supplementation for platelets."
    ↓
Store summary in report object
```

### 4. RAG (Retrieval-Augmented Generation) Engine

Enables **intelligent Q&A** about the medical knowledge base.

**Components**:

**A. Knowledge Base Setup** (Offline, done once):
```
Medical Knowledge Base (JSONL file)
    ↓
Load ~5,000 medical fact snippets
    ↓
For each fact:
  a) Embed using SentenceTransformer (384-dimensional vectors)
  b) Store vector in FAISS index (GPU-optimized)
  c) Keep text reference for retrieval
    ↓
Result: FAISS index + embeddings saved to /models/
```

**B. Query Processing** (Runtime):
```
User Question: "What does low hemoglobin mean?"
    ↓
Embed question using same SentenceTransformer
    ↓
Search FAISS index (top-5 most similar facts)
    ↓
Retrieved Contexts:
  1. "Hemoglobin carries oxygen..."
  2. "Low hemoglobin causes fatigue..."
  3. "Iron-rich foods boost hemoglobin..."
    ↓
Combine contexts + user question + report data
    ↓
Send to Groq LLaMA 3 for final answer
    ↓
Example Response:
"Low hemoglobin (anemia) means your red blood cells 
 are below normal. This causes fatigue and shortness 
 of breath. Eat spinach, lentils, red meat, and take 
 iron supplements with vitamin C."
```

### 5. AI Chatbot (Groq LLaMA 3)

Real-time **conversational AI** powered by Groq's hosted inference.

**Process**:
```
User Message
    ↓
Report Context Injection (if report selected):
├─ Report raw text
├─ Extracted metrics
└─ Summary
    ↓
System Prompt Construction:
"You are a medical AI assistant. Use the following 
 report context and knowledge base to answer 
 questions. Be informative but not diagnostic."
    ↓
LLaMA 3 Stream Response via Groq API
├─ Token streaming (real-time)
├─ Temperature: 0.7 (balanced creativity)
└─ Max tokens: 500
    ↓
Rendered in chat interface
    ↓
Conversation history maintained for follow-ups
```

### 6. Medicine Reminder Scheduling

**Web Flow**:
```
User adds medicine in web dashboard
    ↓
Store in MongoDB reminders collection
    ↓
Browser maintains display (can toggle, delete)
    ↓
No notifications on web (browser limitations)
```

**Mobile Flow**:
```
User adds medicine in mobile app
    ↓
POST to /api/reminders/
    ↓
Backend stores in MongoDB
    ↓
Mobile app receives reminder_id
    ↓
Schedule Expo.Notifications for each time:
  a) Daily trigger at HH:MM
  b) Notification body: "Time to take [medicine]"
  c) Store notification ID in reminder object
    ↓
At scheduled time:
  a) OS fires notification
  b) User taps notification → opens medicine details
  c) User can mark as taken (future feature)
```

### 7. Real-time Synchronization

**Report Upload Sync**:
```
Mobile App uploads report
    ↓
Server processes & stores in MongoDB
    ↓
Web app fetches latest reports on page load/tab switch
    ↓
Both show same data
✓ NO real-time WebSocket (polling-based currently)
```

**Medicine Reminder Sync**:
```
Web: Add reminder → Stored in DB
    ↓
Mobile: Fetch reminders on app launch
    ↓
Both show same list
✓ Desktop reminders display-only (no notifications)
✓ Mobile reminders trigger native OS notifications
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 16+
- MongoDB Atlas account
- Groq API key
- Tesseract OCR installed on server
- Git

### Backend Setup

```bash
# 1. Clone repository
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env with:
# MONGODB_URI=mongodb+srv://...
# GROQ_API_KEY=gsk_...
# JWT_SECRET=your-secret-key

# 5. Install Tesseract OCR
# On Ubuntu: sudo apt-get install tesseract-ocr
# On macOS: brew install tesseract
# On Windows: Download installer from GitHub

# 6. Build RAG index (first time only)
cd ../models
python build_rag_index.py

# 7. Start backend server
cd ../backend
python app.py
# Server runs on http://localhost:5000
```

### Frontend (Web) Setup

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Create .env.local
echo "VITE_API_BASE_URL=http://localhost:5000" > .env.local

# 3. Start dev server
npm run dev
# Opens on http://localhost:5173
```

### Mobile (Android) Setup

```bash
cd android

# 1. Install dependencies
npm install

# 2. Configure backend IP (for non-emulator testing)
# Edit src/api/client.js:
# export const BASE_URL = 'http://10.0.2.2:5000' (for emulator)
# or your LAN IP for physical device: 'http://192.168.1.x:5000'

# 3. Start Expo dev server
npm start

# 4. Press 'a' for Android (emulator or physical)
# Or scan QR code with Expo Go app on physical device
```

---

## 🎯 Main Features Explained

### Feature 1: Smart Report Upload & Analysis

**What it does**:
- Accepts PDF, JPG, PNG files up to 16MB
- Extracts text using OCR (Tesseract) or PDF parsing
- Validates it's a medical document
- Extracts 30+ health metrics automatically
- Generates AI summary in plain English
- Shows status for each metric (Normal/High/Low)

**Example**:
```
Input: blood_report.pdf (scanned lab report)
    ↓
Output: 
{
  "report_type": "CBC",
  "summary": "Your Complete Blood Count shows all values 
             within normal range. Your hemoglobin is good 
             and platelet count is healthy.",
  "metrics": {
    "hemoglobin": 13.5,      ✓ NORMAL
    "wbc": 7.2,              ✓ NORMAL
    "platelets": 280,        ✓ NORMAL
    "rbc": 4.8               ✓ NORMAL
  }
}
```

### Feature 2: Health Metrics Dashboard

**What it does**:
- Shows all extracted metrics from all reports
- Visual gauges showing where each value falls
- Color-coded status (red=low, green=normal, orange=high)
- Trends over time (line charts)
- Actionable health recommendations

**Example**:
```
Hemoglobin: 13.5 g/dL
├─ Status: ✓ NORMAL (12-17 is normal range)
├─ Previous: 13.2, 13.1 (stable trend)
└─ Recommendations:
   • Continue balanced diet with iron sources
   • Good levels — maintain current habits
```

### Feature 3: RAG-Powered AI Chatbot

**What it does**:
- Answer medical questions using AI
- Provides context from user's reports
- Retrieves relevant medical knowledge
- Generates detailed, accurate explanations
- Maintains conversation history

**Example Conversation**:
```
User: "Why is my platelet count low?"
    ↓
AI: "Your platelets are 145 k/µL (normal: 150-400).
    While slightly low, it's borderline. Low platelets 
    (thrombocytopenia) can cause easy bruising. 
    
    Causes include:
    • Certain medications (aspirin)
    • Vitamin deficiency
    • Immune issues
    
    I recommend:
    1. Avoid NSAIDs
    2. Eat foods rich in Vitamin B12 & folate
    3. Follow up with your doctor
    
    Do you have any other symptoms?"
```

### Feature 4: Medicine Reminder System

**What it does**:
- Create reminders for up to multiple medicines
- Set different times for each medicine
- Receive daily notifications (mobile)
- Track dosage information
- Add notes (e.g., "take with food")

**Example**:
```
Medicine: Metformin
Dosage: 500mg
Times: 08:00 AM, 08:00 PM
Status: ✓ Active (reminders enabled)
Notes: Take with breakfast and dinner

[At 8:00 AM]
📱 Notification: "💊 Time to take Metformin 500mg"
```

### Feature 5: Critical Report Detection & Doctor Suggestions

**What it does**:
- Detects critical/abnormal values in uploaded reports using medical threshold checks
- Uses **scoring-based report type detection** (13 categories) instead of first-match for accuracy
- Maps each report type to relevant specialist categories
- Queries the `suggested_doctors` MongoDB collection for matching doctors near the user’s location
- Displays specialist advice text (e.g., "Your CBC report indicates you should consult a Hematologist - MBBS, MD/DM")
- Shows a table of real doctors with name, qualification, hospital, experience, consultation fee, and click-to-call contact

**When It Triggers**:
- Doctor suggestions appear **only when the report is flagged as critical**
- Non-critical reports show analysis and metrics without the specialist table

**Report Types Supported (13)**:
- Blood / CBC Report
- Diabetes / Glucose Report
- Lipid Panel Report
- Kidney Function Report
- Liver Function Report
- Thyroid Report
- Radiology Report
- Urine Analysis Report
- Vitamin / Nutrition Report
- Bone / Orthopedic Report
- Skin / Dermatology Report
- Cardiac / ECG Report
- Pulmonary Report

**Specialist Mapping Example**:
```
Diabetes / Glucose Report → Endocrinologist + Diabetologist + General Physician
Lipid Panel Report → Cardiologist + General Physician
Kidney Function Report → Nephrologist + General Physician
Liver Function Report → Hepatologist + Gastroenterologist + General Physician
```

**Doctor Database**:
- 28 doctors across 12 specializations stored in MongoDB `suggested_doctors` collection
- Auto-seeded on first application startup (`doctor_model.seed_doctors()`)
- Real hospital names from Pune: Sahyadri, Bharati, Ruby Hall Clinic, KEM, Jehangir, Deenanath Mangeshkar
- Includes: name, qualification, hospital, location, city, contact number, experience, rating, consultation fee

**Example Output**:
```
🚨 CRITICAL CONDITION DETECTED

💡 Your CBC report indicates you should consult a Hematologist
   (MBBS, MD/DM in Hematology) for blood-related conditions.

🩺 Recommended Specialists for Consultation [URGENT]
┌─────────────────────────┬────────────────┬────────────────────┬────────────┬──────┬─────────────────┐
│ Doctor                  │ Specialization │ Hospital             │ Experience │ Fee  │ Contact         │
├─────────────────────────┼────────────────┼────────────────────┼────────────┼──────┼─────────────────┤
│ Dr. Chandrakant Lahane  │ Hematologist   │ Sahyadri, Bibwewadi  │ 15+ years  │ ₹800 │ 📞 +91 880625 │
│ Dr. Vinod Borse         │ Gen. Physician │ Katraj PHC           │ 20+ years  │ ₹300 │ 📞 +91 020243 │
└─────────────────────────┴────────────────┴────────────────────┴────────────┴──────┴─────────────────┘

💡 Contact the hospital to confirm doctor availability and book an appointment.
```

**Key Files**:
- `backend/models/doctor_model.py` — MongoDB model + seed data (28 doctors)
- `backend/services/doctor_service.py` — Report-type → specialist mapping + advice text
- `backend/routes/doctors.py` — REST API for doctor CRUD
- `frontend/src/pages/Dashboard.jsx` — Critical alert banner + doctor suggestion table

---

## 🆘 Troubleshooting Guide

### Android App Issues

**Issue**: App crashes on startup
**Solution**:
```
1. Clear app data: Settings → Apps → RAGnosis → Clear Cache
2. Ensure SDK 54+ is installed
3. Update all Expo packages: expo upgrade
4. Restart Expo dev server
```

**Issue**: File upload fails
**Solution**:
```
1. Check permissions: Settings → Apps → RAGnosis → 
   Permissions → Grant Storage & Camera access
2. Verify backend IP in src/api/client.js
3. Ensure backend server is running (curl http://10.0.2.2:5000/api/health)
```

**Issue**: Notifications not appearing
**Solution**:
```
1. In app: Go to Reminders → Toggle reminder off/on
2. In phone: Settings → Apps → RAGnosis → Notifications → Allow
3. Ensure Expo.Notifications plugin in app.json is configured
4. Check that time format is valid (0-23 for hours)
```

### Web App Issues

**Issue**: Charts not rendering
**Solution**:
```
1. Ensure Recharts is installed: npm install recharts
2. Check browser console (F12) for errors
3. Clear browser cache: Ctrl+Shift+Delete
4. Try different browser (Chrome, Firefox)
```

**Issue**: Can't upload reports
**Solution**:
```
1. Check backend is running: curl http://localhost:5000/api/health
2. Verify CORS is enabled in backend/app.py
3. Check file size (< 16MB)
4. Check file type (PDF, JPG, PNG only)
```

### Backend Issues

**Issue**: Tesseract OCR errors
**Solution**:
```bash
# Install Tesseract:
# Ubuntu: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

# Verify installation:
tesseract --version

# If using non-standard path, set in .env:
# TESSERACT_CMD=/usr/bin/tesseract (or your path)
```

**Issue**: MongoDB connection fails
**Solution**:
```
1. Verify MongoDB URI in .env is correct
2. Check internet connection (MongoDB Atlas needs public IP)
3. Whitelist your IP in MongoDB Atlas → Network Access
4. Test connection: python -c "from pymongo import MongoClient; print(MongoClient('YOUR_URI'))"
```

**Issue**: Groq API errors
**Solution**:
```
1. Verify GROQ_API_KEY in .env is correct
2. Check API key is active in Groq Console
3. Ensure you have API quota remaining
4. Test API: curl -X POST https://api.groq.com/... -H "Authorization: Bearer YOUR_KEY"
```

---

## 📊 System Metrics & Performance

### Expected Response Times
- Report upload: 15–30 seconds (OCR + analysis)
- Report retrieval: < 500ms
- Chatbot response: 2–5 seconds (streaming)
- Medicine reminder setup: < 1 second
- Metrics calculation: < 100ms

### Storage Requirements
- MongoDB: ~100MB per 1,000 users
- File uploads: ~1–5MB per report
- ML models: ~500MB (FAISS index, embeddings)
- Total: ~2–3GB for production setup

### Scalability
- Horizontal: Add more backend instances (Flask)
- Vertical: Upgrade MongoDB plan (larger instance)
- Caching: Implement Redis for frequently accessed reports
- Async: Use Celery for long-running tasks (OCR)

---

## 🎓 Learning Resources

### Medical Domain
- [BloodTest Results Explained](https://www.mayoclinic.org/)
- [Medical Abbreviations](https://en.wikipedia.org/wiki/List_of_medical_abbreviations)

### NLP & AI
- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [FAISS Documentation](https://faiss.ai/)
- [Groq API Docs](https://console.groq.com/)

### Development
- [React Documentation](https://react.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Expo Documentation](https://docs.expo.dev/)

---

## 📞 Support & Contributing

For issues, feature requests, or contributions:
1. Check troubleshooting guide above
2. Review existing GitHub issues
3. Contact development team
4. Submit pull request with improvements

---

## 📄 License & Credits

**Project**: RAGnosis (PICT InC 2025)
**Developed by**: Pune Institute of Computer Technology

**Technologies**:
- OpenAI / HuggingFace for AI models
- MongoDB for database
- Expo for mobile framework
- Groq for LLM inference
- Flask for backend

---

**Last Updated**: April 26, 2026  
**Version**: 1.1.0 — Added Critical Detection & Doctor Suggestion System
