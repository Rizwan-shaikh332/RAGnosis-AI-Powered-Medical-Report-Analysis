from datetime import datetime
from database import get_db
from bson import ObjectId


def create_reminder(user_id: str, data: dict) -> str:
    db = get_db()
    reminder = {
        "user_id": user_id,
        "medicine_name": data["medicine_name"],
        "dosage": data.get("dosage", ""),
        "times": data.get("times", []),        # list of {"hour": int, "minute": int, "label": str}
        "frequency": data.get("frequency", "daily"),
        "notes": data.get("notes", ""),
        "active": True,
        "created_at": datetime.utcnow(),
    }
    result = db.reminders.insert_one(reminder)
    return str(result.inserted_id)


def get_reminders_by_user(user_id: str):
    db = get_db()
    reminders = list(db.reminders.find({"user_id": user_id}).sort("created_at", -1))
    for r in reminders:
        r["_id"] = str(r["_id"])
        r["created_at"] = r["created_at"].isoformat() if r.get("created_at") else ""
    return reminders


def get_reminder_by_id(reminder_id: str):
    db = get_db()
    r = db.reminders.find_one({"_id": ObjectId(reminder_id)})
    if r:
        r["_id"] = str(r["_id"])
    return r


def delete_reminder(reminder_id: str):
    db = get_db()
    db.reminders.delete_one({"_id": ObjectId(reminder_id)})


def update_reminder(reminder_id: str, data: dict):
    db = get_db()
    update_fields = {}
    for key in ["medicine_name", "dosage", "times", "frequency", "notes", "active"]:
        if key in data:
            update_fields[key] = data[key]
    db.reminders.update_one(
        {"_id": ObjectId(reminder_id)},
        {"$set": update_fields}
    )
