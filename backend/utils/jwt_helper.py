import jwt
from datetime import datetime, timedelta
from config import Config

def generate_token(user_id: str, role: str = "user") -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRY_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")

def decode_token(token: str):
    try:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to protect routes with JWT auth."""
    from functools import wraps
    from flask import request, jsonify
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization token required"}), 401
        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        request.user_id = payload["user_id"]
        request.user_role = payload.get("role", "user")
        return f(*args, **kwargs)
    return decorated

def require_role(*roles):
    """Decorator to protect routes requiring specific roles (doctor, receptionist)."""
    from functools import wraps
    from flask import request, jsonify
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Authorization token required"}), 401
            token = auth_header.split(" ")[1]
            payload = decode_token(token)
            if not payload:
                return jsonify({"error": "Invalid or expired token"}), 401
            role = payload.get("role", "user")
            if role not in roles:
                return jsonify({"error": f"Access denied. Required role: {', '.join(roles)}"}), 403
            request.user_id = payload["user_id"]
            request.user_role = role
            return f(*args, **kwargs)
        return decorated
    return decorator
