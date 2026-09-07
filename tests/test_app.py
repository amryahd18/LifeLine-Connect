"""
Project: LifeLine Connect (Blood Bank Network)
Component: End-to-End Automated Test Suite for Flask MVC, Oracle, and MongoDB
"""

import sys
import os

# Add root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

def run_tests():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    print("\n" + "=" * 70)
    print("RUNNING LIFELINE CONNECT COMPREHENSIVE TEST SUITE")
    print("=" * 70)

    test_endpoints = [
        ("/", "Executive Dashboard"),
        ("/donors/", "Donor Registry"),
        ("/donors/1001", "Donor Profile (Kasun Fernando)"),
        ("/donors/register", "Donor Registration Form"),
        ("/camps/", "Camps Catalogue"),
        ("/camps/2001", "Camp Detail (Viharamahadevi Park Mega Drive with MongoDB feedback)"),
        ("/camps/top-rated", "Top-Rated Camps (MongoDB Aggregation Pipeline)"),
        ("/inventory/", "Inventory Stock Matrix"),
        ("/inventory/expiring?days=7", "Expiring Stock Alert (PL/SQL Report 2)"),
        ("/inventory/donate", "Donation & Clinical Pre-Screening Intake"),
        ("/hospitals/", "Hospital Registry"),
        ("/hospitals/requests", "Hospital Blood Requisitions"),
        ("/hospitals/requests/new", "New Blood Requisition Form"),
        ("/hospitals/dispatches", "Dispatch Audit Trail"),
        ("/appeals/", "Emergency Appeals Board (MongoDB)"),
        ("/appeals/?blood_group=O-&keyword=trauma", "Emergency Appeals Filter Query"),
        ("/appeals/new", "Emergency Appeal Broadcast Form"),
        ("/reports/", "PL/SQL Business Reports Hub"),
        ("/reports/1", "Report 1: Total Units Collected Across Camps by Blood Group"),
        ("/reports/2?days=7", "Report 2: Inventory Levels & Expiring Units"),
        ("/reports/3?donor_id=1001", "Report 3: Donor Eligibility & History Dossier"),
        ("/reports/4", "Report 4: Hospital Blood Demand & Fulfillment Efficiency"),
        ("/reports/5", "Report 5: Staff & Volunteer Deployment Workload"),
        ("/auth/login", "User Sign-In Screen"),
        ("/auth/register", "User Registration Screen"),
        ("/logistics/", "Geospatial Radar Map & Logistics Command"),
        ("/logistics/api/locations", "Geospatial Locations & Route Coordinates API"),
        ("/logistics/api/telemetry", "IoT Cold-Chain Storage Sensor Telemetry Stream"),
        ("/analytics/forecaster", "AI Clinical Shortage Forecaster & Runway Predictor"),
        ("/database/", "Live Database Explorer & SQL Studio (Oracle + Mongo)"),
    ]

    passed = 0
    failed = 0

    for path, name in test_endpoints:
        try:
            res = client.get(path)
            if res.status_code == 200:
                print(f"[PASS 200 OK] {name:60} -> {path}")
                passed += 1
            else:
                print(f"[FAIL {res.status_code}] {name:60} -> {path}")
                failed += 1
        except Exception as e:
            print(f"[ERROR] {name:60} -> {path} : {e}")
            failed += 1

    # Test API: Dynamic Eligibility Check via AJAX
    print("\n--- Testing Dynamic Eligibility Assessment API ---")
    res = client.post("/donors/1001/check-eligibility")
    if res.status_code == 200 and res.json.get("eligible") is True:
        print(f"[PASS 200 OK] Donor 1001 Eligibility API: {res.json.get('message')}")
        passed += 1
    else:
        print(f"[FAIL] Donor 1001 Eligibility API failed: {res.data}")
        failed += 1

    # Test API: AI Smart Donor Summon API
    print("\n--- Testing AI Smart Donor Summon API ---")
    summon_res = client.post("/analytics/api/summon-donors", json={"blood_group": "O-"})
    if summon_res.status_code == 200 and summon_res.json.get("status") == "SUCCESS":
        print(f"[PASS 200 OK] AI Smart Summon API: {summon_res.json.get('eligible_count')} O- donors identified.")
        passed += 1
    else:
        print(f"[FAIL] AI Smart Summon API failed: {summon_res.data}")
        failed += 1

    # Test API: Live Oracle SQL Query Console API
    print("\n--- Testing Live Oracle SQL Console API ---")
    sql_res = client.post("/database/api/query", json={"sql": "SELECT * FROM DONORS WHERE BLOOD_GROUP = 'O+'"})
    if sql_res.status_code == 200 and sql_res.json.get("success") is True and sql_res.json.get("count") > 0:
        print(f"[PASS 200 OK] Oracle SQL Console API: {sql_res.json.get('count')} rows retrieved from Oracle.")
        passed += 1
    else:
        print(f"[FAIL] Oracle SQL Console API failed: {sql_res.data}")
        failed += 1

    # Test Auth: Login Flow
    print("\n--- Testing Authentication & Registration Flows ---")
    
    # Auth Test Suite: Clear any leftover session
    with client.session_transaction() as sess:
        sess.clear()

    # 1. Invalid Credentials Login (should be rejected)
    bad_login_res = client.post("/auth/login", data={"identifier": "admin", "password": "WrongPassword!!!"}, follow_redirects=True)
    if b"Invalid credentials" in bad_login_res.data:
        print("[PASS 200 Error] Invalid Password correctly rejected.")
        passed += 1
    else:
        print("[FAIL] Invalid Password was not caught.")
        failed += 1

    # 2. Valid Login
    login_res = client.post("/auth/login", data={"identifier": "admin", "password": "AdminPass123#"}, follow_redirects=False)
    if login_res.status_code == 302:
        print("[PASS 302 Redirect] Valid Admin Login successfully established session.")
        passed += 1
    else:
        print(f"[FAIL] Valid Admin Login failed with status {login_res.status_code}")
        failed += 1

    # 3. New User Registration Flow
    import random
    rand_suffix = random.randint(1000, 9999)
    reg_data = {
        "username": f"donor_hero_{rand_suffix}",
        "email": f"hero_{rand_suffix}@lifeline.org",
        "full_name": f"Hero Donor #{rand_suffix}",
        "password": "SecurePassword123#",
        "confirm_password": "SecurePassword123#",
        "role": "DONOR"
    }
    reg_res = client.post("/auth/register", data=reg_data, follow_redirects=False)
    if reg_res.status_code == 302:
        print(f"[PASS 302 Redirect] User {reg_data['username']} registered and auto-logged in.")
        passed += 1
    else:
        print(f"[FAIL] User registration failed: {reg_res.status_code}")
        failed += 1

    # 4. Logout Flow
    logout_res = client.get("/auth/logout", follow_redirects=False)
    if logout_res.status_code == 302:
        print("[PASS 302 Redirect] User logged out and session cleared.")
        passed += 1
    else:
        print(f"[FAIL] Logout failed: {logout_res.status_code}")
        failed += 1

    print("\n" + "=" * 70)
    print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED (Total: {passed + failed})")
    print("=" * 70)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
