# LifeLine Connect (Blood Bank Network) - Technical Specification & Requirements

## Architecture Overview
- **Application Framework**: Python (Flask) with Model-View-Controller (MVC) pattern.
- **Relational Storage (RDBMS)**: Oracle Database 21c Express Edition (`oracledb`).
- **Document / Unstructured Storage (NoSQL)**: MongoDB 8.0+ (`pymongo`).
- **Frontend**: Responsive HTML5, Vanilla CSS3 (Custom Design System with Glassmorphism and modern medical blood-bank theme), Vanilla JS.

---

## 1. Oracle Relational Database (Core Operations)
Highly normalized (3NF) relational database schema for:
1. **Donors**: Registration, blood group classification (ABO/Rh), biometric vitals, health screening, and donation eligibility status tracking.
2. **Camps**: Blood donation camp catalogue, scheduling, organizer and venue management.
3. **Staff & Volunteers**: Medical personnel (Doctors, Phlebotomists, Nurses, Coordinators) and camp shift assignment tracking.
4. **Donation Records**: Physical screening vitals (BP, Hemoglobin, Pulse), test screening status, and donation unit logging.
5. **Inventory**: Blood units by component (Whole Blood, Packed Red Blood Cells, Platelets, Fresh Frozen Plasma), storage shelf locations, collection and FEFO expiration tracking.
6. **Hospitals**: Verified hospital registry, licensing, emergency tier classification.
7. **Blood Requests & Dispatches**: Hospital demand orders, priority levels (Normal, Urgent, Critical Emergency), unit allocations, and dispatch tracking.

### Oracle PL/SQL Requirements:
- Production-ready PL/SQL stored procedures, functions, triggers, cursors, and custom exception handling.
- Comprehensive seed data script populating realistic medical records across all entities.
- Exactly 5 business reports:
  1. Total blood units collected by blood group across different camps.
  2. Blood inventory levels and identification of expiring units within a given time frame.
  3. Individual donor eligibility and donation history summaries.
  4. Hospital demand, emergency turnaround, and fulfillment efficiency report.
  5. Staff & volunteer deployment workload and specialized role coverage report.

---

## 2. MongoDB (Unstructured & Flexible Data)
Schema-flexible document collections for:
1. **`campaign_media`**: Promotional assets, banners, video guides, and medical eligibility guidelines.
2. **`camp_feedback`**: Donor reviews, dimensional ratings (registration speed, staff friendliness, hygiene, refreshment quality, overall score), and open-ended feedback.
3. **`emergency_appeals`**: Critical broadcast notices, patient cases, target blood groups, urgency levels, and community Q&A subdocuments.

### MongoDB Query Requirements:
- Retrieve all feedback and reviews for a specific camp.
- Identify top-rated camps based on aggregated ratings using the MongoDB Aggregation Pipeline.
- Search emergency appeals or threads for specific blood types or keywords with text indexing and regex matching.

---

## 3. Application Integration (Flask MVC)
- Modular MVC architecture with dedicated models for Oracle (`oracledb`) and MongoDB (`pymongo`).
- Blueprints and controllers for Donors, Camps, Inventory, Hospitals, Emergency Appeals, and PL/SQL Reports.
- State-of-the-art UI with responsive cards, live KPI telemetry, inventory heatmaps, and clean forms.
