# 🎬 RAGnosis Project Video Script

## **Total Duration: ~8-10 minutes**

---

## 📺 **OPENING (0:00-0:30) — 30 seconds**

### VISUAL: Hero animation, glowing AI pipeline diagram

**[SPEAKING — Energetic, professional tone]**

"Hello! I'm explaining **RAGnosis** — an AI-powered medical intelligence platform that's transforming how patients, doctors, and hospitals manage health reports.

Today, I'm going to walk you through the complete system — showing you exactly how it works from three different perspectives: as a **patient**, as a **receptionist**, and as a **doctor**. 

Let's dive in!"

**[PAUSE 2 seconds]**

---

## 🏥 **PART 1: PATIENT / USER FLOW (0:30-3:30) — 3 minutes**

### **SECTION 1.1: Registration & Login (0:30-1:30)**

#### VISUAL: Landing page → Register page

**[SPEAKING]**

"First, let's see how a patient gets started. When you visit RAGnosis, you're greeted with this beautiful landing page showing our core features:

- Intelligent AI analysis of medical reports
- RAG-powered chatbot for medical questions
- Real-time health metrics and trends
- And integration with hospitals nationwide

To get started, the patient clicks **'Register'** here.

**[POINT to register button]**

On the registration page, the patient enters their **medical profile**:
- Name, email, and mobile number
- Age, height, and weight
- Blood group and blood pressure
- Gender

**[PAUSE]** This information helps our AI provide personalized health insights. Once they submit, their account is created, and they're ready to login."

---

#### VISUAL: Login page → Dashboard overview

**[SPEAKING - CONTINUE]**

"On login, the patient enters their **email or mobile number** and password — yes, both work!

**[SHOW login form with both options highlighted]**

Once logged in, they enter their personalized dashboard with **8 powerful tabs**. Let me walk you through each one..."

---

### **SECTION 1.2: Patient Dashboard - All Features (1:30-3:30)**

#### **Tab 1: 📊 Overview (1:30-1:50)**

**[VISUAL: Click on Overview tab, show summary cards]**

**[SPEAKING]**

"**Overview** is their health summary at a glance:
- Total reports uploaded
- Reports this month
- A preview of their latest report with an AI-generated summary

This gives them a quick snapshot of their health status without diving deep."

---

#### **Tab 2: 📤 Upload Report (1:50-2:10)**

**[VISUAL: Drag-and-drop zone, upload, progress bar]**

**[SPEAKING]**

"**Upload Report** is where the magic happens! 

The patient can either:
- **Drag and drop** a PDF or image of their blood test
- Or **click to browse** their file

Our AI pipeline instantly:
1. **Extracts all medical metrics** — hemoglobin, glucose, cholesterol, etc.
2. **Generates an AI summary** in plain English
3. **Analyzes abnormal values** and provides health insights
4. **Saves everything** for future tracking

**[SHOW progress bar filling]**

The entire process takes just a few seconds!"

---

#### **Tab 3: 📋 My Reports (2:10-2:25)**

**[VISUAL: Grid of report cards, click to view detail]**

**[SPEAKING]**

"**My Reports** shows all their uploaded blood tests as cards, including:
- Report type (CBC, Diabetes, Lipid Panel, etc.)
- Number of metrics extracted
- Upload date

They can click any report to see the **full AI analysis**, extracted metrics, and personalized health recommendations."

---

#### **Tab 4: 📊 Health Metrics (2:25-2:45)**

**[VISUAL: Health card with metric selector, trends, charts]**

**[SPEAKING]**

"**Health Metrics** is our advanced analytics dashboard. Here's what makes it special:

First, they see their **overall Health Score** — a 0-100% rating based on how many of their metrics are normal. 

**[POINT to health score]**

Then, they can **select a report type** like CBC — and instantly see:
- All 4 CBC metrics: hemoglobin, WBC, RBC, platelets
- A 3-report trend chart showing how each value has changed over time
- Color-coded status: ✅ Normal, ⚠️ High, ⚠️ Low

We also provide **insurance recommendations** — telling them which health insurance plan fits their health profile."

---

#### **Tab 5: 💊 Medicine Reminders (2:45-2:55)**

**[VISUAL: Click add reminder, set medicine name and time]**

**[SPEAKING]**

"**Medicine Reminders** lets patients set daily medication alerts:
- Choose medicine name
- Set time of day
- Set frequency (daily, alternate, weekly)

