"""
Project: LifeLine Connect (Blood Bank Network)
Component: Oracle Connection Pool & Database Access Layer
"""

from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import oracledb
from app.config import Config

_pool: Optional[oracledb.ConnectionPool] = None

def init_oracle_pool():
    global _pool
    if _pool is None:
        try:
            _pool = oracledb.create_pool(
                user=Config.ORACLE_USER,
                password=Config.ORACLE_PASSWORD,
                dsn=Config.ORACLE_DSN,
                min=Config.ORACLE_POOL_MIN,
                max=Config.ORACLE_POOL_MAX,
                increment=Config.ORACLE_POOL_INC
            )
            print("Oracle Connection Pool successfully initialized.")
        except Exception as e:
            print(f"Error initializing Oracle Connection Pool: {e}")
            raise

def close_oracle_pool():
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None
        print("Oracle Connection Pool closed.")

@contextmanager
def get_oracle_conn():
    global _pool
    if _pool is None:
        init_oracle_pool()
    conn = _pool.acquire()
    try:
        yield conn
    finally:
        _pool.release(conn)

def query_all(sql: str, params=None) -> List[Dict[str, Any]]:
    """Executes a SELECT query and returns rows as a list of dictionaries."""
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or [])
            columns = [col[0].lower() for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

def query_one(sql: str, params=None) -> Optional[Dict[str, Any]]:
    """Executes a SELECT query and returns the first row as a dictionary."""
    results = query_all(sql, params)
    return results[0] if results else None

def execute_dml(sql: str, params=None) -> int:
    """Executes an INSERT/UPDATE/DELETE statement and commits."""
    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or [])
            rowcount = cursor.rowcount
            conn.commit()
            return rowcount
