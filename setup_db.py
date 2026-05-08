"""
Database initialization script for Vercel deployment.

Run this after first deployment to create tables and default admin.
"""

import os
from app import create_app, db
from app.models import User, Employee, UserRole

def init_database():
    """Initialize database with tables and default admin."""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")

        # Create default admin if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                role=UserRole.ADMIN.value
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created")
            print("   Username: admin")
            print("   Password: admin123")
            print("   ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!")
        else:
            print("ℹ️  Admin user already exists")

        print("\n✅ Database initialization complete!")

if __name__ == '__main__':
    init_database()
