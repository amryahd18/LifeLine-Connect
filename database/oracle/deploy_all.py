"""
Project: LifeLine Connect (Blood Bank Network)
Component: Automated Deployment and Verification Suite for Oracle Database
Database: Oracle 21c Express Edition (XEPDB1)
Schema: LIFELINE_USER
"""

import sys
import oracledb

def clean_sql_block(block: str) -> str:
    lines = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith('--'):
            continue
        lines.append(line)
    return '\n'.join(lines).strip()

def run_script_file(cursor, filepath: str):
    print(f"Deploying: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If file contains PL/SQL blocks (packages, triggers, procedures) separated by /
    if "PACKAGE" in content.upper() or "TRIGGER" in content.upper() or "AUDIT_DISPATCH_LOG" in content:
        blocks = []
        current = []
        for line in content.splitlines():
            if line.strip() == '/':
                block = '\n'.join(current).strip()
                if block:
                    blocks.append(block)
                current = []
            else:
                current.append(line)
        if current:
            block = '\n'.join(current).strip()
            if block:
                blocks.append(block)

        for b in blocks:
            stmt = clean_sql_block(b)
            if not stmt:
                continue
            if not (stmt.upper().startswith('BEGIN') or stmt.upper().startswith('DECLARE')
                    or stmt.upper().startswith('CREATE OR REPLACE PACKAGE')
                    or stmt.upper().startswith('CREATE OR REPLACE TRIGGER')
                    or stmt.upper().startswith('CREATE OR REPLACE PROCEDURE')
                    or stmt.upper().startswith('CREATE OR REPLACE FUNCTION')):
                stmt = stmt.rstrip().rstrip(';')
            cursor.execute(stmt)
    else:
        # Standard SQL script with statements ending in ; or PL/SQL blocks ending in /
        statements = []
        buffer = []
        in_plsql = False
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith('--') or not stripped:
                continue
            if stripped.upper() in ('BEGIN', 'DECLARE'):
                in_plsql = True
            buffer.append(line)
            if in_plsql:
                if stripped == '/':
                    statements.append('\n'.join(buffer[:-1]))
                    buffer = []
                    in_plsql = False
            else:
                if stripped.endswith(';'):
                    stmt = '\n'.join(buffer).rstrip().rstrip(';')
                    statements.append(stmt)
                    buffer = []
        for s in statements:
            stmt = clean_sql_block(s)
            if stmt:
                cursor.execute(stmt)

def main():
    conn = oracledb.connect(user="lifeline_user", password="Lifeline123#", dsn="localhost:1521/XEPDB1")
    cursor = conn.cursor()

    scripts = [
        r"C:\Users\pc\.gemini\antigravity-ide\scratch\lifeline_connect\database\oracle\01_schema.sql",
        r"C:\Users\pc\.gemini\antigravity-ide\scratch\lifeline_connect\database\oracle\02_sample_data.sql",
        r"C:\Users\pc\.gemini\antigravity-ide\scratch\lifeline_connect\database\oracle\03_procedures_functions.sql",
        r"C:\Users\pc\.gemini\antigravity-ide\scratch\lifeline_connect\database\oracle\04_triggers.sql",
        r"C:\Users\pc\.gemini\antigravity-ide\scratch\lifeline_connect\database\oracle\05_business_reports.sql",
        r"C:\Users\pc\.gemini\antigravity-ide\scratch\lifeline_connect\database\oracle\06_auth_schema.sql"
    ]

    for s in scripts:
        run_script_file(cursor, s)
        conn.commit()

    # Verify compiler status
    cursor.execute("""
        SELECT name, type, line, position, text 
        FROM user_errors 
        WHERE name NOT LIKE 'BIN$%'
        ORDER BY name, sequence
    """)
    errors = cursor.fetchall()
    if errors:
        print("\nCOMPILATION ERRORS DETECTED:")
        for err in errors:
            print(f"[{err[0]} {err[1]}] Line {err[2]}:{err[3]} - {err[4]}")
        sys.exit(1)

    print("\n======================================================================")
    print("ALL ORACLE DDL, DML, PACKAGES, TRIGGERS & REPORTS COMPILED CLEANLY (0 ERRORS)!")
    print("======================================================================")

    # =========================================================================
    # VERIFY THE 5 BUSINESS REPORTS VIA PL/SQL REFCURSORS
    # =========================================================================
    print("\n--- [REPORT 1] Blood Units Collected Across Camps by Blood Group ---")
    c1 = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_camps_collections", oracledb.DB_TYPE_CURSOR)
    for row in c1.fetchall()[:5]:
        print(f"Camp: {row[0]:32} | Group: {row[3]:3} | Units: {row[5]} | Donors: {row[6]}")

    print("\n--- [REPORT 2] Inventory Levels & Units Expiring within 7 Days ---")
    c2 = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_inventory_expiring", oracledb.DB_TYPE_CURSOR, [7])
    for row in c2.fetchall():
        print(f"Unit ID: {row[0]} | Group: {row[1]:3} | Comp: {row[2]:12} | Expiry: {str(row[5])[:10]} | Days Left: {row[7]} | {row[8]}")

    print("\n--- [REPORT 3] Individual Donor Eligibility & Donation History (Donor 1001) ---")
    c3_sum = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_donor_summary", oracledb.DB_TYPE_CURSOR, [1001])
    summary_data = c3_sum.fetchone()
    c3_hist = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_donor_history", oracledb.DB_TYPE_CURSOR, [1001])
    history_data = c3_hist.fetchall()
    print(f"Donor: {summary_data[1]} | Group: {summary_data[4]}{summary_data[5]} | Status: {summary_data[8]} | Lifetime Donations: {summary_data[12]}")
    for h in history_data:
        print(f"   Donation #{h[0]} on {str(h[1])[:10]} at {h[2]:30} | Hb: {h[6]} | Status: {h[7]}")

    print("\n--- [REPORT 4] Hospital Demand & Fulfillment Efficiency ---")
    c4 = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_hospital_fulfillment", oracledb.DB_TYPE_CURSOR)
    for row in c4.fetchall():
        print(f"Hospital: {row[1]:34} | Demanded: {row[5]:2} | Fulfilled: {row[6]:2} | Rate: {row[8]}% | Emergencies: {row[9]}")

    print("\n--- [REPORT 5] Staff Deployment & Workload Summary ---")
    c5 = cursor.callfunc("PKG_LIFELINE_REPORTS.fn_report_staff_workload", oracledb.DB_TYPE_CURSOR)
    for row in c5.fetchall():
        print(f"Staff: {row[1]:20} | Role: {row[2]:14} | Shifts: {row[5]}/{row[6]} | Hours: {row[7]} hrs | Compliance: {row[9]}%")

    conn.close()
    print("\nALL VERIFICATIONS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
