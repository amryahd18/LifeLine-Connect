"""
Project: LifeLine Connect (Blood Bank Network)
Component: Inventory & Donation Collection Controller (Oracle Database)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.inventory_model import (
    get_inventory_summary, get_all_inventory_units, record_donation
)
from app.models.report_model import get_report2_inventory_expiring
from app.models.donor_model import get_all_donors
from app.models.camp_model import get_all_camps

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")

@inventory_bp.route("/")
def stock():
    bg = request.args.get("blood_group", "")
    comp = request.args.get("component_type", "")
    st = request.args.get("status", "")

    summary = get_inventory_summary()
    units = get_all_inventory_units(blood_group=bg, component=comp, status=st)

    return render_template(
        "inventory/stock.html",
        summary=summary,
        units=units,
        selected_bg=bg,
        selected_comp=comp,
        selected_st=st
    )

@inventory_bp.route("/expiring")
def expiring():
    days = request.args.get("days", 7)
    try:
        days = int(days)
    except ValueError:
        days = 7

    # Calls PKG_LIFELINE_REPORTS.fn_report_inventory_expiring in PL/SQL
    expiring_units = get_report2_inventory_expiring(days_ahead=days)

    critical_count = sum(1 for u in expiring_units if u.get("freshness_category") == "CRITICAL_EXPIRING_SOON")
    expired_count = sum(1 for u in expiring_units if u.get("freshness_category") == "EXPIRED")

    return render_template(
        "inventory/expiring.html",
        units=expiring_units,
        days=days,
        critical_count=critical_count,
        expired_count=expired_count
    )

@inventory_bp.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        data = {
            "donor_id": request.form.get("donor_id"),
            "camp_id": request.form.get("camp_id"),
            "blood_pressure_sys": request.form.get("blood_pressure_sys", 120),
            "blood_pressure_dia": request.form.get("blood_pressure_dia", 80),
            "pulse_rate": request.form.get("pulse_rate", 72),
            "hemoglobin_reading": request.form.get("hemoglobin_reading", 14.5),
            "component_type": request.form.get("component_type", "WHOLE_BLOOD"),
            "storage_location": request.form.get("storage_location", "Fridge-A / Shelf-1"),
            "notes": request.form.get("notes", "Clean donation collection.")
        }

        try:
            don_id, unit_id, msg = record_donation(data)
            if don_id and unit_id:
                flash(f"Donation #{don_id} recorded! New Blood Inventory Unit #{unit_id} created with FEFO tracking.", "success")
                return redirect(url_for("inventory.stock"))
            else:
                flash(f"Donation Processing Error: {msg}", "danger")
        except Exception as e:
            flash(f"Screening or Database Exception: {e}", "danger")

    donors = get_all_donors(eligibility="ELIGIBLE")
    camps = get_all_camps()
    return render_template("inventory/donate.html", donors=donors, camps=camps)
