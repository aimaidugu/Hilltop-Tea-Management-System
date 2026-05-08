"""
Configuration module for Hilltop Tea application.

Contains all configuration constants and settings.
"""

import os
from datetime import timedelta

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Security
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hilltop-tea-secret-key-change-in-production-2024'

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'hilltop_tea.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Session
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# Wage Tiers (Production Workers)
PRODUCTION_TIER_LIMITS = {
    'TIER_1_MAX': 349,
    'TIER_2_MIN': 350,
    'TIER_2_MAX': 399,
    'TIER_3_MIN': 400,
    'TIER_3_MAX': 499,
    'TIER_4_MIN': 500
}

PRODUCTION_TIER_RATES = {
    'TIER_1': 250,  # 0-349 cartons
    'TIER_2': 270,  # 350-399 cartons
    'TIER_3': 300,  # 400-499 cartons
    'TIER_4': 320   # 500+ cartons
}

# Wrapping Workers
WRAPPING_RATE_PER_CARTON = 100

# Pagination
ITEMS_PER_PAGE = 20

# File Upload
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

# Company Information
COMPANY_NAME = "HILLTOP TEA"
COMPANY_TAGLINE = "Premium Tea, Precision Tracking"
COMPANY_ADDRESS = "Lagos, Nigeria"

# User Roles
ROLE_ADMIN = 'admin'
ROLE_GM = 'gm'
ROLE_SUPERVISOR = 'supervisor'

# Employee Groups
GROUP_PRODUCTION = 'production'
GROUP_WRAPPING = 'wrapping'

# Default Admin Credentials (for initial setup)
DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin123'
