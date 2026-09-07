"""
Project: LifeLine Connect (Blood Bank Network)
Component: Geospatial Logistics & IoT Cold-Chain Telemetry Controller
"""

from flask import Blueprint, render_template, jsonify, request
from app.models.camp_model import get_all_camps
from app.models.hospital_model import get_all_hospitals
from app.models.inventory_model import get_inventory_summary
import random
import time

logistics_bp = Blueprint("logistics", __name__, url_prefix="/logistics")

# Regional geospatial coordinates centered around Sri Lanka (Western Province / Colombo Health Corridor)
SAMPLE_COORDINATES = {
    "hospitals": [
        {"id": 5001, "name": "National Hospital of Sri Lanka (NHSL Colombo 10)", "lat": 6.9197, "lng": 79.8687, "type": "National Level 1 Trauma", "urgency": "CRITICAL"},
        {"id": 5002, "name": "Colombo South Teaching Hospital (Kalubowila)", "lat": 6.8657, "lng": 79.8837, "type": "Teaching Hospital", "urgency": "NORMAL"},
        {"id": 5003, "name": "Lady Ridgeway Hospital for Children (LRH Borella)", "lat": 6.9205, "lng": 79.8786, "type": "Pediatric Referral", "urgency": "URGENT"},
        {"id": 5004, "name": "Sri Jayewardenepura General Hospital (SJGH)", "lat": 6.8684, "lng": 79.9193, "type": "Tertiary Trauma Care", "urgency": "NORMAL"}
    ],
    "camps": [
        {"id": 2001, "name": "Viharamahadevi Park Mega Blood Drive (Colombo 07)", "lat": 6.9142, "lng": 79.8617, "status": "ACTIVE", "target": 250},
        {"id": 2002, "name": "University of Moratuwa Engineering Faculty Camp", "lat": 6.7972, "lng": 79.9018, "status": "ACTIVE", "target": 180},
        {"id": 2003, "name": "University of Colombo Faculty of Medicine Camp", "lat": 6.9192, "lng": 79.8732, "status": "UPCOMING", "target": 140}
    ],
    "storage_hub": {
        "name": "National Blood Centre (NBTS Sri Lanka)",
        "lat": 6.8938,
        "lng": 79.8828,
        "address": "No. 555/5 Elvitigala Mawatha, Narahenpita, Colombo 05"
    },
    "couriers": [
        {"id": "VAN-101", "name": "NBTS Refrigerated Mobile Unit (WP-CAA-4491)", "driver": "Sunil Shantha", "temp": "3.8°C", "lat": 6.9050, "lng": 79.8720, "status": "EN_ROUTE_HOSPITAL", "destination": "National Hospital (NHSL)"},
        {"id": "VAN-102", "name": "Suwa Seriya 1990 Emergency Transporter", "driver": "Nuwan Pradeep", "temp": "4.1°C", "lat": 6.8850, "lng": 79.8900, "status": "EN_ROUTE_HOSPITAL", "destination": "Kalubowila Hospital"},
        {"id": "DRONE-01", "name": "LifeLine Lanka BioDrone D-01", "driver": "Autonomous BioFlight", "temp": "21.8°C", "lat": 6.9120, "lng": 79.8750, "status": "RAPID_DISPATCH", "destination": "Lady Ridgeway (LRH)"}
    ]
}

@logistics_bp.route("/")
def index():
    camps = get_all_camps()
    hospitals = get_all_hospitals()
    summary = get_inventory_summary()
    return render_template(
        "logistics/index.html",
        camps=camps,
        hospitals=hospitals,
        summary=summary
    )

@logistics_bp.route("/api/locations")
def api_locations():
    """Returns geospatial features for Leaflet Radar Map."""
    return jsonify(SAMPLE_COORDINATES)

@logistics_bp.route("/api/telemetry")
def api_telemetry():
    """Streams simulated live IoT sensor telemetry across 4 cold-chain storage bays."""
    now = time.time()
    # Subtle harmonic micro-variations to emulate real-world sensor fluctuations
    wb_temp = round(3.8 + 0.3 * (random.random() - 0.5), 2)
    rbc_temp = round(4.1 + 0.25 * (random.random() - 0.5), 2)
    plt_temp = round(22.2 + 0.4 * (random.random() - 0.5), 2)
    plasma_temp = round(-23.4 + 0.6 * (random.random() - 0.5), 2)

    return jsonify({
        "timestamp": now,
        "bays": [
            {
                "bay_id": "BAY-WB-01",
                "name": "Whole Blood Main Storage",
                "component": "Whole Blood",
                "temperature": wb_temp,
                "unit": "°C",
                "safe_min": 2.0,
                "safe_max": 6.0,
                "humidity": "48%",
                "door_seal": "LOCKED_SECURE",
                "power_grid": "PRIMARY_GRID (100%)",
                "status": "NOMINAL" if 2.0 <= wb_temp <= 6.0 else "ALERT"
            },
            {
                "bay_id": "BAY-RBC-02",
                "name": "Red Blood Cell Preservation Cell",
                "component": "Packed RBC",
                "temperature": rbc_temp,
                "unit": "°C",
                "safe_min": 2.0,
                "safe_max": 6.0,
                "humidity": "50%",
                "door_seal": "LOCKED_SECURE",
                "power_grid": "PRIMARY_GRID (100%)",
                "status": "NOMINAL" if 2.0 <= rbc_temp <= 6.0 else "ALERT"
            },
            {
                "bay_id": "BAY-PLT-03",
                "name": "Platelet Agitator & Incubator",
                "component": "Platelets",
                "temperature": plt_temp,
                "unit": "°C",
                "safe_min": 20.0,
                "safe_max": 24.0,
                "agitation_rate": "64 RPM (Optimal)",
                "door_seal": "LOCKED_SECURE",
                "power_grid": "UPS_BATTERY_BACKUP",
                "status": "NOMINAL" if 20.0 <= plt_temp <= 24.0 else "ALERT"
            },
            {
                "bay_id": "BAY-PLAS-04",
                "name": "Cryogenic Plasma Deep-Freezer",
                "component": "Fresh Frozen Plasma",
                "temperature": plasma_temp,
                "unit": "°C",
                "safe_min": -40.0,
                "safe_max": -18.0,
                "cryo_compressor": "ACTIVE_DUAL_STAGE",
                "door_seal": "HERMETIC_SEALED",
                "power_grid": "PRIMARY_GRID (100%)",
                "status": "NOMINAL" if plasma_temp <= -18.0 else "ALERT"
            }
        ]
    })
