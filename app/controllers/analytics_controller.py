"""
Project: LifeLine Connect (Blood Bank Network)
Component: AI Shortage Forecaster & Predictive Donor Summoning Controller
"""

from flask import Blueprint, render_template, jsonify, request
from app.models.inventory_model import get_inventory_summary
from app.models.donor_model import get_all_donors
from app.models.hospital_model import get_blood_requests

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@analytics_bp.route("/forecaster")
def forecaster():
    """Predictive Blood Shortage Forecaster evaluating stock runway and demand velocity."""
    summary = get_inventory_summary()
    requests = get_blood_requests()

    # Calculate demand weights based on pending hospital requisitions
    group_demand = {bg: 1.2 for bg in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']}
    for r in requests:
        bg = r.get("blood_group")
        if bg in group_demand:
            group_demand[bg] += float(r.get("units_requested", 1)) * 0.4

    forecast_data = []
    critical_alerts = []

    for g in summary.get("groups", []):
        bg = g["blood_group"]
        avail = g["available_units"]
        burn_rate = round(group_demand.get(bg, 1.0), 1)  # Units consumed per day
        days_remaining = round(avail / burn_rate, 1) if burn_rate > 0 else 99.0

        if days_remaining <= 2.5:
            status = "CRITICAL DEFICIT"
            badge_class = "badge-ineligible"
            action_text = f"Immediate mobile drive or targeted donor summoning required for {bg}."
            critical_alerts.append({"blood_group": bg, "days": days_remaining, "action": action_text})
        elif days_remaining <= 5.0:
            status = "LOW RESERVE"
            badge_class = "badge-deferred"
            action_text = f"Send gentle re-engagement summons to eligible {bg} donors."
        else:
            status = "HEALTHY STOCK"
            badge_class = "badge-eligible"
            action_text = "Inventory nominal. Routine rotation active."

        forecast_data.append({
            "blood_group": bg,
            "available_units": avail,
            "daily_burn_rate": burn_rate,
            "days_remaining": days_remaining,
            "status": status,
            "badge_class": badge_class,
            "action_text": action_text,
            "seven_day_deficit": round(max(0, (burn_rate * 7) - avail), 1),
            "fourteen_day_deficit": round(max(0, (burn_rate * 14) - avail), 1)
        })

    # Sort so most critical shortage is at the top
    forecast_data.sort(key=lambda x: x["days_remaining"])

    return render_template(
        "analytics/forecaster.html",
        forecast=forecast_data,
        critical_alerts=critical_alerts
    )

@analytics_bp.route("/api/summon-donors", methods=["POST"])
def api_summon_donors():
    """Finds all eligible donors in Oracle matching target blood group and prepares emergency summons."""
    data = request.get_json() or {}
    target_bg = data.get("blood_group", "O-")

    # Fetch eligible donors from Oracle RDBMS
    eligible_donors = get_all_donors(blood_group=target_bg, eligibility="ELIGIBLE")

    recipients = []
    for d in eligible_donors[:15]:  # Top priority recipients
        recipients.append({
            "donor_id": d["donor_id"],
            "name": f"{d['first_name']} {d['last_name']}",
            "city": d["city"],
            "phone": d["phone"],
            "email": d["email"],
            "last_donation": str(d.get("last_donation_date", "None"))
        })

    sms_template = (
        f"🚨 [URGENT NBTS SRI LANKA ALERT] National Blood Transfusion Service is experiencing an acute "
        f"shortage of {target_bg} blood units. As a registered donor in Sri Lanka, "
        f"your single donation can save critical emergency patients at NHSL / LRH today. "
        f"Please visit Central Blood Bank Narahenpita or contact emergency hotline 1990 / 011 236 9931: "
        f"https://nbts.health.gov.lk/urgent/{target_bg}"
    )

    return jsonify({
        "status": "SUCCESS",
        "blood_group": target_bg,
        "eligible_count": len(eligible_donors),
        "dispatched_count": len(recipients),
        "recipients": recipients,
        "message_template": sms_template
    })
