"""
Hilltop Tea Application Factory.

Creates and configures the Flask application with all blueprints,
database, and extensions.
"""

from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
import os

# Initialize extensions
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


def create_app(config_name=None):
    """
    Application factory function.

    Creates and configures the Flask application with all blueprints
    and extensions registered.

    Args:
        config_name: Optional configuration name (not used, reads from config.py)

    Returns:
        Flask: Configured application instance
    """
    app = Flask(__name__)

    # Load configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    # Initialize extensions with app
    from app.models import db
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.auth import auth_bp
    from app.employees import employees_bp
    from app.production import production_bp
    from app.payroll import payroll_bp
    from app.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(production_bp, url_prefix='/production')
    app.register_blueprint(payroll_bp, url_prefix='/payroll')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    # Register error handlers
    register_error_handlers(app)

    # Register context processors
    register_context_processors(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login."""
        from app.models import User
        return User.query.get(int(user_id))

    # Create database tables
    with app.app_context():
        db.create_all()
        create_default_admin()

    # Root route
    @app.route('/')
    def index():
        """Redirect to dashboard or login based on authentication."""
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('production.dashboard'))
        return redirect(url_for('auth.login'))

    return app


def create_default_admin():
    """
    Create default admin user if none exists.

    This ensures the application has at least one admin user
    for initial setup.
    """
    from app.models import User
    from config import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD

    if not User.query.filter_by(username=DEFAULT_ADMIN_USERNAME).first():
        admin = User(
            username=DEFAULT_ADMIN_USERNAME,
            role='admin'
        )
        admin.set_password(DEFAULT_ADMIN_PASSWORD)
        from app.models import db
        db.session.add(admin)
        db.session.commit()


def register_error_handlers(app):
    """
    Register custom error handlers for the application.

    Args:
        app: Flask application instance
    """

    @app.errorhandler(403)
    def forbidden(e):
        """Handle 403 Forbidden errors."""
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 Not Found errors."""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 Internal Server errors."""
        from flask import flash
        flash('An internal error occurred. Please try again.', 'danger')
        return render_template('errors/500.html'), 500


def register_context_processors(app):
    """
    Register context processors for template variables.

    Args:
        app: Flask application instance
    """

    @app.context_processor
    def utility_processor():
        """Make utility functions available in templates."""
        from app.utils import format_currency, format_date, get_month_name
        return dict(
            format_currency=format_currency,
            format_date=format_date,
            get_month_name=get_month_name
        )
