"""
Project: LifeLine Connect (Blood Bank Network)
Component: Live Database Explorer & SQL Schema Studio Controller
"""

import re
from flask import Blueprint, render_template, request, jsonify
from app.models.oracle_db import get_oracle_conn, query_all
from app.models.mongo_db import get_mongo_db
from app.config import Config

database_bp = Blueprint("database", __name__, url_prefix="/database")

@database_bp.route("/")
def index():
    """Main database explorer dashboard."""
    selected_table = request.args.get("table", "DONORS").upper().strip()
    
    # Get Oracle Version & Connection Info
    oracle_info = {
        "user": Config.ORACLE_USER,
        "dsn": Config.ORACLE_DSN,
        "product": "Oracle Database 21c Express Edition",
        "version": "21.3.0.0.0",
        "schema": "LIFELINE_USER",
        "service": "XEPDB1",
        "pool_status": "ACTIVE"
    }
    
    # Get all Oracle tables and live row counts
    tables_list = []
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT t.table_name, t.num_rows
                    FROM user_tables t
                    ORDER BY t.table_name
                """)
                for row in cursor.fetchall():
                    t_name = row[0]
                    # Get fresh exact count
                    cursor.execute(f"SELECT COUNT(*) FROM {t_name}")
                    cnt = cursor.fetchone()[0]
                    tables_list.append({"name": t_name, "count": cnt})
            except Exception as e:
                print(f"Error reading tables: {e}")

    # Validate selected table against existing tables
    valid_names = [t["name"] for t in tables_list]
    if selected_table not in valid_names and valid_names:
        selected_table = valid_names[0]

    # Get metadata and rows for selected table
    columns = []
    rows = []
    pk_columns = []
    if selected_table in valid_names:
        with get_oracle_conn() as conn:
            with conn.cursor() as cursor:
                # 1. Primary Keys
                try:
                    cursor.execute("""
                        SELECT cols.column_name
                        FROM user_constraints cons
                        JOIN user_cons_columns cols ON cons.constraint_name = cols.constraint_name
                        WHERE cons.constraint_type = 'P' AND cons.table_name = :t
                    """, [selected_table])
                    pk_columns = [r[0] for r in cursor.fetchall()]
                except Exception:
                    pk_columns = []

                # 2. Columns definition
                try:
                    cursor.execute("""
                        SELECT column_name, data_type, data_length, nullable
                        FROM user_tab_columns
                        WHERE table_name = :t
                        ORDER BY column_id
                    """, [selected_table])
                    for r in cursor.fetchall():
                        col_name = r[0]
                        columns.append({
                            "name": col_name,
                            "type": r[1],
                            "length": r[2],
                            "nullable": r[3] == "Y",
                            "is_pk": col_name in pk_columns
                        })
                except Exception as e:
                    print(f"Error loading columns: {e}")

                # 3. First 50 rows
                try:
                    cursor.execute(f"SELECT * FROM {selected_table} FETCH FIRST 50 ROWS ONLY")
                    col_names = [c[0].lower() for c in cursor.description]
                    for r in cursor.fetchall():
                        # Format dates nicely
                        row_dict = {}
                        for i, val in enumerate(r):
                            c_name = col_names[i]
                            if hasattr(val, "isoformat"):
                                row_dict[c_name] = val.strftime("%Y-%m-%d %H:%M")
                            else:
                                row_dict[c_name] = str(val) if val is not None else "NULL"
                        rows.append(row_dict)
                except Exception as e:
                    print(f"Error loading rows: {e}")

    # MongoDB collections summary
    mongo_collections = []
    try:
        mdb = get_mongo_db()
        for col_name in ["campaign_media", "camp_feedback", "emergency_appeals"]:
            cnt = mdb[col_name].count_documents({})
            sample = list(mdb[col_name].find().limit(2))
            # Convert ObjectId and datetime for display
            clean_sample = []
            for s in sample:
                s["_id"] = str(s["_id"])
                for k, v in s.items():
                    if hasattr(v, "isoformat"):
                        s[k] = v.isoformat()
                clean_sample.append(s)
            mongo_collections.append({
                "name": col_name,
                "count": cnt,
                "sample": clean_sample
            })
    except Exception as e:
        print(f"MongoDB summary error: {e}")

    return render_template(
        "database/index.html",
        oracle_info=oracle_info,
        tables_list=tables_list,
        selected_table=selected_table,
        columns=columns,
        rows=rows,
        mongo_collections=mongo_collections
    )

@database_bp.route("/api/query", methods=["POST"])
def execute_query():
    """Executes SQL statements (SELECT, INSERT, UPDATE, DELETE, MERGE) against Oracle."""
    req_json = request.get_json(silent=True) or {}
    sql = req_json.get("sql", "").strip()

    if not sql:
        return jsonify({"success": False, "error": "Query cannot be empty."}), 400

    # Clean trailing semicolons and normalize
    cleaned_sql = sql.rstrip(';').strip()
    first_word = cleaned_sql.split()[0].upper() if cleaned_sql.split() else ""

    # Permitted SQL statements
    allowed_verbs = ["SELECT", "INSERT", "UPDATE", "DELETE", "MERGE", "CREATE"]
    if first_word not in allowed_verbs:
        return jsonify({
            "success": False,
            "error": f"Security restriction: Command '{first_word}' is not allowed. Permitted commands: {', '.join(allowed_verbs)}."
        }), 400

    # Safeguard against accidental structural drop of entire tables/schema
    destructive_structural = ["DROP", "TRUNCATE", "ALTER"]
    for f in destructive_structural:
        if re.search(r'\b' + f + r'\b', cleaned_sql, re.IGNORECASE):
            return jsonify({
                "success": False,
                "error": f"Security restriction: Structural DDL command '{f}' is disabled. Data operations (SELECT, INSERT, UPDATE, DELETE) are fully enabled."
            }), 400

    try:
        with get_oracle_conn() as conn:
            with conn.cursor() as cursor:
                if first_word == "SELECT":
                    # Add limit if user didn't specify
                    run_sql = cleaned_sql
                    if "FETCH FIRST" not in run_sql.upper() and "ROWNUM" not in run_sql.upper():
                        run_sql = f"{run_sql} FETCH FIRST 100 ROWS ONLY"
                    
                    cursor.execute(run_sql)
                    if not cursor.description:
                        return jsonify({"success": True, "action": "SELECT", "columns": [], "rows": [], "count": 0})
                    
                    cols = [col[0] for col in cursor.description]
                    raw_rows = cursor.fetchall()
                    
                    formatted_rows = []
                    for r in raw_rows:
                        row_data = []
                        for val in r:
                            if hasattr(val, "isoformat"):
                                row_data.append(val.strftime("%Y-%m-%d %H:%M"))
                            else:
                                row_data.append(str(val) if val is not None else "NULL")
                        formatted_rows.append(row_data)

                    return jsonify({
                        "success": True,
                        "action": "SELECT",
                        "columns": cols,
                        "rows": formatted_rows,
                        "count": len(formatted_rows),
                        "sql": run_sql
                    })
                else:
                    # DML Command: INSERT, UPDATE, DELETE, MERGE
                    cursor.execute(cleaned_sql)
                    affected = cursor.rowcount
                    conn.commit()
                    return jsonify({
                        "success": True,
                        "action": first_word,
                        "rows_affected": affected,
                        "count": affected,
                        "message": f"Successfully executed {first_word}. {affected} row(s) affected and committed to Oracle 21c.",
                        "sql": cleaned_sql
                    })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
