# LifeLine Connect: Enterprise Blood Bank Network

LifeLine Connect is an enterprise hybrid database web application combining **Oracle Database 21c (Relational RDBMS)** for core mission-critical transactional operations and **MongoDB 8.0+ (NoSQL)** for polymorphic community and unstructured content. The application is built using **Python (Flask)** adhering strictly to the **Model-View-Controller (MVC)** architectural pattern.

---

## System Architecture

```
                                    +------------------------------+
                                    |     Client Web Browser       |
                                    | (HTML5 / Vanilla CSS3 / JS)  |
                                    +--------------+---------------+
                                                   |
                                                   v
                                    +------------------------------+
                                    |      Flask MVC Controllers   |
                                    |  (Blueprints & HTTP Routes)  |
                                    +-------+--------------+-------+
                                            |              |
                       +--------------------+              +--------------------+
                       |                                                        |
                       v                                                        v
        +------------------------------+                         +------------------------------+
        |     Oracle Data Models       |                         |     MongoDB Data Models      |
        |      (python-oracledb)       |                         |          (pymongo)           |
        +--------------+---------------+                         +--------------+---------------+
                       |                                                        |
                       v                                                        v
        +------------------------------+                         +------------------------------+
        |   Oracle Database 21c XE     |                         |      MongoDB 8.0+ Server     |
        |       (localhost:1521)       |                         |       (localhost:27017)      |
        +------------------------------+                         +------------------------------+
        | - DONORS (Eligibility & Bio) |                         | - campaign_media             |
        | - CAMPS (Catalogue & Venue)  |                         |   (Posters, Guidelines)      |
        | - STAFF & STAFF_ASSIGNMENTS  |                         | - camp_feedback              |
        | - DONATION_RECORDS           |                         |   (Multi-criteria Ratings)   |
        | - BLOOD_INVENTORY (FEFO)     |                         | - emergency_appeals          |
        | - HOSPITALS & BLOOD_REQUESTS |                         |   (Broadcasts & Q&A Threads) |
        | - BLOOD_DISPATCHES (Audit)   |                         +------------------------------+
        | - PL/SQL Packages & Triggers |
        | - 5 Business Reports         |
        +------------------------------+
```

---

## 1. Oracle Relational Database (Core Operations)
- **Schema**: `LIFELINE_USER` on `localhost:1521/XEPDB1`
- **Normalization**: Fully normalized Third Normal Form (3NF).
- **Core Tables**:
  - `DONORS`: Biometric vitals, blood classification, eligibility tracking.
  - `CAMPS`: Venue management, schedules, and collection targets.
  - `STAFF` & `STAFF_ASSIGNMENTS`: Medical personnel (Doctors, Nurses, Phlebotomists, Coordinators, Volunteers) and shift tracking.
  - `DONATION_RECORDS`: Pre-donation physical screening (BP, pulse, hemoglobin) and collection events.
  - `BLOOD_INVENTORY`: Component tracking (Whole Blood, RBC, Platelets, Plasma), storage locations, and First-Expired, First-Out (FEFO) management.
  - `HOSPITALS`: Partner healthcare facilities, trauma centers, and licensing.
  - `BLOOD_REQUESTS`: Demand orders, urgency grading (`CRITICAL_EMERGENCY`, `URGENT`, `NORMAL`).
  - `BLOOD_DISPATCHES`: Tracked fulfillment and logistics delivery.
  - `AUDIT_DISPATCH_LOG`: Automated audit log enforced by database trigger.

### Oracle PL/SQL Requirements:
- **`PKG_LIFELINE_CORE`**:
  - `fn_check_donor_eligibility`: Evaluates recovery interval (56 days), age, weight, and hemoglobin.
  - `sp_register_donor`: Registers donor with clinical parameters validation.
  - `sp_record_donation`: Logs screening vitals and auto-generates inventory unit with component-specific shelf lives.
  - `sp_fulfill_hospital_request`: Implements automated First-Expired, First-Out (FEFO) matching for hospital demand.
  - `sp_assign_staff_to_camp`: Schedules staff without shift overlap.
- **Triggers**:
  - `TRG_DONOR_POST_DONATION`: Auto-updates last donation date and computes next eligible date (+56 days).
  - `TRG_INVENTORY_AUTO_EXPIRE`: Auto-marks expired inventory past shelf life.
  - `TRG_AUDIT_DISPATCH`: Immutable audit logger on every dispatch fulfillment.
