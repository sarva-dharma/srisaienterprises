"""
Bengaluru Building Plan Sanction & Architectural Liaisoning Service
Main Application Launcher
"""
import os
import sys

# Ensure current directory is in Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.database import db
from backend.seed_data import seed_database

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Ensure database tables exist
        db.create_all()
        # Seed initial data (admin, services, demo Sakala project, blogs)
        seed_database()

    port = int(os.environ.get('PORT', 5005))
    print("\n" + "="*70)
    print("  BENGALURU BUILDING PLAN SANCTION & ARCHITECTURAL LIAISONING SERVICE")
    print("  GBA 2026 & Nambike Nakshe Compliance Engine")
    print("="*70)
    print(f"  * Server running at: http://127.0.0.1:{port}")
    print(f"  * Admin Portal:     http://127.0.0.1:{port}/admin")
    print(f"  * Client Portal:    http://127.0.0.1:{port}/portal")
    print("  * Demo Admin Login:  admin@bengaluruapprovals.com / admin123")
    print("  * Demo Client Login: client@example.com / client123")
    print("  * Live Sakala Ref:   SAKALA-GBA-2026-0894")
    print("="*70 + "\n")

    app.run(host='0.0.0.0', port=port, debug=False)
