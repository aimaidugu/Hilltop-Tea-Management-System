"""
Database initialization endpoint for Vercel.

Access this endpoint to initialize the database tables and default admin user.
"""

import os
from flask import jsonify, request
from app import create_app, db
from app.models import User, Employee, UserRole

app = create_app()

@app.route('/api/init-db', methods=['POST'])
def init_database():
    """
    Initialize database with tables and default admin.

    Returns:
        JSON response with initialization status
    """
    try:
        # Create all tables
        db.create_all()

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

            return jsonify({
                'status': 'success',
                'message': 'Database initialized successfully',
                'admin_created': True,
                'admin_username': 'admin',
                'admin_password': 'admin123'
            }), 200
        else:
            return jsonify({
                'status': 'success',
                'message': 'Database already initialized',
                'admin_created': False
            }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
