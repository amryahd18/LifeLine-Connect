"""
Project: LifeLine Connect (Blood Bank Network)
Component: Oracle PL/SQL Business Reports Model
"""

from typing import List, Dict, Any, Tuple
import oracledb
from app.models.oracle_db import get_oracle_conn

def get_report1_camps_collections() -> List[Dict[str, Any]]:
    """Report 1: Total Blood Units Collected by Blood Group Across Camps."""
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            ref_cur = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_camps_collections", oracledb.DB_TYPE_CURSOR)
            columns = [col[0].lower() for col in ref_cur.description]
            rows = ref_cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]

def get_report2_inventory_expiring(days_ahead: int = 7) -> List[Dict[str, Any]]:
    """Report 2: Blood Inventory Levels and Identification of Expiring Units."""
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            ref_cur = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_inventory_expiring", oracledb.DB_TYPE_CURSOR, [int(days_ahead)])
            columns = [col[0].lower() for col in ref_cur.description]
            rows = ref_cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]

def get_report3_donor_history(donor_id: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Report 3: Individual Donor Eligibility and Donation History Summaries."""
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            ref_sum = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_donor_summary", oracledb.DB_TYPE_CURSOR, [int(donor_id)])
            sum_cols = [col[0].lower() for col in ref_sum.description]
            sum_row = ref_sum.fetchone()
            summary = dict(zip(sum_cols, sum_row)) if sum_row else {}

            ref_hist = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_donor_history", oracledb.DB_TYPE_CURSOR, [int(donor_id)])
            hist_cols = [col[0].lower() for col in ref_hist.description]
            hist_rows = ref_hist.fetchall()
            history = [dict(zip(hist_cols, r)) for r in hist_rows]

            return summary, history

def get_report4_hospital_fulfillment() -> List[Dict[str, Any]]:
    """Report 4: Hospital Blood Demand & Fulfillment Efficiency."""
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            ref_cur = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_hospital_fulfillment", oracledb.DB_TYPE_CURSOR)
            columns = [col[0].lower() for col in ref_cur.description]
            rows = ref_cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]

def get_report5_staff_workload() -> List[Dict[str, Any]]:
    """Report 5: Staff & Volunteer Deployment and Operational Workload Report."""
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            ref_cur = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_staff_workload", oracledb.DB_TYPE_CURSOR)
            columns = [col[0].lower() for col in ref_cur.description]
            rows = ref_cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]
