"""
Project: LifeLine Connect (Blood Bank Network)
Component: Camp Management & Reviews Controller (Oracle + MongoDB)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.camp_model import get_all_camps, get_camp_by_id, get_camp_staff, create_camp
from app.models.nosql_model import get_camp_feedback, get_campaign_media, get_top_rated_camps, add_camp_feedback

camp_bp = Blueprint("camps", __name__, url_prefix="/camps")

@camp_bp.route("/")
def index():
    status = request.args.get("status", "")
    camps = get_all_camps(status=status)
    return render_template("camps/list.html", camps=camps, selected_status=status)

@camp_bp.route("/<int:camp_id>")
def detail(camp_id: int):
    camp = get_camp_by_id(camp_id)
    if not camp:
        flash("Camp record not found.", "danger")
        return redirect(url_for("camps.index"))

    # Oracle Relational Data
    staff_assignments = get_camp_staff(camp_id)

    # MongoDB Unstructured Data
    feedback_reviews = get_camp_feedback(camp_id)
    campaign_media = get_campaign_media(camp_id)

    # Calculate average feedback score if reviews exist
    avg_score = 0
    if feedback_reviews:
        scores = [f["ratings"]["overall_score"] for f in feedback_reviews if "ratings" in f]
        if scores:
            avg_score = round(sum(scores) / len(scores), 1)

    return render_template(
        "camps/detail.html",
        camp=camp,
        staff=staff_assignments,
        feedback=feedback_reviews,
        media=campaign_media,
        avg_score=avg_score
    )

@camp_bp.route("/<int:camp_id>/feedback", methods=["POST"])
def submit_feedback(camp_id: int):
    camp = get_camp_by_id(camp_id)
    if not camp:
        flash("Camp not found.", "danger")
        return redirect(url_for("camps.index"))

    data = {
        "camp_id": camp_id,
        "donor_id": request.form.get("donor_id", 0),
        "donor_name": request.form.get("donor_name", "Anonymous Donor"),
        "blood_group": request.form.get("blood_group", "O+"),
        "overall_score": float(request.form.get("overall_score", 5)),
        "registration_speed": float(request.form.get("registration_speed", 5)),
        "staff_friendliness": float(request.form.get("staff_friendliness", 5)),
        "hygiene_and_safety": float(request.form.get("hygiene_and_safety", 5)),
        "refreshment_quality": float(request.form.get("refreshment_quality", 5)),
        "feedback_text": request.form.get("feedback_text", ""),
        "recommend_to_others": request.form.get("recommend_to_others") == "on"
    }

    try:
        feedback_id = add_camp_feedback(data)
        flash("Thank you! Your feedback and ratings were logged into MongoDB.", "success")
    except Exception as e:
        flash(f"Feedback Submission Error: {e}", "danger")

    return redirect(url_for("camps.detail", camp_id=camp_id))

@camp_bp.route("/top-rated")
def top_rated():
    # MongoDB Aggregation Pipeline query
    top_camps_stats = get_top_rated_camps(min_reviews=1)
    
    # Enrich with Oracle camp info
    enriched = []
    for stat in top_camps_stats:
        camp_meta = get_camp_by_id(stat["camp_id"])
        if camp_meta:
            combined = {**stat, **camp_meta}
            enriched.append(combined)

    return render_template("camps/top_rated.html", top_camps=enriched)
