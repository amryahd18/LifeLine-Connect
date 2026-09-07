"""
Project: LifeLine Connect (Blood Bank Network)
Component: Inventory & Donation Collection Data Model (Oracle Database)
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import oracledb
from app.models.oracle_db import get_oracle_conn, query_all, query_one

def get_inventory_summary() -> Dict[str, Any]:
    """Returns matrix of blood groups by component type and totals."""
    sql = """
        SELECT 
            blood_group,
            COUNT(CASE WHEN status = 'AVAILABLE' THEN 1 END) AS available_units,
            COUNT(CASE WHEN status = 'RESERVED' THEN 1 END) AS reserved_units,
            COUNT(CASE WHEN status = 'EXPIRED' THEN 1 END) AS expired_units,
            COUNT(CASE WHEN status = 'TRANSFUSED' THEN 1 END) AS transfused_units,
            COUNT(CASE WHEN component_type = 'WHOLE_BLOOD' AND status = 'AVAILABLE' THEN 1 END) AS whole_blood,
            COUNT(CASE WHEN component_type = 'RBC' AND status = 'AVAILABLE' THEN 1 END) AS rbc,
            COUNT(CASE WHEN component_type = 'PLATELETS' AND status = 'AVAILABLE' THEN 1 END) AS platelets,
            COUNT(CASE WHEN component_type = 'PLASMA' AND status = 'AVAILABLE' THEN 1 END) AS plasma,
            COUNT(*) AS total_units
        FROM BLOOD_INVENTORY
        GROUP BY blood_group
        ORDER BY blood_group
    """
    rows = query_all(sql)
    
    # Calculate overall KPIs
    total_avail = sum(r["available_units"] for r in rows)
    total_exp = sum(r["expired_units"] for r in rows)
    total_trans = sum(r["transfused_units"] for r in rows)

    return {
        "groups": rows,
        "total_available": total_avail,
        "total_expired": total_exp,
        "total_transfused": total_trans
    }

def get_all_inventory_units(
    blood_group: Optional[str] = None,
    component: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict[str, Any]]:
    sql = """
        SELECT 
            bi.unit_id,
            bi.donation_id,
            bi.blood_group,
            bi.component_type,
            bi.collection_date,
            bi.expiration_date,
            bi.storage_location,
            bi.status,
            ROUND(bi.expiration_date - TRUNC(SYSDATE)) AS days_remaining,
            d.donor_id,
            d.first_name || ' ' || d.last_name AS donor_name
        FROM BLOOD_INVENTORY bi
        JOIN DONATION_RECORDS dr ON bi.donation_id = dr.donation_id
        JOIN DONORS d ON dr.donor_id = d.donor_id
        WHERE 1=1
    """
    params = []
    if blood_group and blood_group.strip():
        sql += " AND bi.blood_group = :bg"
        params.append(blood_group.strip())
    if component and component.strip():
        sql += " AND bi.component_type = :comp"
        params.append(component.strip())
    if status and status.strip():
        sql += " AND bi.status = :st"
        params.append(status.strip().upper())

    sql += " ORDER BY bi.expiration_date ASC"
    return query_all(sql, params)

def record_donation(data: Dict[str, Any]) -> Tuple[Optional[int], Optional[int], str]:
    """Records donation and generates inventory unit via PKG_LIFELINE_CORE.sp_record_donation."""
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            o_don_id = cursor.var(oracledb.NUMBER)
            o_unit_id = cursor.var(oracledb.NUMBER)
            o_msg = cursor.var(str)

            camp_id = data.get("camp_id")
            if camp_id and str(camp_id).strip():
                camp_id = int(camp_id)
            else:
                camp_id = None

            cursor.callproc("PKG_LIFELINE_CORE.sp_record_donation", [
                int(data["donor_id"]),
                camp_id,
                int(data["blood_pressure_sys"]),
                int(data["blood_pressure_dia"]),
                int(data["pulse_rate"]),
                float(data["hemoglobin_reading"]),
                data.get("component_type", "WHOLE_BLOOD"),
                data.get("storage_location", "Main Cold Storage / Shelf 1"),
                data.get("notes", "Routine donation accepted."),
                o_don_id,
                o_unit_id,
                o_msg
            ])
            conn.commit()
            return o_don_id.getvalue(), o_unit_id.getvalue(), o_msg.getvalue()
