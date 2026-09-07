"""
Project: LifeLine Connect (Blood Bank Network)
Component: Emergency Appeals & Community Q&A Controller (MongoDB)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.nosql_model import (
    search_emergency_appeals, create_emergency_appeal, add_appeal_qa
)
from app.models.hospital_model import get_all_hospitals

appeal_bp = Blueprint("appeals", __name__, url_prefix="/appeals")

@appeal_bp.route("/")
def index():
    bg = request.args.get("blood_group", "")
    keyword = request.args.get("keyword", "")
    status = request.args.get("status", "")

    # Executes PyMongo search with regex/text matching
    appeals = search_emergency_appeals(
        blood_group=bg,
        keyword=keyword,
        status=status
    )

    return render_template(
        "appeals/list.html",
        appeals=appeals,
        selected_bg=bg,
        keyword=keyword,
        selected_status=status
    )

@appeal_bp.route("/new", methods=["GET", "POST"])
def new_appeal():
    if request.method == "POST":
        data = {
            "hospital_name": request.form.get("hospital_name", "").strip(),
            "blood_group": request.form.get("blood_group", "O+"),
            "urgency": request.form.get("urgency", "CRITICAL"),
            "units_required": request.form.get("units_required", 2),
            "patient_condition": request.form.get("patient_condition", "").strip(),
            "city": request.form.get("city", "").strip(),
            "contact_phone": request.form.get("contact_phone", "").strip()
        }

        try:
            appeal_id = create_emergency_appeal(data)
            flash(f"Emergency Broadcast [{appeal_id}] launched across LifeLine network channels!", "success")
            return redirect(url_for("appeals.index"))
        except Exception as e:
            flash(f"Appeal Broadcast Error: {e}", "danger")

    hospitals = get_all_hospitals()
    return render_template("appeals/new_appeal.html", hospitals=hospitals)

@appeal_bp.route("/<appeal_id>/qa", methods=["POST"])
def post_qa(appeal_id: str):
    qa_data = {
        "user_name": request.form.get("user_name", "Anonymous Donor"),
        "user_type": request.form.get("user_type", "Community Member"),
        "message": request.form.get("message", "").strip(),
        "reply": request.form.get("reply", "").strip()
    }

    if not qa_data["message"]:
        flash("Message cannot be empty.", "warning")
        return redirect(url_for("appeals.index"))

    try:
        success = add_appeal_qa(appeal_id, qa_data)
        if success:
            flash("Your question / update was posted to the emergency thread.", "success")
    except Exception as e:
        flash(f"Error posting comment: {e}", "danger")

    return redirect(url_for("appeals.index"))
