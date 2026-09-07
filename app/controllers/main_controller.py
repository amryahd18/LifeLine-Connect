"""
Project: LifeLine Connect (Blood Bank Network)
Component: Main Dashboard Controller
"""

from flask import Blueprint, render_template
from app.models.inventory_model import get_inventory_summary
from app.models.donor_model import get_all_donors
from app.models.camp_model import get_all_camps
from app.models.hospital_model import get_blood_requests
from app.models.nosql_model import search_emergency_appeals, get_top_rated_camps

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def dashboard():
    # 1. Oracle Telemetry
    inventory_summary = get_inventory_summary()
    all_donors = get_all_donors()
    all_camps = get_all_camps()
    active_camps = [c for c in all_camps if c["status"] == "ACTIVE"]
    pending_requests = get_blood_requests(status="PENDING")
    
    # 2. MongoDB Telemetry
    emergency_appeals = search_emergency_appeals(status="OPEN")
    top_camps = get_top_rated_camps()[:3]

    stats = {
        "available_units": inventory_summary["total_available"],
        "total_donors": len(all_donors),
        "active_camps": len(active_camps),
        "pending_requests": len(pending_requests),
        "emergency_appeals": len(emergency_appeals),
        "transfused_units": inventory_summary["total_transfused"]
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        groups=inventory_summary["groups"],
        appeals=emergency_appeals[:4],
        top_camps=top_camps,
        recent_donors=all_donors[:5],
        active_camps=active_camps
    )
