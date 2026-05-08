"""
Production launcher for Hilltop Tea application.

Uses Waitress WSGI server for production deployment.
"""

import os
from waitress import serve
from app import create_app

# Create the Flask application
app = create_app()

# Get configuration from environment variables
host = os.environ.get('HOST', '0.0.0.0')
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    print(f"""
    ============================================
    HILLTOP TEA - Premium Nigerian Tea Factory
    ============================================
    Starting production server...
    Host: {host}
    Port: {port}
    ============================================
    """)

    # Serve with Waitress
    serve(app, host=host, port=port)
