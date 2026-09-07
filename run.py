"""
Project: LifeLine Connect (Blood Bank Network)
Component: Application Entry Point
"""

import sys
import os

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

app = create_app()

if __name__ == "__main__":
    print("=" * 70)
    print("Starting LifeLine Connect Blood Bank Network (Flask MVC)")
    print("Connecting to:")
    print("  - Oracle 21c Database: localhost:1521/XEPDB1 (Schema: LIFELINE_USER)")
    print("  - MongoDB 8.0 Database: mongodb://localhost:27017/lifeline_connect")
    print("URL: http://127.0.0.1:5000")
    print("=" * 70)
    app.run(host="127.0.0.1", port=5000, debug=True)
