"""
Project: LifeLine Connect (Blood Bank Network)
Component: MongoDB NoSQL Data Model (Media, Feedback, Emergency Appeals)
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import pymongo
from app.models.mongo_db import get_collection

# =============================================================================
# 1. CAMPAIGN MEDIA & GUIDELINES
# =============================================================================
def get_campaign_media(camp_id: Optional[int] = None) -> List[Dict[str, Any]]:
    col = get_collection("campaign_media")
    query = {}
    if camp_id is not None:
        query["camp_id"] = int(camp_id)
    return list(col.find(query, {"_id": 0}).sort("created_at", pymongo.DESCENDING))

# =============================================================================
# 2. CAMP FEEDBACK & REVIEWS
# =============================================================================
def get_camp_feedback(camp_id: int) -> List[Dict[str, Any]]:
    col = get_collection("camp_feedback")
    return list(col.find({"camp_id": int(camp_id)}, {"_id": 0}).sort("submitted_at", pymongo.DESCENDING))

def get_top_rated_camps(min_reviews: int = 1) -> List[Dict[str, Any]]:
    col = get_collection("camp_feedback")
    pipeline = [
        {
            "$group": {
                "_id": "$camp_id",
                "camp_id": {"$first": "$camp_id"},
                "review_count": {"$sum": 1},
                "avg_overall_score": {"$avg": "$ratings.overall_score"},
                "avg_registration_speed": {"$avg": "$ratings.registration_speed"},
                "avg_staff_friendliness": {"$avg": "$ratings.staff_friendliness"},
                "avg_hygiene_safety": {"$avg": "$ratings.hygiene_and_safety"},
                "avg_refreshment_quality": {"$avg": "$ratings.refreshment_quality"},
                "recommend_count": {
                    "$sum": {"$cond": [{"$eq": ["$recommend_to_others", True]}, 1, 0]}
                }
            }
        },
        {"$match": {"review_count": {"$gte": min_reviews}}},
        {
            "$project": {
                "_id": 0,
                "camp_id": 1,
                "review_count": 1,
                "avg_overall_score": {"$round": ["$avg_overall_score", 2]},
                "avg_registration_speed": {"$round": ["$avg_registration_speed", 2]},
                "avg_staff_friendliness": {"$round": ["$avg_staff_friendliness", 2]},
                "avg_hygiene_safety": {"$round": ["$avg_hygiene_safety", 2]},
                "avg_refreshment_quality": {"$round": ["$avg_refreshment_quality", 2]},
                "recommendation_pct": {
                    "$round": [
                        {"$multiply": [{"$divide": ["$recommend_count", "$review_count"]}, 100]},
                        1
                    ]
                }
            }
        },
        {"$sort": {"avg_overall_score": pymongo.DESCENDING, "review_count": pymongo.DESCENDING}}
    ]
    return list(col.aggregate(pipeline))

def add_camp_feedback(data: Dict[str, Any]) -> str:
    col = get_collection("camp_feedback")
    doc = {
        "camp_id": int(data["camp_id"]),
        "donor_id": int(data.get("donor_id", 0)),
        "donor_name": data["donor_name"],
        "blood_group": data.get("blood_group", "O+"),
        "ratings": {
            "registration_speed": float(data.get("registration_speed", 5)),
            "staff_friendliness": float(data.get("staff_friendliness", 5)),
            "hygiene_and_safety": float(data.get("hygiene_and_safety", 5)),
            "refreshment_quality": float(data.get("refreshment_quality", 5)),
            "overall_score": float(data.get("overall_score", 5))
        },
        "feedback_text": data["feedback_text"],
        "recommend_to_others": data.get("recommend_to_others") in (True, "true", "on", 1),
        "donor_badges": ["Verified Donor"],
        "submitted_at": datetime.now(timezone.utc)
    }
    res = col.insert_one(doc)
    return str(res.inserted_id)

# =============================================================================
# 3. EMERGENCY APPEALS & COMMUNITY Q&A
# =============================================================================
def search_emergency_appeals(
    blood_group: Optional[str] = None,
    keyword: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict[str, Any]]:
    col = get_collection("emergency_appeals")
    query: Dict[str, Any] = {}

    if blood_group and blood_group.strip():
        query["blood_group"] = blood_group.strip().upper()

    if status and status.strip():
        query["status"] = status.strip().upper()

    if keyword and keyword.strip():
        term = keyword.strip()
        regex_pattern = {"$regex": term, "$options": "i"}
        query["$or"] = [
            {"patient_condition": regex_pattern},
            {"hospital_name": regex_pattern},
            {"city": regex_pattern},
            {"community_qa.message": regex_pattern},
            {"community_qa.reply": regex_pattern}
        ]

    return list(col.find(query, {"_id": 0}).sort("created_at", pymongo.DESCENDING))

def create_emergency_appeal(data: Dict[str, Any]) -> str:
    col = get_collection("emergency_appeals")
    appeal_count = col.count_documents({}) + 1
    doc = {
        "appeal_id": f"APPEAL-2026-{appeal_count:03d}",
        "hospital_id": int(data.get("hospital_id", 7001)),
        "hospital_name": data["hospital_name"],
        "blood_group": data["blood_group"].upper(),
        "urgency": data.get("urgency", "CRITICAL").upper(),
        "units_required": int(data["units_required"]),
        "patient_condition": data["patient_condition"],
        "city": data["city"],
        "contact_phone": data.get("contact_phone", "+94-11-269-1111"),
        "status": "OPEN",
        "created_at": datetime.now(timezone.utc),
        "broadcast_channels": ["LifeLine Network Alert", "SMS Broadcast"],
        "community_qa": []
    }
    col.insert_one(doc)
    return doc["appeal_id"]

def add_appeal_qa(appeal_id: str, qa_data: Dict[str, Any]) -> bool:
    col = get_collection("emergency_appeals")
    qa_entry = {
        "user_name": qa_data.get("user_name", "Anonymous Volunteer"),
        "user_type": qa_data.get("user_type", "Community Member"),
        "message": qa_data["message"],
        "reply": qa_data.get("reply", "Under review by LifeLine emergency coordinator."),
        "timestamp": datetime.now(timezone.utc)
    }
    res = col.update_one(
        {"appeal_id": appeal_id},
        {"$push": {"community_qa": qa_entry}}
    )
    return res.modified_count > 0
