from flask import Flask, request
from flask_cors import CORS
import os
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Create upload folder
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    # CORS - Configure allowed origins
    allowed_origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5000",
    ]
    
    # Add frontend URLs from environment variables
    if os.getenv("FRONTEND_URL"):
        allowed_origins.append(os.getenv("FRONTEND_URL"))
    
    # Add Vercel frontend domain (you'll set this in production)
    # Example: https://your-app.vercel.app
    if os.getenv("VERCEL_FRONTEND_URL"):
        allowed_origins.append(os.getenv("VERCEL_FRONTEND_URL"))
    
    # For local development, allow requests from any local IP
    if os.getenv("ALLOW_ALL_ORIGINS") == "true":
        allowed_origins = "*"
    
    CORS(app,
         origins=allowed_origins,
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])

    # Log all incoming requests
    @app.before_request
    def log_request():
        print(f"\n[REQUEST] {request.method} {request.path}")
        print(f"[REQUEST] From: {request.remote_addr}")
        print(f"[REQUEST] Origin: {request.headers.get('Origin', 'None')}")
        print(f"[REQUEST] Headers: Content-Type={request.content_type}, Auth={request.headers.get('Authorization', 'None')}")

    # Register blueprints
    from routes.auth import auth_bp
    from routes.reports import reports_bp
    from routes.chatbot import chatbot_bp
    from routes.reminders import reminders_bp
    from routes.hospital import hospital_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(chatbot_bp, url_prefix="/api/chat")
    app.register_blueprint(reminders_bp, url_prefix="/api/reminders")
    app.register_blueprint(hospital_bp, url_prefix="/api/hospital")

    from routes.doctors import doctors_bp
    app.register_blueprint(doctors_bp, url_prefix="/api/doctors")

    # Seed doctors collection on first run
    from models.doctor_model import seed_doctors
    with app.app_context():
        seed_doctors()

    @app.route("/api/health")
    def health():
        print("[HEALTH] Health check requested")
        from services.text_extractor import get_tesseract_status
        tesseract_status = get_tesseract_status()
        return {
            "status": "ok",
            "message": "RAGnosis API is running",
            "tesseract": tesseract_status
        }

    @app.route("/api/diagnostics/tesseract")
    def tesseract_diagnostic():
        """Diagnostic endpoint to check Tesseract installation and configuration."""
        import subprocess
        from services.text_extractor import get_tesseract_status

        status = get_tesseract_status()
        details = {"status": status}

        # Try to run Tesseract version command if found
        if status.get("tesseract_path"):
            try:
                result = subprocess.run([status["tesseract_path"], "--version"], capture_output=True, text=True, timeout=5)
                details["version_check"] = "OK" if result.returncode == 0 else "FAILED"
                details["version_output"] = result.stdout.split('\n')[0] if result.returncode == 0 else result.stderr[:100]
            except Exception as e:
                details["version_check"] = f"ERROR: {str(e)}"
        else:
            details["version_check"] = "TESSERACT_NOT_FOUND"

        return {"diagnostic": details}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    print("[CORS] Allowing cross-origin requests from: http://localhost:5173, http://localhost:3000")
    print("[SERVER] Starting on 0.0.0.0:5000 (accessible on LAN at 172.20.10.7:5000)")
    app.run(
        host='0.0.0.0',      # Listen on all interfaces so phone can connect over WiFi
        debug=True,
        port=5000,
        threaded=True,       # Allow concurrent requests (fixes ECONNRESET on long uploads)
        use_reloader=False,  # Prevent ML models from loading twice on startup
    )