They'll get **daily push notifications** on their phone, so they never miss a dose!"

---

#### **Tab 6: 🩺 Prescriptions (2:55-3:10)**

**[VISUAL: Click prescription card header, medicines expand]**

**[SPEAKING]**

"**Prescriptions** shows all medicines prescribed by their doctor:

By default, they see only the **doctor's name, date, and medicine count**. 

**[CLICK to expand]**

When they open it, they see:
- Medicine name and dosage
- Frequency (twice daily, etc.)
- Duration (30 days)
- Special instructions (take with food, etc.)
- Doctor's notes

This way, they always have their prescription handy!"

---

#### **Tab 7: 🤖 AI Chatbot (3:10-3:25)**

**[VISUAL: Type a question, get AI response with context]**

**[SPEAKING]**

"**AI Chatbot** is powered by Groq's LLaMA 3 with **RAG** — Retrieval-Augmented Generation.

Patients can ask **any health question**:
- 'What does hemoglobin mean?'
- 'Why is my glucose high?'
- 'What should I eat?'

Our AI:
1. Searches our medical knowledge base
2. Pulls context from their reports
3. Gives a personalized, accurate answer

**[SHOW response appearing]**

The response cites sources and is grounded in real medical data."

---

#### **Tab 8: 👤 My Profile (3:25-3:30)**

**[VISUAL: Show profile page with all medical info]**

**[SPEAKING]**

"**My Profile** displays their complete medical information for reference or updating. They can also **logout** from here.

That's the complete patient experience! Now, let's see how the hospital portal works..."

---

## 👔 **PART 2: RECEPTIONIST FLOW (3:30-5:30) — 2 minutes**

### **SECTION 2.1: Receptionist Registration & Link (3:30-4:00)**

#### VISUAL: Hospital landing page → Receptionist login card → Register form

**[SPEAKING]**

"Now let's look at the **hospital portal** — starting with receptionists.

When a receptionist opens the app, they see the **Hospital Portal section** on the landing page with three roles: Patient, Doctor, and Receptionist.

**[POINT to receptionist card]**

If it's their **first time**, they click **'Register as Receptionist'** and enter:
- Name
- Email
- Password
- And most importantly: **Doctor ID**

The Doctor ID is a unique code (like 'DR-2025-0001') that **links them to a specific doctor**. This is key — one receptionist works for one doctor, so they only see that doctor's appointments.

**[SHOW dropdown of available doctors or link instructions]**

Once registered, they get a JWT token with role: 'receptionist'."

---

### **SECTION 2.2: Receptionist Dashboard — 3 Tabs (4:00-5:30)**

#### **Tab 1: 📅 Book Appointment (4:00-4:30)**

**[VISUAL: Search patient form → Calendar picker → Book button]**

**[SPEAKING]**

"The receptionist's main job is **booking appointments** for their doctor.

Here's the flow:

**Step 1:** They search for a patient by:
- Name
- Email
- Mobile number

**[SHOW live search working]**

**Step 2:** They select the patient

**Step 3:** They pick a date (defaults to today)

**Step 4:** They pick a time (defaults to now + 30 minutes)

**Step 5:** They click **'Book Appointment'**

That appointment is now saved in the system. The patient will see it on their dashboard, and the doctor will see it in their appointments list."

---

#### **Tab 2: ☁️ Upload Report (4:30-5:00)**

**[VISUAL: Patient search → File picker → Upload → AI processing]**

**[SPEAKING]**

"Receptionists can also **upload blood reports on behalf of patients** — super useful when patients bring physical copies or when testing happens at the clinic.

The flow is:
1. Search for the patient
2. Upload a PDF or image of their blood test
3. Click upload

**[SHOW upload happening]**

Our AI pipeline kicks in immediately:
- Extracts all metrics
- Generates a summary
- Saves it under the patient's account

The patient instantly sees the new report in their 'My Reports' tab — no manual file transfer needed!"

---

#### **Tab 3: 📋 All Appointments (5:00-5:30)**

**[VISUAL: Click appointments tab, show list with dates and statuses]**

**[SPEAKING]**

"**All Appointments** shows every appointment booked by this receptionist:

- Patient name
- Appointment date and time
- Prescription status (pending or completed)

The receptionist can see at a glance:
- Which appointments the doctor still needs to prescribe for
- The complete history of bookings

This helps them follow up and ensure no patient falls through the cracks.

