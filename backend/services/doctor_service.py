"""
Doctor suggestion service — queries MongoDB doctors collection
and maps report types to specialist categories.
"""
from models.doctor_model import get_all_doctors

# Specialist mapping for ALL report types
# Each entry: specializations to query, plus a human-readable advice line
SPECIALIST_MAPPING = {
    "Blood / CBC Report": {
        "specs": ["Hematologist", "General Physician"],
        "advice": "Your CBC report indicates you should consult a Hematologist (MBBS, MD/DM in Hematology) for blood-related conditions."
    },
    "Diabetes / Glucose Report": {
        "specs": ["Endocrinologist", "Diabetologist", "General Physician"],
        "advice": "Your Glucose/Diabetes report indicates you should consult an Endocrinologist or Diabetologist (MBBS, MD/DM in Endocrinology) for sugar and hormonal management."
    },
    "Lipid Panel Report": {
        "specs": ["Cardiologist", "General Physician"],
        "advice": "Your Lipid Panel report indicates you should consult a Cardiologist (MBBS, MD/DM in Cardiology) for heart and cholesterol management."
    },
    "Kidney Function Report": {
        "specs": ["Nephrologist", "General Physician"],
        "advice": "Your Kidney Function report indicates you should consult a Nephrologist (MBBS, MD/DM in Nephrology) for kidney-related conditions."
    },
    "Liver Function Report": {
        "specs": ["Hepatologist", "Gastroenterologist", "General Physician"],
        "advice": "Your Liver Function report indicates you should consult a Hepatologist or Gastroenterologist (MBBS, MD/DM in Gastroenterology) for liver health."
    },
    "Thyroid Report": {
        "specs": ["Endocrinologist", "General Physician"],
        "advice": "Your Thyroid report indicates you should consult an Endocrinologist (MBBS, MD/DM in Endocrinology) for thyroid hormone management."
    },
    "Radiology Report": {
        "specs": ["Radiologist", "General Physician"],
        "advice": "Your Radiology report indicates you should consult a Radiologist (MBBS, MD in Radiology) for imaging interpretation."
    },
    "Urine Analysis Report": {
        "specs": ["Nephrologist", "Urologist", "General Physician"],
        "advice": "Your Urine Analysis report indicates you should consult a Nephrologist or Urologist (MBBS, MS/MCh in Urology) for urinary tract conditions."
    },
    "Vitamin / Nutrition Report": {
        "specs": ["General Physician", "Endocrinologist"],
        "advice": "Your Vitamin/Nutrition report indicates you should consult a General Physician or Endocrinologist (MBBS, MD) for nutritional deficiency management."
    },
    "Bone / Orthopedic Report": {
        "specs": ["Orthopedic Surgeon", "General Physician"],
        "advice": "Your Bone/Orthopedic report indicates you should consult an Orthopedic Surgeon (MBBS, MS in Orthopedics) for bone and joint conditions."
    },
    "Skin / Dermatology Report": {
        "specs": ["Dermatologist", "General Physician"],
        "advice": "Your Skin/Dermatology report indicates you should consult a Dermatologist (MBBS, MD in Dermatology) for skin-related conditions."
    },
    "Cardiac / ECG Report": {
        "specs": ["Cardiologist", "General Physician"],
        "advice": "Your Cardiac/ECG report indicates you should consult a Cardiologist (MBBS, MD/DM in Cardiology) for heart-related conditions."
    },
    "Pulmonary Report": {
        "specs": ["Pulmonologist", "General Physician"],
        "advice": "Your Pulmonary report indicates you should consult a Pulmonologist (MBBS, MD in Pulmonary Medicine) for lung and respiratory conditions."
    },
    "General Medical Report": {
        "specs": ["General Physician"],
        "advice": "Your report indicates you should consult a General Physician (MBBS, MD in General Medicine) for comprehensive evaluation."
    },
}


def get_specialist_advice(report_type):
    """Get the specialist recommendation text for a given report type."""
    mapping = SPECIALIST_MAPPING.get(report_type, SPECIALIST_MAPPING["General Medical Report"])
    return mapping["advice"]


def get_suggested_doctors(report_type, city="Pune"):
    """
    Suggest doctors based on report type and city.
    Queries the MongoDB doctors collection for matching specialists.
    """
    mapping = SPECIALIST_MAPPING.get(report_type, SPECIALIST_MAPPING["General Medical Report"])
    specializations = mapping["specs"]

    suggested = []
    for spec in specializations:
        docs = get_all_doctors(city=city, specialization=spec)
        suggested.extend(docs)

    # Remove duplicates (in case a doc appears in multiple queries)
    seen_ids = set()
    unique = []
    for d in suggested:
        if d["_id"] not in seen_ids:
            seen_ids.add(d["_id"])
            unique.append(d)

    return unique
