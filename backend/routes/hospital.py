"""
Hospital portal routes — Doctor & Receptionist
Collections used:
  - doctors
  - receptionists
  - appointments
  - prescriptions
  - reports (existing) — receptionist uploads go here under the patient's user_id
"""

import os
import uuid
import traceback
from datetime import datetime, date, timedelta

import bcrypt
from bson import ObjectId
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from database import get_db
from utils.jwt_helper import generate_token, require_role, require_auth
from config import Config

hospital_bp = Blueprint("hospital", __name__)

# ─────────────────────────────────────────────
#  PASSWORD HELPERS
# ─────────────────────────────────────────────

def _hash(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def _verify(pw: str, hashed: str) -> bool:
    return bcrypt.checkpw(pw.encode(), hashed.encode())


# ═══════════════════════════════════════════════
#  DOCTOR — REGISTER & LOGIN
# ═══════════════════════════════════════════════

@hospital_bp.route("/doctor/register", methods=["POST"])
def doctor_register():
    data = request.get_json()
    for field in ["name", "email", "password", "specialization"]:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    db = get_db()
    if db.doctors.find_one({"email": data["email"].lower()}):
        return jsonify({"error": "Email already registered"}), 409

    doc = {
        "name": data["name"],
        "email": data["email"].lower(),
        "password": _hash(data["password"]),
        "specialization": data["specialization"],
        "hospital": data.get("hospital", ""),
        "created_at": datetime.utcnow(),
    }
    result = db.doctors.insert_one(doc)
    doctor_id = str(result.inserted_id)
    token = generate_token(doctor_id, role="doctor")
    return jsonify({
        "message": f"Welcome Dr. {data['name']}! 🩺",
        "token": token,
        "doctor": {"id": doctor_id, "name": data["name"], "email": data["email"]},
    }), 201


@hospital_bp.route("/doctor/login", methods=["POST"])
def doctor_login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = get_db()
    doctor = db.doctors.find_one({"email": email})
    if not doctor or not _verify(password, doctor["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(str(doctor["_id"]), role="doctor")
    return jsonify({
        "message": f"Welcome back, Dr. {doctor['name']}! 👋",
        "token": token,
        "doctor": {
            "id": str(doctor["_id"]),
            "name": doctor["name"],
            "email": doctor["email"],
            "specialization": doctor.get("specialization", ""),
            "hospital": doctor.get("hospital", ""),
        },
    }), 200


@hospital_bp.route("/doctor/me", methods=["GET"])
@require_role("doctor")
def doctor_me():
    db = get_db()
    doc = db.doctors.find_one({"_id": ObjectId(request.user_id)})
    if not doc:
        return jsonify({"error": "Doctor not found"}), 404
    doc["_id"] = str(doc["_id"])
    doc.pop("password", None)
    return jsonify(doc), 200


# ═══════════════════════════════════════════════
#  RECEPTIONIST — REGISTER & LOGIN
# ═══════════════════════════════════════════════

@hospital_bp.route("/receptionist/register", methods=["POST"])
def receptionist_register():
    data = request.get_json()
    for field in ["name", "email", "password", "doctor_id"]:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    db = get_db()

    # Validate doctor_id
    try:
        doctor = db.doctors.find_one({"_id": ObjectId(data["doctor_id"])})
    except Exception:
        return jsonify({"error": "Invalid doctor_id format"}), 400
    if not doctor:
        return jsonify({"error": "No doctor found with that ID"}), 404

    if db.receptionists.find_one({"email": data["email"].lower()}):
        return jsonify({"error": "Email already registered"}), 409

    rec = {
        "name": data["name"],
        "email": data["email"].lower(),
        "password": _hash(data["password"]),
        "doctor_id": data["doctor_id"],
        "created_at": datetime.utcnow(),
    }
    result = db.receptionists.insert_one(rec)
    rec_id = str(result.inserted_id)
    token = generate_token(rec_id, role="receptionist")
    return jsonify({
        "message": f"Welcome, {data['name']}! 🏥",
        "token": token,
        "receptionist": {"id": rec_id, "name": data["name"], "email": data["email"], "doctor_id": data["doctor_id"]},
    }), 201


@hospital_bp.route("/receptionist/login", methods=["POST"])
def receptionist_login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = get_db()
    rec = db.receptionists.find_one({"email": email})
    if not rec or not _verify(password, rec["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    # Also fetch linked doctor info
    doctor = db.doctors.find_one({"_id": ObjectId(rec["doctor_id"])})

    token = generate_token(str(rec["_id"]), role="receptionist")
    return jsonify({
        "message": f"Welcome, {rec['name']}! 🏥",
        "token": token,
        "receptionist": {
            "id": str(rec["_id"]),
            "name": rec["name"],
            "email": rec["email"],
            "doctor_id": rec["doctor_id"],
            "doctor_name": doctor["name"] if doctor else "Unknown",
        },
    }), 200


@hospital_bp.route("/receptionist/me", methods=["GET"])
@require_role("receptionist")
def receptionist_me():
    db = get_db()
    rec = db.receptionists.find_one({"_id": ObjectId(request.user_id)})
    if not rec:
        return jsonify({"error": "Receptionist not found"}), 404
    rec["_id"] = str(rec["_id"])
    rec.pop("password", None)
    doctor = db.doctors.find_one({"_id": ObjectId(rec["doctor_id"])})
    rec["doctor_name"] = doctor["name"] if doctor else "Unknown"
    return jsonify(rec), 200


# ═══════════════════════════════════════════════
#  PATIENT SEARCH  (receptionist)
# ═══════════════════════════════════════════════

@hospital_bp.route("/patients/search", methods=["GET"])
@require_role("receptionist")
def search_patients():
    q = request.args.get("q", "").strip()
    if not q or len(q) < 2:
        return jsonify({"patients": []}), 200

    db = get_db()
    # Search by name, email, or mobile using regex (case-insensitive)
    regex = {"$regex": q, "$options": "i"}
    cursor = db.users.find(
        {"$or": [{"name": regex}, {"email": regex}, {"mobile": regex}]},
        {"password": 0},
    ).limit(10)

    patients = []
    for u in cursor:
        u["_id"] = str(u["_id"])
        u.pop("reports", None)
        patients.append(u)

    return jsonify({"patients": patients}), 200


# ═══════════════════════════════════════════════
#  APPOINTMENTS  (receptionist books, doctor reads)
# ═══════════════════════════════════════════════

@hospital_bp.route("/appointments", methods=["POST"])
@require_role("receptionist")
def book_appointment():
    data = request.get_json()
    for field in ["patient_id", "appointment_date", "appointment_time"]:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    db = get_db()
    rec = db.receptionists.find_one({"_id": ObjectId(request.user_id)})
    if not rec:
        return jsonify({"error": "Receptionist not found"}), 404

    # Validate patient
    try:
        patient = db.users.find_one({"_id": ObjectId(data["patient_id"])}, {"password": 0})
    except Exception:
        return jsonify({"error": "Invalid patient_id"}), 400
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    appt = {
        "patient_id": data["patient_id"],
        "patient_name": patient.get("name", ""),
        "patient_email": patient.get("email", ""),
        "patient_mobile": patient.get("mobile", ""),
        "doctor_id": rec["doctor_id"],
        "receptionist_id": str(rec["_id"]),
        "appointment_date": data["appointment_date"],  # "YYYY-MM-DD"
        "appointment_time": data["appointment_time"],  # "HH:MM"
        "notes": data.get("notes", ""),
        "status": "scheduled",
        "created_at": datetime.utcnow(),
    }
    result = db.appointments.insert_one(appt)
    return jsonify({
        "message": f"Appointment booked for {patient.get('name')} ✅",
        "appointment_id": str(result.inserted_id),
    }), 201


@hospital_bp.route("/appointments/today", methods=["GET"])
@require_role("doctor")
def todays_appointments():
    db = get_db()
    today_str = date.today().isoformat()  # "YYYY-MM-DD"
    appts = list(db.appointments.find(
        {"doctor_id": request.user_id, "appointment_date": today_str}
    ).sort("appointment_time", 1))

    for a in appts:
        a["_id"] = str(a["_id"])
    return jsonify({"appointments": appts}), 200


@hospital_bp.route("/appointments/all-patients", methods=["GET"])
@require_role("doctor")
def all_patients():
    """All unique patients who ever had an appointment with this doctor."""
    db = get_db()
    appts = list(db.appointments.find(
        {"doctor_id": request.user_id},
        {"patient_id": 1, "patient_name": 1, "patient_email": 1, "patient_mobile": 1, "appointment_date": 1},
    ).sort("appointment_date", -1))

    seen = {}
    for a in appts:
        pid = a["patient_id"]
        if pid not in seen:
            seen[pid] = {
                "patient_id": pid,
                "patient_name": a.get("patient_name", ""),
                "patient_email": a.get("patient_email", ""),
                "patient_mobile": a.get("patient_mobile", ""),
                "last_visit": a.get("appointment_date", ""),
            }

    return jsonify({"patients": list(seen.values())}), 200


@hospital_bp.route("/receptionist/my-patients", methods=["GET"])
@require_role("receptionist")
def receptionist_my_patients():
    """All patients booked by this receptionist's doctor."""
    db = get_db()
    rec = db.receptionists.find_one({"_id": ObjectId(request.user_id)})
    appts = list(db.appointments.find(
        {"doctor_id": rec["doctor_id"]},
        {"patient_id": 1, "patient_name": 1, "patient_email": 1, "patient_mobile": 1, "appointment_date": 1, "appointment_time": 1, "status": 1},
    ).sort("appointment_date", -1))
    for a in appts:
        a["_id"] = str(a["_id"])
    return jsonify({"patients": appts}), 200


# ═══════════════════════════════════════════════
#  PRESCRIPTIONS
# ═══════════════════════════════════════════════

@hospital_bp.route("/prescriptions", methods=["POST"])
@require_role("doctor")
def write_prescription():
    data = request.get_json()
    for field in ["patient_id", "medicines"]:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400
    if not isinstance(data["medicines"], list) or len(data["medicines"]) == 0:
        return jsonify({"error": "At least one medicine is required"}), 400

    db = get_db()
    doctor = db.doctors.find_one({"_id": ObjectId(request.user_id)})

    # Validate patient
    try:
        patient = db.users.find_one({"_id": ObjectId(data["patient_id"])}, {"password": 0})
    except Exception:
        return jsonify({"error": "Invalid patient_id"}), 400
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Normalize medicines list
    medicines = []
    for m in data["medicines"]:
        if not m.get("name"):
            continue
        medicines.append({
            "name": m["name"],
            "dosage": m.get("dosage", ""),
            "frequency": m.get("frequency", ""),
            "duration": m.get("duration", ""),
            "instructions": m.get("instructions", ""),
        })

    if not medicines:
        return jsonify({"error": "At least one valid medicine is required"}), 400

    prescription = {
        "patient_id": data["patient_id"],
        "patient_name": patient.get("name", ""),
        "doctor_id": request.user_id,
        "doctor_name": doctor.get("name", "") if doctor else "",
        "doctor_specialization": doctor.get("specialization", "") if doctor else "",
        "medicines": medicines,
        "notes": data.get("notes", ""),
        "appointment_id": data.get("appointment_id", ""),
        "created_at": datetime.utcnow(),
    }
    result = db.prescriptions.insert_one(prescription)
    return jsonify({
        "message": f"Prescription saved for {patient.get('name')} ✅",
        "prescription_id": str(result.inserted_id),
    }), 201


@hospital_bp.route("/prescriptions/my", methods=["GET"])
@require_role("doctor")
def my_prescriptions():
    """All prescriptions written by this doctor."""
    db = get_db()
    prescriptions = list(db.prescriptions.find(
        {"doctor_id": request.user_id}
    ).sort("created_at", -1))
    for p in prescriptions:
        p["_id"] = str(p["_id"])
    return jsonify({"prescriptions": prescriptions}), 200


@hospital_bp.route("/prescriptions/patient/<patient_id>", methods=["GET"])
@require_role("doctor", "user")
def patient_prescriptions_for_doctor(patient_id):
    """Prescriptions for a specific patient (doctor view)."""
    db = get_db()
    prescriptions = list(db.prescriptions.find(
        {"patient_id": patient_id}
    ).sort("created_at", -1))
    for p in prescriptions:
        p["_id"] = str(p["_id"])
    return jsonify({"prescriptions": prescriptions}), 200


@hospital_bp.route("/prescriptions/me", methods=["GET"])
@require_auth
def my_prescriptions_user():
    """Prescriptions for the logged-in patient (user dashboard)."""
    db = get_db()
    prescriptions = list(db.prescriptions.find(
        {"patient_id": request.user_id}
    ).sort("created_at", -1))
    for p in prescriptions:
        p["_id"] = str(p["_id"])
    return jsonify({"prescriptions": prescriptions}), 200


# ═══════════════════════════════════════════════
#  BLOOD REPORT UPLOAD  (receptionist → patient)
# ═══════════════════════════════════════════════

@hospital_bp.route("/reports/upload", methods=["POST"])
@require_role("receptionist")
def receptionist_upload_report():
    """
    Receptionist uploads a blood report on behalf of a patient.
    The report is stored under the patient's user_id and goes through
    the same AI pipeline as a self-uploaded report.
    """
    patient_id = request.form.get("patient_id", "").strip()
    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    from services.text_extractor import (
        extract_text, allowed_file, extract_medical_metrics,
        detect_report_type, is_medical_report,
    )
    from services.bert_summarizer import summarize_medical_text, simplify_medical_summary, build_recommendations
    from models.report_model import create_report

    db = get_db()

    # Validate patient
    try:
        patient = db.users.find_one({"_id": ObjectId(patient_id)}, {"name": 1, "email": 1})
    except Exception:
        return jsonify({"error": "Invalid patient_id"}), 400
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if not allowed_file(file.filename, Config.ALLOWED_EXTENSIONS):
        return jsonify({"error": f"File type '{ext}' not allowed. Use PDF, JPG, PNG, JPEG"}), 400

    unique_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(Config.UPLOAD_FOLDER, unique_name)
    file.save(save_path)

    def _safe_remove(path):
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

    try:
        raw_text = extract_text(save_path, ext)
    except Exception as e:
        _safe_remove(save_path)
        return jsonify({"error": "ocr_failed", "message": str(e)}), 500

    if len(raw_text.strip()) < 20:
        _safe_remove(save_path)
        return jsonify({"error": "unreadable", "message": "Could not read text from this file."}), 400

    if not is_medical_report(raw_text):
        _safe_remove(save_path)
        return jsonify({"error": "out_of_knowledge_base", "message": "This file does not appear to be a medical report."}), 422

    try:
        metrics = extract_medical_metrics(raw_text)
        report_type = detect_report_type(raw_text)
    except Exception as e:
        _safe_remove(save_path)
        return jsonify({"error": "metrics_failed", "message": str(e)}), 500

    try:
        summary_raw = summarize_medical_text(raw_text)
        summary = simplify_medical_summary(summary_raw, metrics)
        recommendations = build_recommendations(metrics)
    except Exception:
        summary = "Summary could not be generated."
        recommendations = []

    try:
        report_id = create_report(patient_id, {
            "filename": unique_name,
            "original_name": secure_filename(file.filename),
            "file_type": ext,
            "file_path": save_path,
            "raw_text": raw_text,
            "summary": summary,
            "metrics": metrics,
            "report_type": report_type,
            "recommendations": recommendations,
            "uploaded_by": "receptionist",
        })
    except Exception as e:
        _safe_remove(save_path)
        return jsonify({"error": "db_error", "message": str(e)}), 500

    return jsonify({
        "message": f"Report uploaded and analyzed for {patient.get('name', 'patient')} ✅",
        "report_id": report_id,
        "report_type": report_type,
        "summary": summary,
        "metrics": metrics,
        "recommendations": recommendations,
    }), 201

# ═══════════════════════════════════════════════
#  DEMO SEED  — creates demo accounts if they don't exist
# ═══════════════════════════════════════════════

@hospital_bp.route("/demo/seed", methods=["POST"])
def seed_demo():
    """Creates demo doctor and receptionist accounts for testing."""
    db = get_db()

    # Demo Doctor
    demo_email_doc = "demo.doctor@ragnosis.com"
    demo_pw_doc = "demo1234"
    if not db.doctors.find_one({"email": demo_email_doc}):
        res = db.doctors.insert_one({
            "name": "Dr. Demo Doctor",
            "email": demo_email_doc,
            "password": _hash(demo_pw_doc),
            "specialization": "General Physician",
            "hospital": "RAGnosis Demo Hospital",
            "created_at": datetime.utcnow(),
        })
        doctor_id = str(res.inserted_id)
    else:
        doc = db.doctors.find_one({"email": demo_email_doc})
        doctor_id = str(doc["_id"])

    # Demo Receptionist  
    demo_email_rec = "demo.receptionist@ragnosis.com"
    demo_pw_rec = "demo1234"
    if not db.receptionists.find_one({"email": demo_email_rec}):
        db.receptionists.insert_one({
            "name": "Demo Receptionist",
            "email": demo_email_rec,
            "password": _hash(demo_pw_rec),
            "doctor_id": doctor_id,
            "created_at": datetime.utcnow(),
        })

    return jsonify({
        "message": "Demo accounts ready! ✅",
        "doctor": {"email": demo_email_doc, "password": demo_pw_doc, "doctor_id": doctor_id},
        "receptionist": {"email": demo_email_rec, "password": demo_pw_rec, "linked_doctor_id": doctor_id},
    }), 200


@hospital_bp.route("/doctor/id", methods=["GET"])
@require_role("doctor")
def get_doctor_id():
    """Returns the logged-in doctor's ID (used when setting up a receptionist)."""
    db = get_db()
    doc = db.doctors.find_one({"_id": ObjectId(request.user_id)}, {"_id": 1, "name": 1})
    if not doc:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"doctor_id": str(doc["_id"]), "name": doc["name"]}), 200
