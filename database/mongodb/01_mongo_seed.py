"""
Project: LifeLine Connect (Blood Bank Network)
Component: Phase 2 - MongoDB Collections & Sample Data Seeder - Sri Lanka Edition
Database: MongoDB 8.0+
Database Name: lifeline_connect
"""

import sys
from datetime import datetime, timezone, timedelta
import pymongo
from pymongo import ASCENDING, DESCENDING, TEXT

def seed_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["lifeline_connect"]

    print("Connecting to MongoDB at localhost:27017/lifeline_connect...")

    # Drop existing collections for clean state
    db["campaign_media"].drop()
    db["camp_feedback"].drop()
    db["emergency_appeals"].drop()

    # =========================================================================
    # 1. CAMPAIGN MEDIA (Promotional materials & Medical Guidelines)
    # =========================================================================
    campaign_media_data = [
        {
            "camp_id": 2001,
            "title": "Viharamahadevi Park Mega Blood Drive - Give Blood, Save Lives in Sri Lanka",
            "media_type": "PROMOTIONAL_BANNER",
            "campaign_theme": "National Health Resilience & Community Care",
            "asset_url": "/static/images/campaigns/colombo_mega_drive.png",
            "target_audience": ["Colombo Residents", "Commuters", "First-Time Youth Donors"],
            "guidelines": {
                "general_eligibility": "Sri Lankan citizens aged 18-60, weight at least 50 kg, hemoglobin >= 12.5 g/dL.",
                "pre_donation_instructions": [
                    "Drink at least 500ml water or king coconut water 30 minutes before donation.",
                    "Eat a healthy, iron-rich meal (e.g. green leafy vegetables, dhal, rice) within 2-3 hours prior.",
                    "Avoid alcohol and tobacco for 24 hours prior."
                ],
                "temporary_deferrals": [
                    "Tattoo or body piercing within the last 12 months.",
                    "Recent fever, dengue recovery, or antibiotic medication within 14-28 days.",
                    "Dental surgery or extraction within 72 hours."
                ]
            },
            "languages_available": ["English", "Sinhala (සිංහල)", "Tamil (தமிழ்)"],
            "is_active": True,
            "created_at": datetime.now(timezone.utc) - timedelta(days=25)
        },
        {
            "camp_id": 2002,
            "title": "University of Moratuwa - Code Red: Engineers Saving Lives",
            "media_type": "DIGITAL_FLYER",
            "campaign_theme": "Undergraduate Youth Mobilization",
            "asset_url": "/static/images/campaigns/uom_drive.png",
            "target_audience": ["University Undergraduates", "Academic Staff", "Moratuwa Residents"],
            "guidelines": {
                "general_eligibility": "Minimum 50 kg body weight, valid Student ID or National Identity Card (NIC).",
                "pre_donation_instructions": [
                    "Get at least 6-7 hours of good night's rest.",
                    "Bring your Sri Lankan NIC / driving license / university student card.",
                    "Rest for 15 minutes at the refreshments pavilion after donating."
                ],
                "temporary_deferrals": [
                    "Recent viral fever or severe cough within 14 days."
                ]
            },
            "languages_available": ["English", "Sinhala (සිංහල)"],
            "is_active": True,
            "created_at": datetime.now(timezone.utc) - timedelta(days=15)
        },
        {
            "camp_id": 2003,
            "title": "Faculty of Medicine National Camp - Future Healers Blood Drive",
            "media_type": "INFOGRAPHIC_GUIDE",
            "campaign_theme": "Clinical Excellence & Platelet Mobilization",
            "asset_url": "/static/images/campaigns/med_faculty_drive.png",
            "target_audience": ["Medical Undergraduates", "Nursing Staff", "General Public"],
            "guidelines": {
                "general_eligibility": "Ages 18-60, weight 50kg+, screened by NBTS medical doctors.",
                "pre_donation_instructions": [
                    "Complimentary refreshments (fresh milk, biscuits, fruit) provided post-donation.",
                    "Recognized with official NBTS Donor Certificate of Appreciation."
                ],
                "temporary_deferrals": [
                    "COVID-19 vaccination within the last 7 days."
                ]
            },
            "languages_available": ["English", "Sinhala (සිංහල)", "Tamil (தமிழ்)"],
            "is_active": True,
            "created_at": datetime.now(timezone.utc) - timedelta(days=5)
        },
        {
            "camp_id": 2004,
            "title": "Kandy City Centre Blood Fair - Central Province Solidarity",
            "media_type": "POSTER",
            "campaign_theme": "Provincial Blood Stock Fortification",
            "asset_url": "/static/images/campaigns/kandy_fair.png",
            "target_audience": ["Kandy Community", "Lions Club Members", "Local Shoppers"],
            "guidelines": {
                "general_eligibility": "Healthy adults aged 18 to 60 with valid identification.",
                "pre_donation_instructions": [
                    "Registration desk located at KCC Level 3 Atrium next to the escalators."
                ],
                "temporary_deferrals": ["Pregnancy or lactation within 12 months."]
            },
            "languages_available": ["English", "Sinhala (සිංහල)"],
            "is_active": True,
            "created_at": datetime.now(timezone.utc) - timedelta(days=2)
        }
    ]

    db["campaign_media"].insert_many(campaign_media_data)
    db["campaign_media"].create_index([("camp_id", ASCENDING)])
    db["campaign_media"].create_index([("title", TEXT), ("campaign_theme", TEXT)])
    print(f"-> Seeded {len(campaign_media_data)} campaign media documents.")

    # =========================================================================
    # 2. CAMP FEEDBACK (Donor Reviews, Dimensional Ratings & Testimonials)
    # =========================================================================
    camp_feedback_data = [
        # Camp 2001 (Viharamahadevi Park - Completed) - Feedback 1
        {
            "camp_id": 2001,
            "donor_id": 1001,
            "donor_name": "Kasun Fernando",
            "blood_group": "O+",
            "ratings": {
                "registration_speed": 5,
                "staff_friendliness": 5,
                "hygiene_and_safety": 5,
                "refreshment_quality": 5,
                "overall_score": 5.0
            },
            "feedback_text": "Remarkably organized camp in the heart of Colombo! The NBTS medical officers and volunteers made the intake fast and painless. The refreshment lounge had fresh milk and biscuits.",
            "recommend_to_others": True,
            "donor_badges": ["Regular Donor", "Jeevithaye Thilina (Gift of Life)"],
            "submitted_at": datetime.now(timezone.utc) - timedelta(days=20)
        },
        # Camp 2001 - Feedback 2
        {
            "camp_id": 2001,
            "donor_id": 1002,
            "donor_name": "Dilini Jayasinghe",
            "blood_group": "O-",
            "ratings": {
                "registration_speed": 5,
                "staff_friendliness": 5,
                "hygiene_and_safety": 5,
                "refreshment_quality": 5,
                "overall_score": 5.0
            },
            "feedback_text": "As an O-Negative universal donor from Kandy visiting Colombo, I was treated with utmost care. The phlebotomist explained how this unit will help emergency trauma patients at NHSL.",
            "recommend_to_others": True,
            "donor_badges": ["Universal Donor", "Trauma LifeSaver"],
            "submitted_at": datetime.now(timezone.utc) - timedelta(days=20)
        },
        # Camp 2001 - Feedback 3
        {
            "camp_id": 2001,
            "donor_id": 1003,
            "donor_name": "Nuwan Bandara",
            "blood_group": "A+",
            "ratings": {
                "registration_speed": 4,
                "staff_friendliness": 5,
                "hygiene_and_safety": 5,
                "refreshment_quality": 4,
                "overall_score": 4.5
            },
            "feedback_text": "Brief queue during morning peak hours, but the digital registration QR system was very smooth. The staff at Viharamahadevi Park did an outstanding job.",
            "recommend_to_others": True,
            "donor_badges": ["Dengue Platelet Vanguard"],
            "submitted_at": datetime.now(timezone.utc) - timedelta(days=19)
        },
        # Camp 2002 (University of Moratuwa - Completed) - Feedback 1
        {
            "camp_id": 2002,
            "donor_id": 1005,
            "donor_name": "Mohamed Rifaz",
            "blood_group": "B+",
            "ratings": {
                "registration_speed": 5,
                "staff_friendliness": 5,
                "hygiene_and_safety": 5,
                "refreshment_quality": 4,
                "overall_score": 4.8
            },
            "feedback_text": "Incredible youthful enthusiasm at Moratuwa campus! The Rotaract student volunteers guided every donor meticulously. Highly sterile cots.",
            "recommend_to_others": True,
            "donor_badges": ["Campus Hero"],
            "submitted_at": datetime.now(timezone.utc) - timedelta(days=11)
        },
        # Camp 2002 - Feedback 2
        {
            "camp_id": 2002,
            "donor_id": 1006,
            "donor_name": "Fatima Farook",
            "blood_group": "B-",
            "ratings": {
                "registration_speed": 4,
                "staff_friendliness": 5,
                "hygiene_and_safety": 5,
                "refreshment_quality": 4,
                "overall_score": 4.5
            },
            "feedback_text": "Very respectful and reassuring nursing staff. As a rare B-Negative donor, I am proud to support our national health service.",
            "recommend_to_others": True,
            "donor_badges": ["Rare Blood Hero"],
            "submitted_at": datetime.now(timezone.utc) - timedelta(days=10)
        },
        # Camp 2003 (Faculty of Medicine - Active) - Feedback 1
        {
            "camp_id": 2003,
            "donor_id": 1001,
            "donor_name": "Kasun Fernando",
            "blood_group": "O+",
            "ratings": {
                "registration_speed": 5,
                "staff_friendliness": 5,
                "hygiene_and_safety": 5,
                "refreshment_quality": 5,
                "overall_score": 5.0
            },
            "feedback_text": "The energy at the Faculty of Medicine Quadrangle is inspiring! Medical students handled the hemoglobin screening and vital checks with supreme professional care.",
            "recommend_to_others": True,
            "donor_badges": ["Centurion Donor"],
            "submitted_at": datetime.now(timezone.utc) - timedelta(days=2)
        }
    ]

    db["camp_feedback"].insert_many(camp_feedback_data)
    db["camp_feedback"].create_index([("camp_id", ASCENDING)])
    db["camp_feedback"].create_index([("ratings.overall_score", DESCENDING)])
    print(f"-> Seeded {len(camp_feedback_data)} camp feedback documents.")

    # =========================================================================
    # 3. EMERGENCY APPEALS (Urgent notices, blood groups, Community Q&A)
    # =========================================================================
    emergency_appeals_data = [
        {
            "appeal_id": "APPEAL-2026-001",
            "hospital_id": 7001,
            "hospital_name": "National Hospital of Sri Lanka (NHSL)",
            "blood_group": "O-",
            "urgency": "CRITICAL",
            "units_required": 4,
            "patient_condition": "Multi-vehicle collision on Southern Expressway - 3 acute emergency surgeries underway in NHSL Trauma ICU",
            "city": "Colombo 10",
            "contact_phone": "+94-11-269-1111",
            "status": "OPEN",
            "created_at": datetime.now(timezone.utc) - timedelta(hours=6),
            "expires_at": datetime.now(timezone.utc) + timedelta(hours=18),
            "broadcast_channels": ["1990 Suwa Seriya Network", "NBTS Alert SMS", "National Radio Sri Lanka", "Hospital Exchange"],
            "community_qa": [
                {
                    "user_name": "Dr. Kavinga Perera",
                    "user_type": "NBTS Consultant Physician",
                    "message": "Can donors who gave blood 60 days ago participate?",
                    "reply": "Yes! The minimum interval is 56 days (8 weeks). Any healthy O-Negative donor in Colombo or Gampaha is urgently requested.",
                    "timestamp": datetime.now(timezone.utc) - timedelta(hours=4)
                },
                {
                    "user_name": "Saman Kumara",
                    "user_type": "Prospective Donor",
                    "message": "Where is the intake center open right now?",
                    "reply": "Please report directly to National Blood Centre (NBTS Narahenpita, Colombo 05) or the NHSL Blood Bank counter (Ground Floor, Regent St).",
                    "timestamp": datetime.now(timezone.utc) - timedelta(hours=2)
                }
            ]
        },
        {
            "appeal_id": "APPEAL-2026-002",
            "hospital_id": 7003,
            "hospital_name": "Lady Ridgeway Hospital for Children (LRH)",
            "blood_group": "A+",
            "urgency": "URGENT",
            "units_required": 3,
            "patient_condition": "Pediatric Dengue Hemorrhagic Fever Ward 7 - multiple young patients with severe acute thrombocytopenia",
            "city": "Colombo 08",
            "contact_phone": "+94-11-269-3711",
            "status": "OPEN",
            "created_at": datetime.now(timezone.utc) - timedelta(hours=14),
            "expires_at": datetime.now(timezone.utc) + timedelta(hours=34),
            "broadcast_channels": ["Dengue Emergency Registry", "Web Portal", "Rotary Blood Network"],
            "community_qa": [
                {
                    "user_name": "Nuwan Bandara",
                    "user_type": "A+ Platelet Donor",
                    "message": "I donated whole blood 3 months ago. Can I donate apheresis platelets today at Narahenpita?",
                    "reply": "Yes, Nuwan! Apheresis platelet donation can be done safely. Please visit the Narahenpita Blood Centre apheresis unit.",
                    "timestamp": datetime.now(timezone.utc) - timedelta(hours=10)
                }
            ]
        },
        {
            "appeal_id": "APPEAL-2026-003",
            "hospital_id": 7005,
            "hospital_name": "Teaching Hospital Karapitiya (Galle)",
            "blood_group": "O+",
            "urgency": "CRITICAL",
            "units_required": 3,
            "patient_condition": "Emergency obstetric patient experiencing acute postpartum hemorrhage in Galle Maternity Ward",
            "city": "Galle",
            "contact_phone": "+94-91-223-2250",
            "status": "OPEN",
            "created_at": datetime.now(timezone.utc) - timedelta(hours=3),
            "expires_at": datetime.now(timezone.utc) + timedelta(hours=21),
            "broadcast_channels": ["Southern Provincial Network", "1990 Emergency Logistics"],
            "community_qa": [
                {
                    "user_name": "Sister Nirmala",
                    "user_type": "Hospital Transfusion Officer",
                    "message": "LifeLine courier dispatch has routed 1 unit via Galle expressway corridor. Requesting 2 local O+ donors to replenish southern reserve.",
                    "reply": "Received. Southern provincial donor registry broadcast dispatched.",
                    "timestamp": datetime.now(timezone.utc) - timedelta(hours=1)
                }
            ]
        },
        {
            "appeal_id": "APPEAL-2026-004",
            "hospital_id": 7002,
            "hospital_name": "Colombo South Teaching Hospital (Kalubowila)",
            "blood_group": "B-",
            "urgency": "NORMAL",
            "units_required": 2,
            "patient_condition": "Elective cardiovascular reconstructive surgery scheduled for tomorrow morning",
            "city": "Dehiwala",
            "contact_phone": "+94-11-276-3037",
            "status": "FULFILLED",
            "created_at": datetime.now(timezone.utc) - timedelta(days=2),
            "expires_at": datetime.now(timezone.utc) - timedelta(days=1),
            "broadcast_channels": ["Donor Network Portal"],
            "community_qa": [
                {
                    "user_name": "Fatima Farook",
                    "user_type": "B- Donor",
                    "message": "Unit donated yesterday at Kalubowila hospital blood bank.",
                    "reply": "Cross-matched and allocated for the surgical procedure. Bohoma Sthuthi (Thank you) for saving a life!",
                    "timestamp": datetime.now(timezone.utc) - timedelta(days=1)
                }
            ]
        }
    ]

    db["emergency_appeals"].insert_many(emergency_appeals_data)
    db["emergency_appeals"].create_index([("blood_group", ASCENDING), ("status", ASCENDING)])
    db["emergency_appeals"].create_index([("urgency", ASCENDING)])
    db["emergency_appeals"].create_index([
        ("patient_condition", TEXT),
        ("hospital_name", TEXT),
        ("city", TEXT),
        ("community_qa.message", TEXT)
    ])
    print(f"-> Seeded {len(emergency_appeals_data)} emergency appeals documents.")

    client.close()
    print("\nMongoDB initialization and sample seeding completed successfully!")

if __name__ == "__main__":
    seed_mongodb()
