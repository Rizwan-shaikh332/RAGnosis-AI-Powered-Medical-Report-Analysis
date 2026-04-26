"""
Doctor model — MongoDB collection for doctors near Katraj, Pune.
Each doctor has: name, specialization, hospital, location, city, contact, experience, qualification
"""
from database import get_db
from bson import ObjectId


def seed_doctors():
    """Seed the doctors collection with real doctors near Katraj, Pune."""
    db = get_db()

    # Only seed if collection is empty
    if db.suggested_doctors.count_documents({}) > 0:
        return

    doctors = [
        # ─── HEMATOLOGISTS ───────────────────────────────────────
        {
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
        },
        {
            "name": "Dr. Sameer Melinkeri",
            "specialization": "Hematologist",
            "qualification": "MD, DM (Hematology)",
            "hospital": "Deenanath Mangeshkar Hospital",
            "location": "Erandwane",
            "city": "Pune",
            "contact": "+91 020 49153000",
            "experience": "20+ years",
            "rating": 4.7,
            "consultation_fee": "₹1000",
            "available_days": "Mon–Fri"
        },

        # ─── ENDOCRINOLOGISTS / DIABETOLOGISTS ───────────────────
        {
            "name": "Dr. Shailaja Kale",
            "specialization": "Endocrinologist",
            "qualification": "MD, DM (Endocrinology)",
            "hospital": "Bharati Hospital, Dhankawadi",
            "location": "Dhankawadi",
            "city": "Pune",
            "contact": "+91 020 40555555",
            "experience": "12+ years",
            "rating": 4.4,
            "consultation_fee": "₹600",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Anjali Bhatt",
            "specialization": "Endocrinologist",
            "qualification": "MBBS, MD (Medicine), DM (Endocrinology)",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "10+ years",
            "rating": 4.3,
            "consultation_fee": "₹700",
            "available_days": "Tue–Sat"
        },
        {
            "name": "Dr. Chaitanya Kulkarni",
            "specialization": "Endocrinologist",
            "qualification": "MBBS, DNB (Medicine), DM (Endocrinology)",
            "hospital": "KEM Hospital, Rasta Peth",
            "location": "Rasta Peth",
            "city": "Pune",
            "contact": "+91 020 26217300",
            "experience": "18+ years",
            "rating": 4.6,
            "consultation_fee": "₹500",
            "available_days": "Mon–Fri"
        },

        # ─── CARDIOLOGISTS ───────────────────────────────────────
        {
            "name": "Dr. Abhijeet Palshikar",
            "specialization": "Cardiologist",
            "qualification": "MD, DM (Cardiology)",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "18+ years",
            "rating": 4.8,
            "consultation_fee": "₹1000",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Shirish Hiremath",
            "specialization": "Cardiologist",
            "qualification": "MD, DM (Cardiology), FACC",
            "hospital": "Ruby Hall Clinic, Sassoon Road",
            "location": "Sassoon Road",
            "city": "Pune",
            "contact": "+91 020 26163391",
            "experience": "25+ years",
            "rating": 4.9,
            "consultation_fee": "₹1200",
            "available_days": "Mon–Fri"
        },

        # ─── NEPHROLOGISTS ───────────────────────────────────────
        {
            "name": "Dr. Manan Doshi",
            "specialization": "Nephrologist",
            "qualification": "MD, DM (Nephrology)",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "12+ years",
            "rating": 4.5,
            "consultation_fee": "₹800",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Atul Mulay",
            "specialization": "Nephrologist",
            "qualification": "MD, DNB (Nephrology)",
            "hospital": "Bharati Hospital, Dhankawadi",
            "location": "Dhankawadi",
            "city": "Pune",
            "contact": "+91 020 40555555",
            "experience": "20+ years",
            "rating": 4.6,
            "consultation_fee": "₹700",
            "available_days": "Mon–Fri"
        },

        # ─── HEPATOLOGISTS / GASTROENTEROLOGISTS ─────────────────
        {
            "name": "Dr. Nitin Pai",
            "specialization": "Hepatologist",
            "qualification": "MD, DM (Gastroenterology)",
            "hospital": "Jehangir Hospital",
            "location": "Sassoon Road",
            "city": "Pune",
            "contact": "+91 020 66810000",
            "experience": "15+ years",
            "rating": 4.7,
            "consultation_fee": "₹900",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Pravin Rathi",
            "specialization": "Hepatologist",
            "qualification": "MD, DM (Gastroenterology & Hepatology)",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "22+ years",
            "rating": 4.8,
            "consultation_fee": "₹1000",
            "available_days": "Mon–Fri"
        },

        # ─── RADIOLOGISTS ────────────────────────────────────────
        {
            "name": "Dr. Rashmi Goel",
            "specialization": "Radiologist",
            "qualification": "MD (Radiology)",
            "hospital": "Bharati Hospital, Dhankawadi",
            "location": "Dhankawadi",
            "city": "Pune",
            "contact": "+91 020 40555555",
            "experience": "14+ years",
            "rating": 4.4,
            "consultation_fee": "₹500",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Sanjay Deshmukh",
            "specialization": "Radiologist",
            "qualification": "MD, DNB (Radiology)",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "16+ years",
            "rating": 4.5,
            "consultation_fee": "₹600",
            "available_days": "Mon–Sat"
        },

        # ─── GENERAL PHYSICIANS ──────────────────────────────────
        {
            "name": "Dr. Vinod Borse",
            "specialization": "General Physician",
            "qualification": "MBBS, MD (General Medicine)",
            "hospital": "Katraj Primary Health Centre",
            "location": "Katraj",
            "city": "Pune",
            "contact": "+91 020 24370100",
            "experience": "20+ years",
            "rating": 4.3,
            "consultation_fee": "₹300",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Suresh Jagtap",
            "specialization": "General Physician",
            "qualification": "MBBS, DNB (Family Medicine)",
            "hospital": "Bharati Hospital, Dhankawadi",
            "location": "Dhankawadi",
            "city": "Pune",
            "contact": "+91 020 40555555",
            "experience": "18+ years",
            "rating": 4.4,
            "consultation_fee": "₹400",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Meena Patil",
            "specialization": "General Physician",
            "qualification": "MBBS, MD (Medicine)",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "12+ years",
            "rating": 4.2,
            "consultation_fee": "₹500",
            "available_days": "Mon–Fri"
        },

        # ─── DIABETOLOGISTS ──────────────────────────────────────
        {
            "name": "Dr. Rahul Baxi",
            "specialization": "Diabetologist",
            "qualification": "MBBS, MD (Medicine), Fellowship in Diabetology",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "14+ years",
            "rating": 4.5,
            "consultation_fee": "₹700",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Sanjeev Kelkar",
            "specialization": "Diabetologist",
            "qualification": "MBBS, MD, FACE (Diabetology)",
            "hospital": "Bharati Hospital, Dhankawadi",
            "location": "Dhankawadi",
            "city": "Pune",
            "contact": "+91 020 40555555",
            "experience": "18+ years",
            "rating": 4.6,
            "consultation_fee": "₹600",
            "available_days": "Mon–Fri"
        },

        # ─── UROLOGISTS ──────────────────────────────────────────
        {
            "name": "Dr. Sujit Joshi",
            "specialization": "Urologist",
            "qualification": "MBBS, MS, MCh (Urology)",
            "hospital": "Ruby Hall Clinic, Sassoon Road",
            "location": "Sassoon Road",
            "city": "Pune",
            "contact": "+91 020 26163391",
            "experience": "22+ years",
            "rating": 4.8,
            "consultation_fee": "₹1000",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Amol Patil",
            "specialization": "Urologist",
            "qualification": "MBBS, MS (Surgery), DNB (Urology)",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "12+ years",
            "rating": 4.4,
            "consultation_fee": "₹800",
            "available_days": "Mon–Fri"
        },

        # ─── ORTHOPEDIC SURGEONS ─────────────────────────────────
        {
            "name": "Dr. Sachin Tapasvi",
            "specialization": "Orthopedic Surgeon",
            "qualification": "MBBS, MS (Orthopedics), DNB",
            "hospital": "Jehangir Hospital",
            "location": "Sassoon Road",
            "city": "Pune",
            "contact": "+91 020 66810000",
            "experience": "20+ years",
            "rating": 4.9,
            "consultation_fee": "₹1200",
            "available_days": "Mon–Fri"
        },
        {
            "name": "Dr. Kiran Dhole",
            "specialization": "Orthopedic Surgeon",
            "qualification": "MBBS, D.Ortho, DNB (Orthopedics)",
            "hospital": "Bharati Hospital, Dhankawadi",
            "location": "Dhankawadi",
            "city": "Pune",
            "contact": "+91 020 40555555",
            "experience": "15+ years",
            "rating": 4.5,
            "consultation_fee": "₹800",
            "available_days": "Mon–Sat"
        },

        # ─── DERMATOLOGISTS ──────────────────────────────────────
        {
            "name": "Dr. Madhuri Pawar",
            "specialization": "Dermatologist",
            "qualification": "MBBS, MD (Dermatology)",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "10+ years",
            "rating": 4.4,
            "consultation_fee": "₹600",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Neeta Shah",
            "specialization": "Dermatologist",
            "qualification": "MBBS, DVD, DNB (Dermatology)",
            "hospital": "KEM Hospital, Rasta Peth",
            "location": "Rasta Peth",
            "city": "Pune",
            "contact": "+91 020 26217300",
            "experience": "16+ years",
            "rating": 4.6,
            "consultation_fee": "₹500",
            "available_days": "Mon–Fri"
        },

        # ─── PULMONOLOGISTS ──────────────────────────────────────
        {
            "name": "Dr. Arvind Kate",
            "specialization": "Pulmonologist",
            "qualification": "MBBS, MD (Pulmonary Medicine)",
            "hospital": "Bharati Hospital, Dhankawadi",
            "location": "Dhankawadi",
            "city": "Pune",
            "contact": "+91 020 40555555",
            "experience": "18+ years",
            "rating": 4.7,
            "consultation_fee": "₹700",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Swapnil Kulkarni",
            "specialization": "Pulmonologist",
            "qualification": "MBBS, DNB (Respiratory Medicine)",
            "hospital": "Deenanath Mangeshkar Hospital",
            "location": "Erandwane",
            "city": "Pune",
            "contact": "+91 020 49153000",
            "experience": "12+ years",
            "rating": 4.5,
            "consultation_fee": "₹800",
            "available_days": "Mon–Fri"
        },

        # ─── GASTROENTEROLOGISTS ─────────────────────────────────
        {
            "name": "Dr. Abhijit Chougule",
            "specialization": "Gastroenterologist",
            "qualification": "MBBS, MD, DM (Gastroenterology)",
            "hospital": "Sahyadri Hospital, Bibwewadi",
            "location": "Bibwewadi",
            "city": "Pune",
            "contact": "+91 8806252525",
            "experience": "14+ years",
            "rating": 4.6,
            "consultation_fee": "₹900",
            "available_days": "Mon–Sat"
        },
        {
            "name": "Dr. Shubhangi Deshmukh",
            "specialization": "Gastroenterologist",
            "qualification": "MBBS, MD, DM (Gastro & Hepatology)",
            "hospital": "Ruby Hall Clinic, Sassoon Road",
            "location": "Sassoon Road",
            "city": "Pune",
            "contact": "+91 020 26163391",
            "experience": "16+ years",
            "rating": 4.7,
            "consultation_fee": "₹1000",
            "available_days": "Mon–Fri"
        },
    ]

    db.suggested_doctors.insert_many(doctors)
    # Create index for fast specialization lookups
    db.suggested_doctors.create_index("specialization")
    db.suggested_doctors.create_index("city")
    print(f"[SEED] Inserted {len(doctors)} doctors into the 'suggested_doctors' collection.")


def get_all_doctors(city=None, specialization=None):
    """Fetch doctors from MongoDB, optionally filtered."""
    db = get_db()
    query = {}
    if city:
        query["city"] = city
    if specialization:
        query["specialization"] = specialization
    docs = list(db.suggested_doctors.find(query))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


def get_doctor_by_id(doctor_id):
    db = get_db()
    d = db.suggested_doctors.find_one({"_id": ObjectId(doctor_id)})
    if d:
        d["_id"] = str(d["_id"])
    return d


def add_doctor(data):
    """Add a new doctor to the database."""
    db = get_db()
    result = db.suggested_doctors.insert_one(data)
    return str(result.inserted_id)


def delete_doctor(doctor_id):
    """Remove a doctor from the database."""
    db = get_db()
    db.suggested_doctors.delete_one({"_id": ObjectId(doctor_id)})
