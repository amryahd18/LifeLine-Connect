"""
Project: LifeLine Connect (Blood Bank Network)
Component: Hospital & Blood Requests Data Model (Oracle Database)
"""

from typing import List, Dict, Any, Optional, Tuple
import oracledb
from app.models.oracle_db import get_oracle_conn, query_all, query_one, execute_dml

def get_all_hospitals() -> List[Dict[str, Any]]:
    sql = """
        SELECT 
            h.hospital_id,
            h.hospital_name,
            h.license_no,
            h.category,
            h.contact_person,
            h.phone,
            h.email,
            h.address,
            h.city,
            COUNT(br.request_id) AS total_requests
        FROM HOSPITALS h
        LEFT JOIN BLOOD_REQUESTS br ON h.hospital_id = br.hospital_id
        GROUP BY 
            h.hospital_id, h.hospital_name, h.license_no, h.category,
            h.contact_person, h.phone, h.email, h.address, h.city
        ORDER BY h.hospital_name ASC
    """
    return query_all(sql)

def get_blood_requests(
    status: Optional[str] = None,
    urgency: Optional[str] = None
) -> List[Dict[str, Any]]:
    sql = """
        SELECT 
            br.request_id,
            br.hospital_id,
            h.hospital_name,
            h.city AS hospital_city,
            br.blood_group,
            br.component_type,
            br.units_requested,
            br.units_fulfilled,
            (br.units_requested - br.units_fulfilled) AS units_pending,
            br.urgency_level,
            br.request_date,
            br.required_by_date,
            br.status,
            br.notes,
            COUNT(bd.dispatch_id) AS dispatch_count
        FROM BLOOD_REQUESTS br
        JOIN HOSPITALS h ON br.hospital_id = h.hospital_id
        LEFT JOIN BLOOD_DISPATCHES bd ON br.request_id = bd.request_id
        WHERE 1=1
    """
    params = []
    if status and status.strip():
        sql += " AND br.status = :st"
        params.append(status.strip().upper())
    if urgency and urgency.strip():
        sql += " AND br.urgency_level = :urg"
        params.append(urgency.strip().upper())

    sql += """
        GROUP BY 
            br.request_id, br.hospital_id, h.hospital_name, h.city,
            br.blood_group, br.component_type, br.units_requested,
            br.units_fulfilled, br.urgency_level, br.request_date,
            br.required_by_date, br.status, br.notes
        ORDER BY 
            CASE br.urgency_level 
                WHEN 'CRITICAL_EMERGENCY' THEN 1 
                WHEN 'URGENT' THEN 2 
                ELSE 3 
            END ASC,
            br.request_date DESC
    """
    return query_all(sql, params)

def create_blood_request(data: Dict[str, Any]) -> int:
    sql = """
        INSERT INTO BLOOD_REQUESTS (
            hospital_id, blood_group, component_type, units_requested,
            urgency_level, request_date, required_by_date, units_fulfilled,
            status, notes
        ) VALUES (
            :hid, :bg, :comp, :units,
            :urg, TRUNC(SYSDATE), TO_DATE(:req_by, 'YYYY-MM-DD'), 0,
            'PENDING', :notes
        )
    """
    return execute_dml(sql, [
        int(data["hospital_id"]),
        data["blood_group"],
        data.get("component_type", "WHOLE_BLOOD"),
        int(data["units_requested"]),
        data.get("urgency_level", "NORMAL"),
        data["required_by_date"],
        data.get("notes", "Urgent clinical requirement.")
    ])

def fulfill_blood_request(
    request_id: int,
    staff_id: int = 3006,
    transporter: str = "LifeLine Rapid Dispatch"
) -> Tuple[int, str, str]:
    """Executes FEFO fulfillment via PKG_LIFELINE_CORE.sp_fulfill_hospital_request."""
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            o_units = cursor.var(oracledb.NUMBER)
            o_stat = cursor.var(str)
            o_msg = cursor.var(str)

            cursor.callproc("PKG_LIFELINE_CORE.sp_fulfill_hospital_request", [
                int(request_id),
                int(staff_id),
                transporter,
                o_units,
                o_stat,
                o_msg
            ])
            conn.commit()
            return int(o_units.getvalue() or 0), o_stat.getvalue(), o_msg.getvalue()

def get_dispatch_history() -> List[Dict[str, Any]]:
    sql = """
        SELECT 
            bd.dispatch_id,
            bd.request_id,
            bd.unit_id,
            bd.dispatch_date,
            bd.transporter_name,
            bd.delivery_status,
            bd.dispatch_notes,
            h.hospital_name,
            h.city AS destination_city,
            bi.blood_group,
            bi.component_type,
            s.first_name || ' ' || s.last_name AS authorized_by
        FROM BLOOD_DISPATCHES bd
        JOIN BLOOD_REQUESTS br ON bd.request_id = br.request_id
        JOIN HOSPITALS h ON br.hospital_id = h.hospital_id
        JOIN BLOOD_INVENTORY bi ON bd.unit_id = bi.unit_id
        LEFT JOIN STAFF s ON bd.dispatched_by = s.staff_id
        ORDER BY bd.dispatch_date DESC
    """
    return query_all(sql)
