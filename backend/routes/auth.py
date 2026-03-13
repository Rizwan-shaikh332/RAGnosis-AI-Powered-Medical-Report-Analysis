from flask import Blueprint, request, jsonify
from models.user_model import create_user, find_user_by_email, find_user_by_mobile, verify_password
from utils.jwt_helper import generate_token
import re

auth_bp = Blueprint("auth", __name__)

def is_valid_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)

def is_valid_mobile(mobile):
    return re.match(r"^\d{10}$", mobile)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required = ["name", "email", "mobile", "password", "age", "height_inches", "gender"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email address"}), 400
    if not is_valid_mobile(str(data["mobile"])):
        return jsonify({"error": "Mobile number must be 10 digits"}), 400
    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if find_user_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 409
    if find_user_by_mobile(str(data["mobile"])):
        return jsonify({"error": "Mobile number already registered"}), 409

    user_id = create_user(data)
    token = generate_token(user_id)
    return jsonify({
        "message": "Registration successful! Welcome to RAGnosis 🩺",
        "token": token,
        "user": {
            "id": user_id,
            "name": data["name"],
            "email": data["email"]
        }
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    identifier = data.get("identifier", "").strip()  # email or mobile
    password = data.get("password", "")

    if not identifier or not password:
        return jsonify({"error": "Identifier and password are required"}), 400

    # Try email first, then mobile
    user = find_user_by_email(identifier)
    if not user:
        user = find_user_by_mobile(identifier)
    if not user:
        return jsonify({"error": "No account found with this email or mobile"}), 404

    if not verify_password(password, user["password"]):
        return jsonify({"error": "Incorrect password"}), 401

    token = generate_token(str(user["_id"]))
    return jsonify({
        "message": f"Welcome back, {user['name']}! 👋",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "mobile": user.get("mobile", ""),
            "age": user.get("age"),
            "gender": user.get("gender", ""),
        }
    }), 200

@auth_bp.route("/me", methods=["GET"])
def me():
    from utils.jwt_helper import decode_token
    from models.user_model import find_user_by_id
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401
    token = auth_header.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        return jsonify({"error": "Invalid or expired token"}), 401
    user = find_user_by_id(payload["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["_id"] = str(user["_id"])
    user.pop("password", None)
    return jsonify(user), 200
