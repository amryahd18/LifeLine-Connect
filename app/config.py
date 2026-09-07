"""
Project: LifeLine Connect (Blood Bank Network)
Component: Configuration Module
"""

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "lifeline-secret-key-production-2026")
    
    # Oracle Database Settings
    ORACLE_USER = os.environ.get("ORACLE_USER", "lifeline_user")
    ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", "Lifeline123#")
    ORACLE_DSN = os.environ.get("ORACLE_DSN", "localhost:1521/XEPDB1")
    ORACLE_POOL_MIN = 2
    ORACLE_POOL_MAX = 10
    ORACLE_POOL_INC = 1

    # MongoDB Settings
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB = os.environ.get("MONGO_DB", "lifeline_connect")

    # Flask Settings
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
