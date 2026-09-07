"""
Project: LifeLine Connect (Blood Bank Network)
Component: Camp Data Model (Oracle Database)
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models.oracle_db import query_all, query_one, execute_dml

def get_all_camps(status: Optional[str] = None) -> List[Dict[str, Any]]:
    sql = """
        SELECT 
            c.camp_id,
            c.camp_name,
            c.organizer_name,
            c.venue_address,
            c.city,
            c.start_date,
            c.end_date,
            c.target_units,
            c.status,
            NVL(SUM(dr.units_donated), 0) AS units_collected,
            COUNT(DISTINCT dr.donation_id) AS total_donations,
            COUNT(DISTINCT sa.staff_id) AS staff_count
        FROM CAMPS c
        LEFT JOIN DONATION_RECORDS dr ON c.camp_id = dr.camp_id AND dr.screening_status = 'PASSED'
        LEFT JOIN STAFF_ASSIGNMENTS sa ON c.camp_id = sa.camp_id
        WHERE 1=1
    """
    params = []
    if status and status.strip():
        sql += " AND c.status = :st"
        params.append(status.strip().upper())

    sql += """
        GROUP BY 
            c.camp_id, c.camp_name, c.organizer_name, c.venue_address,
            c.city, c.start_date, c.end_date, c.target_units, c.status
        ORDER BY c.start_date DESC
    """
    return query_all(sql, params)

def get_camp_by_id(camp_id: int) -> Optional[Dict[str, Any]]:
    sql = """
        SELECT 
            c.camp_id,
            c.camp_name,
            c.organizer_name,
            c.venue_address,
            c.city,
            c.start_date,
            c.end_date,
            c.target_units,
            c.status,
            NVL(SUM(dr.units_donated), 0) AS units_collected,
            COUNT(DISTINCT dr.donation_id) AS total_donations
        FROM CAMPS c
        LEFT JOIN DONATION_RECORDS dr ON c.camp_id = dr.camp_id AND dr.screening_status = 'PASSED'
        WHERE c.camp_id = :id
        GROUP BY 
            c.camp_id, c.camp_name, c.organizer_name, c.venue_address,
            c.city, c.start_date, c.end_date, c.target_units, c.status
    """
    return query_one(sql, [camp_id])

def get_camp_staff(camp_id: int) -> List[Dict[str, Any]]:
    sql = """
        SELECT 
            sa.assignment_id,
            sa.role_assigned,
            sa.shift_date,
            sa.hours_worked,
            sa.status AS shift_status,
            s.staff_id,
            s.first_name || ' ' || s.last_name AS staff_name,
            s.role AS primary_role,
            s.phone,
            s.email
        FROM STAFF_ASSIGNMENTS sa
        JOIN STAFF s ON sa.staff_id = s.staff_id
        WHERE sa.camp_id = :id
        ORDER BY sa.shift_date ASC, s.first_name ASC
    """
    return query_all(sql, [camp_id])

def create_camp(data: Dict[str, Any]) -> int:
    sql = """
        INSERT INTO CAMPS (
            camp_name, organizer_name, venue_address, city,
            start_date, end_date, target_units, status
        ) VALUES (
            :name, :organizer, :venue, :city,
            TO_DATE(:start_d, 'YYYY-MM-DD'), TO_DATE(:end_d, 'YYYY-MM-DD'),
            :target, :status
        )
    """
    return execute_dml(sql, [
        data["camp_name"],
        data["organizer_name"],
        data["venue_address"],
        data["city"],
        data["start_date"],
        data["end_date"],
        int(data.get("target_units", 50)),
        data.get("status", "UPCOMING")
    ])
