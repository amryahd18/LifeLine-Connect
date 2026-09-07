"""
Project: LifeLine Connect (Blood Bank Network)
Component: Phase 2 - PyMongo Query Implementations
Database: MongoDB (lifeline_connect)

This module provides production-grade query functions for:
1. get_camp_feedback(camp_id): Retrieve all feedback/reviews for a specific camp.
2. get_top_rated_camps(): Identify top-rated camps based on aggregated ratings.
3. search_emergency_appeals(blood_group=None, keyword=None): Search emergency appeals or threads.
"""

from typing import List, Dict, Any, Optional
import pymongo

def get_mongo_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client["lifeline_connect"]

# =============================================================================
# QUERY 1: Retrieve all feedback/reviews for a specific camp
# =============================================================================
def get_camp_feedback(camp_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves all donor reviews, ratings, and open-ended feedback for a specific camp,
    sorted by submission date descending.
    """
    db = get_mongo_db()
    cursor = db["camp_feedback"].find(
        {"camp_id": int(camp_id)},
        {"_id": 0}
    ).sort("submitted_at", pymongo.DESCENDING)
    return list(cursor)

# =============================================================================
# QUERY 2: Identify top-rated camps based on aggregated ratings
# =============================================================================
def get_top_rated_camps(min_reviews: int = 1) -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline over camp_feedback to calculate:
    - Average overall score
    - Average registration speed
    - Average staff friendliness
    - Average hygiene & safety
    - Average refreshment quality
    - Total review count
    - % recommendation rate
    Sorted by average overall score in descending order.
    """
    db = get_mongo_db()
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
        {
            "$match": {
                "review_count": {"$gte": min_reviews}
            }
        },
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
        {
            "$sort": {"avg_overall_score": pymongo.DESCENDING, "review_count": pymongo.DESCENDING}
        }
    ]
    return list(db["camp_feedback"].aggregate(pipeline))

# =============================================================================
# QUERY 3: Search emergency appeals or threads for specific blood types or keywords
# =============================================================================
def search_emergency_appeals(
    blood_group: Optional[str] = None,
    keyword: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Searches emergency appeal notices and community Q&A subdocuments by:
    - blood_group (exact match or ABO compatibility)
    - keyword (matched case-insensitively across patient_condition, hospital_name,
      city, and community Q&A questions/answers)
    - status ('OPEN', 'FULFILLED', etc.)
    """
    db = get_mongo_db()
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

    cursor = db["emergency_appeals"].find(query, {"_id": 0}).sort("created_at", pymongo.DESCENDING)
    return list(cursor)

# =============================================================================
# HELPER QUERY: Retrieve Campaign Media for a Camp or Guidelines
# =============================================================================
def get_campaign_media_by_camp(camp_id: int) -> List[Dict[str, Any]]:
    db = get_mongo_db()
    cursor = db["campaign_media"].find({"camp_id": int(camp_id)}, {"_id": 0})
    return list(cursor)

# =============================================================================
# VERIFICATION DEMO
# =============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("1. QUERY DEMO: Retrieve Feedback for Camp 2001 (City Hall Drive)")
    print("=" * 70)
    feedback_2001 = get_camp_feedback(2001)
    for f in feedback_2001:
        print(f"Donor: {f['donor_name']} ({f['blood_group']}) | Rating: {f['ratings']['overall_score']}/5.0")
        print(f"Comment: {f['feedback_text']}")
        print(f"Badges: {f.get('donor_badges', [])}\n")

    print("=" * 70)
    print("2. QUERY DEMO: Identify Top-Rated Camps (Aggregation Pipeline)")
    print("=" * 70)
    top_camps = get_top_rated_camps()
    for rank, c in enumerate(top_camps, 1):
        print(f"Rank {rank}: Camp ID {c['camp_id']} | Avg Score: {c['avg_overall_score']}/5.0 | "
              f"Reviews: {c['review_count']} | Recommend: {c['recommendation_pct']}%")
        print(f"   Detail: Friendliness {c['avg_staff_friendliness']}/5.0 | Hygiene {c['avg_hygiene_safety']}/5.0 | "
              f"Speed {c['avg_registration_speed']}/5.0\n")

    print("=" * 70)
    print("3. QUERY DEMO: Search Emergency Appeals by Blood Group ('O-') & Keyword ('trauma')")
    print("=" * 70)
    results = search_emergency_appeals(blood_group="O-", keyword="trauma")
    for a in results:
        print(f"[{a['appeal_id']}] {a['urgency']} - Blood Group: {a['blood_group']} ({a['units_required']} Units)")
        print(f"Hospital: {a['hospital_name']}, {a['city']}")
        print(f"Condition: {a['patient_condition']}")
        print(f"Community Q&A entries: {len(a.get('community_qa', []))}")
        for qa in a.get('community_qa', []):
            print(f"   Q by {qa['user_name']}: {qa['message']}")
            print(f"   A: {qa['reply']}")
        print()

    print("=" * 70)
    print("3B. QUERY DEMO: Search Emergency Appeals by Keyword ('platelet')")
    print("=" * 70)
    platelet_appeals = search_emergency_appeals(keyword="platelet")
    for a in platelet_appeals:
        print(f"[{a['appeal_id']}] {a['hospital_name']} needs {a['blood_group']} ({a['units_required']} Units)")
        print(f"Condition: {a['patient_condition']}\n")
