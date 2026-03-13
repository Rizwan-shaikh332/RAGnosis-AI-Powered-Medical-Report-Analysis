from flask import Blueprint, request, jsonify
from utils.jwt_helper import require_auth
from services.groq_service import get_chatbot_response
from models.report_model import get_report_by_id

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/", methods=["POST"])
@require_auth
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    report_id = data.get("report_id", None)
    chat_history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Retrieve report context if provided
    report_text = ""
    if report_id:
        report = get_report_by_id(report_id)
        if report and report.get("user_id") == request.user_id:
            report_text = report.get("raw_text", "")

    response = get_chatbot_response(user_message, report_text, chat_history)

    return jsonify({
        "response": response,
        "report_id": report_id
    }), 200

@chatbot_bp.route("/suggestions", methods=["GET"])
@require_auth
def get_suggestions():
    """Return helpful default questions for the chatbot."""
    suggestions = [
        "What does my hemoglobin level mean?",
        "Is my blood sugar level normal?",
        "Explain my cholesterol results in simple terms",
        "What should I eat to improve my blood count?",
        "Are there any abnormal values in my report?",
        "What is the significance of my WBC count?",
        "How can I improve my kidney function?",
        "What does my TSH level indicate about my thyroid?",
    ]
    return jsonify({"suggestions": suggestions}), 200