That's the receptionist's role! Now let's meet the **doctor**..."

---

## 🩺 **PART 3: DOCTOR FLOW (5:30-8:00) — 2.5 minutes**

### **SECTION 3.1: Doctor Registration & Get Doctor ID (5:30-6:00)**

#### VISUAL: Doctor login page → Register form

**[SPEAKING]**

"When a **doctor** visits RAGnosis, they see the Doctor Portal login.

On their **first visit**, they click **'Register as Doctor'** and enter:
- Name
- Email
- Password
- **Specialization** (Cardiology, Dermatology, etc.)
- **Hospital name** (where they practice)
- Phone number

**[SHOW form being filled]**

Once submitted, the system generates a **unique Doctor ID** — something like 'DR-2025-0042'.

**[HIGHLIGHT Doctor ID prominently]**

This Doctor ID is important! The doctor needs to share it with any receptionist that will be booking their appointments."

---

### **SECTION 3.2: Doctor Dashboard — Sidebar (6:00-6:20)**

#### VISUAL: Doctor logs in, show sidebar with doctor info

**[SPEAKING]**

"On the doctor's dashboard sidebar, they see:
- Their name
- Specialization
- Hospital
- **Their unique Doctor ID** (with a copy button)

They can share this ID with admin or send it to receptionists via email. The receptionist then uses this ID during registration to link to the doctor."

---

### **SECTION 3.3: Doctor Dashboard — Today's Appointments (6:20-7:30)**

#### VISUAL: Today's appointments tab with table, click prescribe button

**[SPEAKING]**

"The **'Today's Appointments'** tab shows all appointments scheduled for the current day.

The table displays:
- **Patient Name**
- **Mobile and Email** (to contact them)
- **Appointment Time**
- **Prescription Status** (Pending or ✅ Prescribed)
- **✍️ Prescribe Button**

**[POINT to a pending appointment]**

When the doctor clicks **'Prescribe'** for a patient, a modal opens:

**[SHOW prescribe modal]**

The doctor can add **multiple medicines**:
- **Medicine Name** (e.g., 'Aspirin')
- **Dosage** (e.g., '100mg')
- **Frequency** — a dropdown with options:
  - Once daily
  - Twice daily
  - Three times daily
  - Every 6 hours
  - As needed
- **Duration** (e.g., '30 days')
- **Instructions** (e.g., 'Take with food')

They can also add **Doctor's Notes** — general medical advice for the patient.

**[SHOW multiple medicines being added]**

Once they click **'Save Prescription'**, the system stores it, and:
1. The button changes to **✅ Prescribed** (prevents duplicate entries)
2. The patient instantly sees this prescription in their dashboard
3. Each medicine is saved with full details

This is seamless — no paperwork, all digital!"

---

### **SECTION 3.4: Doctor Dashboard — All Patients (7:30-8:00)**

#### VISUAL: All patients tab, click patient, show prescription history

**[SPEAKING]**

"The **'All Patients'** tab shows every unique patient the doctor has ever seen.

From here, the doctor can:
- **Search by name** using the search bar
- **Click a patient** to view their full prescription history
- See all medicines prescribed, dates, and dosages

This is helpful for:
- Following up on long-term patients
- Checking what they've prescribed before
- Understanding a patient's medical history in seconds

**[SHOW clicking a patient and viewing history]**

Perfect for continuity of care!"

---

## 🔄 **SECTION 3.5: Complete End-to-End Flow Recap (8:00-8:30)**

#### VISUAL: Animated flowchart showing all 3 roles

**[SPEAKING — Summarizing]**

"So here's how the complete hospital workflow works:

**Step 1: Receptionist** books an appointment for a patient with the doctor

**Step 2: Receptionist** uploads the patient's blood report (optional — patient can do it too)

**Step 3: Patient** logs in, sees the appointment, can view their report, check health metrics, and chat with our AI chatbot

**Step 4: Doctor** logs in, sees today's appointments, reviews the patient's reports, and prescribes medicines directly in the system

**Step 5: Patient** receives a notification, sees the new prescription, can set medicine reminders, and track their health

**[PAUSE]**

Everything is **automated, secure, and instant** — no paper, no delays, no miscommunication.

And the **AI layer** is watching everything:
- Extracting metrics from PDFs automatically
- Generating summaries
- Providing personalized health insights
- Answering patient questions via chatbot

This is the future of healthcare! 🚀"

---

