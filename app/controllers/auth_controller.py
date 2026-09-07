"""
Project: LifeLine Connect (Blood Bank Network)
Component: Authentication Controller (Login, Register, Logout & Role Decorators)
"""

from functools import wraps
from flask import (
    Blueprint, render_template, request, redirect, url_for, session, flash, g
)
from app.models.user_model import authenticate_user, create_user, get_user_by_id
from app.models.donor_model import get_all_donors
from app.models.hospital_model import get_all_hospitals

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for("auth.login", next=request.url))
            user_role = session.get("role", "DONOR")
            if user_role not in allowed_roles:
                flash(f"Access restricted. Required role: {', '.join(allowed_roles)}.", "danger")
                return redirect(url_for("main.dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")
        next_url = request.args.get("next") or url_for("main.dashboard")

        if not identifier or not password:
            flash("Please provide both username/email and password.", "warning")
            return render_template("auth/login.html")

        user = authenticate_user(identifier, password)
        if user:
            session.clear()
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]
            session["donor_id"] = user["donor_id"]
            session["hospital_id"] = user["hospital_id"]
            session["staff_id"] = user["staff_id"]

            flash(f"Welcome back, {user['full_name']} ({user['role']})!", "success")
            return redirect(next_url)
        else:
            flash("Invalid credentials. Please verify your username/email and password.", "danger")

    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "DONOR").strip().upper()

        if password != confirm_password:
            flash("Passwords do not match. Please re-enter.", "warning")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "warning")
            return render_template("auth/register.html")

        user_id, message = create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            role=role
        )

        if user_id:
            # Auto login the new user
            session.clear()
            session["user_id"] = user_id
            session["username"] = username.lower()
            session["full_name"] = full_name
            session["role"] = role

            flash(f"Account created successfully! Welcome to LifeLine Connect, {full_name}.", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash(f"Registration Error: {message}", "danger")

    return render_template("auth/register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out securely.", "info")
    return redirect(url_for("auth.login"))
