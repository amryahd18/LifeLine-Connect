"""
Project: LifeLine Connect (Blood Bank Network)
Component: PL/SQL Business Reports Controller
"""

from flask import Blueprint, render_template, request
from app.models.report_model import (
    get_report1_camps_collections,
    get_report2_inventory_expiring,
    get_report3_donor_history,
    get_report4_hospital_fulfillment,
    get_report5_staff_workload
)
from app.models.donor_model import get_all_donors

report_bp = Blueprint("reports", __name__, url_prefix="/reports")

@report_bp.route("/")
def index():
    return render_template("reports/index.html")

@report_bp.route("/1")
def report1():
    # Report 1: Total Blood Units Collected by Blood Group Across Camps
    data = get_report1_camps_collections()
    total_units = sum(r.get("total_units_collected", 0) for r in data)
    total_donations = sum(r.get("total_donations", 0) for r in data)
    return render_template(
        "reports/report1.html",
        data=data,
        total_units=total_units,
        total_donations=total_donations
    )

@report_bp.route("/2")
def report2():
    # Report 2: Inventory Levels & Units Expiring within Time Frame
    days = request.args.get("days", 7)
    try:
        days = int(days)
    except ValueError:
        days = 7

    data = get_report2_inventory_expiring(days_ahead=days)
    return render_template("reports/report2.html", data=data, days=days)

@report_bp.route("/3")
def report3():
    # Report 3: Individual Donor Eligibility & Donation History Summaries
    donor_id = request.args.get("donor_id", 1001)
    try:
        donor_id = int(donor_id)
    except ValueError:
        donor_id = 1001

    summary, history = get_report3_donor_history(donor_id)
    donors = get_all_donors()

    return render_template(
        "reports/report3.html",
        summary=summary,
        history=history,
        donors=donors,
        selected_donor_id=donor_id
    )

@report_bp.route("/4")
def report4():
    # Report 4: Hospital Blood Demand & Fulfillment Efficiency
    data = get_report4_hospital_fulfillment()
    demanded = sum(r.get("total_units_demanded", 0) for r in data)
    fulfilled = sum(r.get("total_units_fulfilled", 0) for r in data)
    avg_rate = round((fulfilled / demanded * 100), 1) if demanded > 0 else 0

    return render_template(
        "reports/report4.html",
        data=data,
        total_demanded=demanded,
        total_fulfilled=fulfilled,
        avg_rate=avg_rate
    )

@report_bp.route("/5")
def report5():
    # Report 5: Staff & Volunteer Deployment and Operational Workload
    data = get_report5_staff_workload()
    total_hours = sum(r.get("total_hours_worked", 0) for r in data)
    total_shifts = sum(r.get("shifts_attended", 0) for r in data)

    return render_template(
        "reports/report5.html",
        data=data,
        total_hours=total_hours,
        total_shifts=total_shifts
    )
