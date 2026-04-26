from datetime import datetime
from database import get_db
from bson import ObjectId

def create_report(user_id: str, data: dict) -> str:
    db = get_db()
    report = {
        "user_id": user_id,
        "filename": data["filename"],
        "original_name": data["original_name"],
        "file_type": data["file_type"],
        "file_path": data["file_path"],
        "raw_text": data.get("raw_text", ""),
        "summary": data.get("summary", ""),
        "entities": data.get("entities", []),
        "metrics": data.get("metrics", {}),    # extracted health numbers
        "recommendations": data.get("recommendations", []),  # customized health tips
        "report_type": data.get("report_type", "General"),
        "is_critical": data.get("is_critical", False),
        "suggested_doctors": data.get("suggested_doctors", []),
        "specialist_advice": data.get("specialist_advice", ""),
        "uploaded_at": datetime.utcnow(),
        "status": "processed"
    }
    result = db.reports.insert_one(report)
    # Also push report id to user doc
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"reports": str(result.inserted_id)}}
    )
    return str(result.inserted_id)

def get_reports_by_user(user_id: str):
    db = get_db()
    reports = list(db.reports.find({"user_id": user_id}).sort("uploaded_at", -1))
    for r in reports:
        r["_id"] = str(r["_id"])
    return reports

def get_report_by_id(report_id: str):
    db = get_db()
    r = db.reports.find_one({"_id": ObjectId(report_id)})
    if r:
        r["_id"] = str(r["_id"])
    return r

def update_report_metrics(report_id: str, metrics: dict, summary: str, recommendations: list, report_type: str):
    """Update an existing report's metrics, summary, recommendations, and type in MongoDB."""
    db = get_db()
    db.reports.update_one(
        {"_id": ObjectId(report_id)},
        {"$set": {
            "metrics": metrics,
            "summary": summary,
            "recommendations": recommendations,
            "report_type": report_type,
        }},
    )

