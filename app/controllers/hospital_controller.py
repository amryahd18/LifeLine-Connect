"""
Project: LifeLine Connect (Blood Bank Network)
Component: Hospital & Requisitions Controller (Oracle Database)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.hospital_model import (
    get_all_hospitals, get_blood_requests, create_blood_request,
    fulfill_blood_request, get_dispatch_history
)

hospital_bp = Blueprint("hospitals", __name__, url_prefix="/hospitals")

@hospital_bp.route("/")
def index():
    hospitals = get_all_hospitals()
    return render_template("hospitals/list.html", hospitals=hospitals)

@hospital_bp.route("/requests")
def requests():
    st = request.args.get("status", "")
    urg = request.args.get("urgency", "")

    req_list = get_blood_requests(status=st, urgency=urg)
    return render_template(
        "hospitals/requests.html",
        requests=req_list,
        selected_st=st,
        selected_urg=urg
    )

@hospital_bp.route("/requests/new", methods=["GET", "POST"])
def new_request():
    if request.method == "POST":
        data = {
            "hospital_id": request.form.get("hospital_id"),
            "blood_group": request.form.get("blood_group", "O+"),
            "component_type": request.form.get("component_type", "WHOLE_BLOOD"),
            "units_requested": request.form.get("units_requested", 1),
            "urgency_level": request.form.get("urgency_level", "NORMAL"),
            "required_by_date": request.form.get("required_by_date"),
            "notes": request.form.get("notes", "")
        }

        try:
            create_blood_request(data)
            flash("Blood Requisition submitted successfully! Logged for FEFO cross-matching.", "success")
            return redirect(url_for("hospitals.requests"))
        except Exception as e:
            flash(f"Submission Error: {e}", "danger")

    hospitals = get_all_hospitals()
    return render_template("hospitals/new_request.html", hospitals=hospitals)

@hospital_bp.route("/requests/<int:request_id>/fulfill", methods=["POST"])
def fulfill(request_id: int):
    transporter = request.form.get("transporter_name", "RapidMed Emergency Logistics")
    try:
        units, stat, msg = fulfill_blood_request(
            request_id=request_id,
            staff_id=3006,
            transporter=transporter
        )
        if units > 0:
            flash(f"FEFO Fulfillment Success: Dispatched {units} unit(s). Request status: {stat}.", "success")
        else:
            flash(f"Fulfillment Notice: {msg}", "warning")
    except Exception as e:
        flash(f"PL/SQL Fulfillment Error: {e}", "danger")

    return redirect(url_for("hospitals.requests"))

@hospital_bp.route("/dispatches")
def dispatches():
    dispatch_list = get_dispatch_history()
    return render_template("hospitals/dispatches.html", dispatches=dispatch_list)