## 🎓 **CLOSING (8:30-9:00) — 30 seconds**

#### VISUAL: Key features recap, team slide, project name

**[SPEAKING]**

"**RAGnosis** brings together:
- ✅ Intelligent AI-powered medical report analysis
- ✅ A seamless hospital management workflow
- ✅ Real-time health tracking and insights
- ✅ 24/7 AI chatbot for patient questions
- ✅ Beautiful, dark-themed interface for easy use

Built on cutting-edge technology:
- Artificial Intelligence: BioBERT, BART, RAG, Groq LLaMA 3
- Frontend: React 18 with smooth animations
- Backend: Python Flask with secure JWT authentication
- Database: MongoDB for real-time storage
- Mobile: React Native for iOS and Android

This is **RAGnosis** — where AI meets healthcare.

Thank you for watching! If you have questions, check out our documentation, and feel free to try the demo accounts right on our website.

See you next time! 👋"

**[FADE OUT with project logo]**

---

## 📝 **OPTIONAL: Demo Credentials Slide (End Credits)**

**[Display on screen for 15 seconds]**

```
🎬 RAGNOSIS - DEMO CREDENTIALS

Try it yourself!

👤 PATIENT
- Register a new account at /register
- Use any email and password

🏥 HOSPITAL PORTAL

🩺 DOCTOR
- Email: demo.doctor@ragnosis.com
- Password: demo1234
- URL: /doctor/login

👔 RECEPTIONIST
- Email: demo.receptionist@ragnosis.com
- Password: demo1234
- URL: /receptionist/login

⚡ PRO TIP: Click "Create Demo Accounts" on the landing page
to auto-seed these demo accounts!
```

---

## 🎥 **FILMING TIPS**

### **What to Show:**
1. **Screen Recording** of the entire flow (Patient → Receptionist → Doctor)
2. **Zoomed-in views** of important buttons/fields
3. **Smooth transitions** between tabs/pages
4. **Real data** (make demo reports with actual metrics)
5. **Animations** — show the AI pipeline animation on /system page

### **Pacing:**
- **Intro**: Energetic, hook them immediately
- **Patient section**: Show practical use cases, relatable
- **Receptionist section**: Emphasize efficiency and automation
- **Doctor section**: Highlight clinical benefits and ease of use
- **Closing**: Inspire with technology + impact

### **Audio:**
- Use **clear, professional narration**
- Add **subtle background music** (healthcare/tech vibe)
- **No mumbling** — practice the script once before recording
- Pause for 2-3 seconds between major sections

### **Visual Effects (Optional):**
- Highlight important buttons with **arrows or circles**
- Add **text overlays** for key terms (AI, RAG, JWT, MongoDB)
- Use **color flash effects** when showing results
- Fade between sections cleanly

### **Resolution:**
- Record in **1080p (1920×1080)** minimum
- Use **4K if possible** for a professional look
- Test **zoom levels** so text is readable

---

## ⏱️ **TIME BREAKDOWN**

| Section | Duration | Start-End |
|---------|----------|-----------|
| Opening | 30s | 0:00-0:30 |
| Patient Registration | 1m | 0:30-1:30 |
| Patient Dashboard (6 tabs) | 2m | 1:30-3:30 |
| Receptionist Registration | 30s | 3:30-4:00 |
| Receptionist Dashboard | 1.5m | 4:00-5:30 |
| Doctor Registration | 30s | 5:30-6:00 |
| Doctor Sidebar | 20s | 6:00-6:20 |
| Doctor Dashboard | 1m 10s | 6:20-7:30 |
| Doctor All Patients | 30s | 7:30-8:00 |
| End-to-End Summary | 30s | 8:00-8:30 |
| Closing | 30s | 8:30-9:00 |
| **TOTAL** | **~9 minutes** | |

---

## 🎯 **KEY MESSAGES TO EMPHASIZE**

✨ **"AI-Powered"** — Mention multiple times (BioBERT, BART, RAG, Groq)
📊 **"Automated"** — No manual data entry, no delays
🔄 **"Seamless Workflow"** — Patient → Receptionist → Doctor → Patient
🔐 **"Secure"** — JWT, encryption, role-based access
💡 **"User-Friendly"** — Dark theme, smooth animations, intuitive UI
⚡ **"Real-Time"** — Instant report processing, live notifications
🌍 **"Hospital Integration"** — Works nationwide, scalable

---

**Good luck with your video! This script is ready to record. 🎬**
