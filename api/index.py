"""
Vercel serverless function entry point for Hilltop Tea application.

This file serves as the entry point for Vercel's serverless deployment.
"""

from app import create_app

# Create the Flask application
app = create_app()

# Vercel requires the app to be available at module level
# The WSGI application is exposed for Vercel to use
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