- **5 Business Reports (`PKG_LIFELINE_REPORTS`)**:
  1. *Total blood units collected by blood group across different camps*.
  2. *Blood inventory levels and identification of expiring units within a given time frame*.
  3. *Individual donor eligibility and donation history summaries*.
  4. *Hospital blood demand, emergency turnaround, and fulfillment efficiency*.
  5. *Staff and volunteer deployment workload and specialized role coverage*.

---

## 2. MongoDB (Unstructured & Polymorphic Data)
- **Database**: `lifeline_connect` on `mongodb://localhost:27017`
- **Collections**:
  - `campaign_media`: Marketing assets, banners, video guides, and medical eligibility rules.
  - `camp_feedback`: Dimensional donor reviews (registration speed, friendliness, hygiene, refreshments, overall 1-5 score).
  - `emergency_appeals`: Real-time emergency notices, target blood groups, urgency levels, and community Q&A subdocuments.
- **PyMongo Queries**:
  - `get_camp_feedback(camp_id)`: Fetches reviews for a specific camp.
  - `get_top_rated_camps()`: Live MongoDB Aggregation Pipeline calculating average ratings and recommendation percentages.
  - `search_emergency_appeals(blood_group, keyword)`: Full-text and regex search across appeals and community discussions.

---

## 3. Application Structure (Flask MVC)

```
lifeline_connect/
├── app/
│   ├── __init__.py               # Flask application factory & filters
│   ├── config.py                 # Oracle & MongoDB configuration
│   ├── models/
│   │   ├── oracle_db.py          # Oracle connection pool & helper queries
│   │   ├── mongo_db.py           # MongoDB client & collection helpers
│   │   ├── donor_model.py        # Donor entity model
│   │   ├── camp_model.py         # Camp & assignment model
│   │   ├── inventory_model.py    # Inventory & donation collection model
│   │   ├── hospital_model.py     # Hospital request & dispatch model
│   │   ├── nosql_model.py        # Campaign media, feedback & appeals model
│   │   └── report_model.py       # PL/SQL Ref Cursor report model
│   ├── controllers/
│   │   ├── main_controller.py      # Executive Dashboard
│   │   ├── donor_controller.py     # Donor directory & profile
│   │   ├── camp_controller.py      # Camp catalogue & reviews
│   │   ├── inventory_controller.py # Inventory & donation intake
│   │   ├── hospital_controller.py  # Requisitions & FEFO dispatch
│   │   ├── appeal_controller.py    # Emergency appeals & community Q&A
│   │   └── report_controller.py    # The 5 PL/SQL business reports
│   ├── static/
│   │   ├── css/style.css         # Clinical dark glassmorphic design system
│   │   └── js/main.js            # Client-side dynamic interactions
│   └── templates/                # Responsive Jinja2 views
│       ├── base.html
│       ├── dashboard.html
│       ├── donors/ (list, register, profile)
│       ├── camps/ (list, detail, top_rated)
│       ├── inventory/ (stock, expiring, donate)
│       ├── hospitals/ (list, requests, new_request, dispatches)
│       ├── appeals/ (list, new_appeal)
│       └── reports/ (index, report1 - report5)
├── database/
│   ├── oracle/
│   │   ├── 01_schema.sql
│   │   ├── 02_sample_data.sql
│   │   ├── 03_procedures_functions.sql
│   │   ├── 04_triggers.sql
│   │   ├── 05_business_reports.sql
│   │   └── deploy_all.py         # Automated Oracle deployment suite
│   └── mongodb/
│       ├── 01_mongo_seed.py      # MongoDB collection seeder
│       └── 02_mongo_queries.py   # Standalone PyMongo query tester
├── docs/
│   ├── LifeLine_Connect_Requirements.md
│   └── ERD_Diagram.md
├── tests/
│   └── test_app.py               # Comprehensive 24-point automated test suite
├── run.py                        # Application entry point
└── requirements.txt
```

---

## Quick Start & Execution

### 1. Requirements Installation
```bash
pip install flask oracledb pymongo
```

### 2. Deploy Oracle 21c Database Objects
```bash
python database/oracle/deploy_all.py
```

### 3. Seed MongoDB Collections
```bash
python database/mongodb/01_mongo_seed.py
```

### 4. Run Automated Test Suite
```bash
python tests/test_app.py
```

### 5. Launch the Web Application
```bash
python run.py
```
Open **http://127.0.0.1:5000** in your browser.
