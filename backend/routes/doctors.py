"""
Doctors API routes — CRUD + search for the doctors collection.
"""
from flask import Blueprint, request, jsonify
from models.doctor_model import get_all_doctors, get_doctor_by_id, add_doctor, delete_doctor

doctors_bp = Blueprint("doctors", __name__)


@doctors_bp.route("/", methods=["GET"])
def list_doctors():
    """List all doctors, optionally filtered by city or specialization."""
    city = request.args.get("city")
    specialization = request.args.get("specialization")
    doctors = get_all_doctors(city=city, specialization=specialization)
    return jsonify({"doctors": doctors, "count": len(doctors)}), 200


@doctors_bp.route("/<doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    doc = get_doctor_by_id(doctor_id)
    if not doc:
        return jsonify({"error": "Doctor not found"}), 404
    return jsonify(doc), 200


@doctors_bp.route("/", methods=["POST"])
def create_doctor():
    """Add a new doctor (admin use)."""
    data = request.get_json()
    required = ["name", "specialization", "hospital", "city", "contact"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    doc_id = add_doctor(data)
    return jsonify({"message": "Doctor added", "doctor_id": doc_id}), 201


@doctors_bp.route("/<doctor_id>", methods=["DELETE"])
def remove_doctor(doctor_id):
    delete_doctor(doctor_id)
    return jsonify({"message": "Doctor removed"}), 200
