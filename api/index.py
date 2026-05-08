"""
Simplified Vercel serverless function entry point for Hilltop Tea application.

This version removes WeasyPrint dependency for easier deployment.
"""

import os
from app import create_app

# Create the Flask application
app = create_app()

# Vercel requires the app to be available at module level
wsgi_app = app

# For Vercel serverless functions
def handler(request):
    """
    Vercel serverless function handler.

    Args:
        request: The incoming request object

    Returns:
        Response from the Flask application
    """
    return app(request.environ, lambda status, headers: None)
