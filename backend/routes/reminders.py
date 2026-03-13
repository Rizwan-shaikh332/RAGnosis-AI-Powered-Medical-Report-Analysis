from flask import Blueprint, request, jsonify
from utils.jwt_helper import require_auth
from models.reminder_model import (
    create_reminder, get_reminders_by_user,
    get_reminder_by_id, delete_reminder, update_reminder
)

reminders_bp = Blueprint("reminders", __name__)


@reminders_bp.route("/", methods=["GET"])
@require_auth
def list_reminders():
    """Get all medicine reminders for the logged-in user."""
    reminders = get_reminders_by_user(request.user_id)
    return jsonify({"reminders": reminders}), 200


@reminders_bp.route("/", methods=["POST"])
@require_auth
def add_reminder():
    """Create a new medicine reminder."""
    data = request.get_json()
    if not data.get("medicine_name"):
        return jsonify({"error": "medicine_name is required"}), 400
    if not data.get("times") or not isinstance(data["times"], list) or len(data["times"]) == 0:
        return jsonify({"error": "At least one time is required"}), 400

    reminder_id = create_reminder(request.user_id, data)
    return jsonify({
        "message": "Medicine reminder added successfully 💊",
        "reminder_id": reminder_id
    }), 201


@reminders_bp.route("/<reminder_id>", methods=["DELETE"])
@require_auth
def remove_reminder(reminder_id):
    """Delete a medicine reminder."""
    reminder = get_reminder_by_id(reminder_id)
    if not reminder or reminder["user_id"] != request.user_id:
        return jsonify({"error": "Reminder not found"}), 404
    delete_reminder(reminder_id)
    return jsonify({"message": "Reminder deleted"}), 200


@reminders_bp.route("/<reminder_id>", methods=["PUT"])
@require_auth
def update_reminder_route(reminder_id):
    """Update a reminder (e.g., toggle active, change time)."""
    reminder = get_reminder_by_id(reminder_id)
    if not reminder or reminder["user_id"] != request.user_id:
        return jsonify({"error": "Reminder not found"}), 404
    data = request.get_json()
    update_reminder(reminder_id, data)
    return jsonify({"message": "Reminder updated"}), 200
