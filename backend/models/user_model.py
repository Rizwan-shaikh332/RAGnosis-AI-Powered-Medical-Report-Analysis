from datetime import datetime
from database import get_db
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_user(data: dict) -> str:
    db = get_db()
    user = {
        "name": data["name"],
        "email": data["email"].lower(),
        "mobile": data.get("mobile", ""),
        "password": hash_password(data["password"]),
        "age": data.get("age"),
        "height_inches": data.get("height_inches"),
        "weight_kg": data.get("weight_kg"),
        "blood_pressure": data.get("blood_pressure", ""),  # optional
        "blood_group": data.get("blood_group", ""),        # optional
        "gender": data.get("gender", ""),
        "created_at": datetime.utcnow(),
        "reports": []
    }
    result = db.users.insert_one(user)
    return str(result.inserted_id)

def find_user_by_email(email: str):
    db = get_db()
    return db.users.find_one({"email": email.lower()})

def find_user_by_mobile(mobile: str):
    db = get_db()
    return db.users.find_one({"mobile": mobile})

def find_user_by_id(user_id: str):
    from bson import ObjectId
    db = get_db()
    return db.users.find_one({"_id": ObjectId(user_id)})
