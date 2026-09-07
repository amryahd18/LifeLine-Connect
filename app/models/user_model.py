"""
Project: LifeLine Connect (Blood Bank Network)
Component: User Authentication Model (Oracle Database & werkzeug.security)
"""

from typing import Optional, Dict, Any, Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.oracle_db import query_one, execute_dml, get_oracle_conn
import oracledb

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    sql = """
        SELECT 
            user_id, username, email, full_name, role,
            donor_id, hospital_id, staff_id, created_at
        FROM USERS
        WHERE user_id = :id
    """
    return query_one(sql, [user_id])

def get_user_by_identifier(identifier: str) -> Optional[Dict[str, Any]]:
    """Looks up user by either username or email."""
    sql = """
        SELECT 
            user_id, username, email, password_hash, full_name, role,
            donor_id, hospital_id, staff_id, created_at
        FROM USERS
        WHERE LOWER(username) = LOWER(:id1) OR LOWER(email) = LOWER(:id2)
    """
    return query_one(sql, [identifier.strip(), identifier.strip()])

def authenticate_user(identifier: str, password: str) -> Optional[Dict[str, Any]]:
    """Verifies credentials and returns user dict without password hash if successful."""
    user = get_user_by_identifier(identifier)
    if not user:
        return None

    if check_password_hash(user["password_hash"], password):
        # Remove hash before returning to caller
        user.pop("password_hash", None)
        return user
    return None

def create_user(
    username: str,
    email: str,
    password: str,
    full_name: str,
    role: str = "DONOR",
    donor_id: Optional[int] = None,
    hospital_id: Optional[int] = None,
    staff_id: Optional[int] = None
) -> Tuple[Optional[int], str]:
    """Hashes password and inserts a new user record into Oracle USERS table."""
    username = username.strip().lower()
    email = email.strip().lower()
    role = role.strip().upper()

    if role not in ("ADMIN", "STAFF", "HOSPITAL", "DONOR"):
        role = "DONOR"

    # Check for existing username or email
    existing = get_user_by_identifier(username)
    if existing:
        return None, "Username already taken. Please select a different username."

    existing_email = get_user_by_identifier(email)
    if existing_email:
        return None, "An account with this email address already exists."

    pw_hash = generate_password_hash(password)

    sql = """
        INSERT INTO USERS (
            username, email, password_hash, full_name, role,
            donor_id, hospital_id, staff_id
        ) VALUES (
            :u, :e, :p, :f, :r, :did, :hid, :sid
        ) RETURNING user_id INTO :out_id
    """

    with get_oracle_conn() as conn:
        with conn.cursor() as cursor:
            out_id = cursor.var(oracledb.NUMBER)
            cursor.execute(sql, {
                "u": username,
                "e": email,
                "p": pw_hash,
                "f": full_name.strip(),
                "r": role,
                "did": donor_id,
                "hid": hospital_id,
                "sid": staff_id,
                "out_id": out_id
            })
            conn.commit()
            new_id = int(out_id.getvalue()[0])
            return new_id, "User registered successfully!"
