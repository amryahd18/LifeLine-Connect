"""
Project: LifeLine Connect (Blood Bank Network)
Component: Donor Data Model (Oracle Database)
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import oracledb
from app.models.oracle_db import get_oracle_conn, query_all, query_one

def get_all_donors(
    blood_group: Optional[str] = None,
    eligibility: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    sql = """
        SELECT 
            d.donor_id,
            d.first_name,
            d.last_name,
            d.email,
            d.phone,
            d.date_of_birth,
            d.gender,
            d.blood_group,
            d.rh_factor,
            d.weight_kg,
            d.hemoglobin_level,
            d.eligibility_status,
            d.last_donation_date,
            d.next_eligible_date,
            d.city,
            COUNT(dr.donation_id) AS total_donations
        FROM DONORS d
        LEFT JOIN DONATION_RECORDS dr ON d.donor_id = dr.donor_id
        WHERE 1=1
    """
    params = []
    if blood_group and blood_group.strip():
        sql += " AND d.blood_group = :bg"
        params.append(blood_group.strip())
    if eligibility and eligibility.strip():
        sql += " AND d.eligibility_status = :el"
        params.append(eligibility.strip())
    if search and search.strip():
        term = f"%{search.strip().lower()}%"
        sql += " AND (LOWER(d.first_name) LIKE :s1 OR LOWER(d.last_name) LIKE :s2 OR LOWER(d.city) LIKE :s3 OR LOWER(d.email) LIKE :s4)"
        params.extend([term, term, term, term])

    sql += """
        GROUP BY 
            d.donor_id, d.first_name, d.last_name, d.email, d.phone,
            d.date_of_birth, d.gender, d.blood_group, d.rh_factor,
            d.weight_kg, d.hemoglobin_level, d.eligibility_status,
            d.last_donation_date, d.next_eligible_date, d.city
        ORDER BY d.donor_id DESC
    """
    return query_all(sql, params)

def get_donor_by_id(donor_id: int) -> Optional[Dict[str, Any]]:
    sql = """
        SELECT 
            donor_id, first_name, last_name, email, phone,
            date_of_birth, gender, blood_group, rh_factor,
            weight_kg, hemoglobin_level, eligibility_status,
            last_donation_date, next_eligible_date, address, city, created_at
        FROM DONORS
        WHERE donor_id = :id
    """
    return query_one(sql, [donor_id])

def get_donor_donations(donor_id: int) -> List[Dict[str, Any]]:
    sql = """
        SELECT 
            dr.donation_id,
            dr.donation_date,
            dr.units_donated,
            dr.blood_pressure_sys,
            dr.blood_pressure_dia,
            dr.pulse_rate,
            dr.hemoglobin_reading,
            dr.screening_status,
            dr.tested_status,
            dr.notes,
            c.camp_id,
            NVL(c.camp_name, 'Central Blood Facility') AS camp_name
        FROM DONATION_RECORDS dr
        LEFT JOIN CAMPS c ON dr.camp_id = c.camp_id
        WHERE dr.donor_id = :id
        ORDER BY dr.donation_date DESC
    """
    return query_all(sql, [donor_id])

def check_donor_eligibility(donor_id: int) -> str:
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            res = cursor.callfunc("PKG_LIFELINE_CORE.fn_check_donor_eligibility", str, [donor_id])
            return res

def register_donor(donor_data: Dict[str, Any]) -> Tuple[Optional[int], str]:
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            o_id = cursor.var(oracledb.NUMBER)
            o_msg = cursor.var(str)
            
            dob_val = donor_data["date_of_birth"]
            if isinstance(dob_val, str):
                dob_val = datetime.strptime(dob_val, "%Y-%m-%d")

            cursor.callproc("PKG_LIFELINE_CORE.sp_register_donor", [
                donor_data["first_name"],
                donor_data["last_name"],
                donor_data["email"],
                donor_data["phone"],
                dob_val,
                donor_data["gender"],
                donor_data["blood_group"],
                donor_data["rh_factor"],
                float(donor_data["weight_kg"]),
                float(donor_data["hemoglobin_level"]),
                donor_data.get("address", ""),
                donor_data["city"],
                o_id,
                o_msg
            ])
            conn.commit()
            return o_id.getvalue(), o_msg.getvalue()
