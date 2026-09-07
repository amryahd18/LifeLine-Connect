"""
Project: LifeLine Connect (Blood Bank Network)
Component: Application Factory
"""

from flask import Flask
from app.config import Config
from app.models.oracle_db import init_oracle_pool, close_oracle_pool

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Oracle DB Connection Pool
    with app.app_context():
        try:
            init_oracle_pool()
        except Exception as e:
            print(f"Warning: Could not initialize Oracle pool at startup: {e}")

    # Register Blueprints
    from app.controllers.main_controller import main_bp
    from app.controllers.donor_controller import donor_bp
    from app.controllers.camp_controller import camp_bp
    from app.controllers.inventory_controller import inventory_bp
    from app.controllers.hospital_controller import hospital_bp
    from app.controllers.appeal_controller import appeal_bp
    from app.controllers.report_controller import report_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.logistics_controller import logistics_bp
    from app.controllers.analytics_controller import analytics_bp
    from app.controllers.database_controller import database_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(donor_bp)
    app.register_blueprint(camp_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(appeal_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(logistics_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(database_bp)

    @app.context_processor
    def inject_user():
        from flask import session
        if "user_id" in session:
            return {
                "current_user": {
                    "id": session.get("user_id"),
                    "username": session.get("username"),
                    "full_name": session.get("full_name"),
                    "role": session.get("role")
                }
            }
        return {"current_user": None}

    # Template Filters
    @app.template_filter("format_date")
    def format_date(value, fmt="%b %d, %Y"):
        if not value:
            return "N/A"
        try:
            if hasattr(value, "strftime"):
                return value.strftime(fmt)
            return str(value)[:10]
        except Exception:
            return str(value)

    return app
