"""
Project: LifeLine Connect (Blood Bank Network)
Component: Donor Management Controller
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.donor_model import (
    get_all_donors, get_donor_by_id, get_donor_donations,
    check_donor_eligibility, register_donor
)

donor_bp = Blueprint("donors", __name__, url_prefix="/donors")

@donor_bp.route("/")
def index():
    blood_group = request.args.get("blood_group", "")
    eligibility = request.args.get("eligibility", "")
    search = request.args.get("search", "")

    donors = get_all_donors(
        blood_group=blood_group,
        eligibility=eligibility,
        search=search
    )
    return render_template(
        "donors/list.html",
        donors=donors,
        selected_bg=blood_group,
        selected_el=eligibility,
        search=search
    )

@donor_bp.route("/<int:donor_id>")
def profile(donor_id: int):
    donor = get_donor_by_id(donor_id)
    if not donor:
        flash("Donor record not found.", "danger")
        return redirect(url_for("donors.index"))

    donations = get_donor_donations(donor_id)
    eligibility_msg = check_donor_eligibility(donor_id)

    return render_template(
        "donors/profile.html",
        donor=donor,
        donations=donations,
        eligibility_msg=eligibility_msg
    )

@donor_bp.route("/<int:donor_id>/check-eligibility", methods=["POST"])
def check_eligibility_api(donor_id: int):
    status_msg = check_donor_eligibility(donor_id)
    is_eligible = status_msg == "ELIGIBLE"
    return jsonify({"eligible": is_eligible, "message": status_msg})

@donor_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "date_of_birth": request.form.get("date_of_birth", "").strip(),
            "gender": request.form.get("gender", "MALE"),
            "blood_group": request.form.get("blood_group", "O+"),
            "rh_factor": request.form.get("rh_factor", "POSITIVE"),
            "weight_kg": request.form.get("weight_kg", 60),
            "hemoglobin_level": request.form.get("hemoglobin_level", 14.0),
            "address": request.form.get("address", ""),
            "city": request.form.get("city", "").strip()
        }

        try:
            donor_id, message = register_donor(data)
            if donor_id:
                flash(f"Donor successfully registered! Allocated Donor ID #{donor_id}.", "success")
                return redirect(url_for("donors.profile", donor_id=donor_id))
            else:
                flash(f"Registration Error: {message}", "danger")
        except Exception as e:
            flash(f"System Error: {e}", "danger")

    return render_template("donors/register.html")
