# config.py
import os
import re
from datetime import timedelta

# Flask app configuration
class Config:
    # Get Render-specific values if available
    IS_RENDER = os.getenv('RENDER', False)
    RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL', '')
    
    # Get DATABASE_URL with debugging
    DATABASE_URL = os.getenv('DATABASE_URL')
    print(f"DEBUG: DATABASE_URL from environment: {DATABASE_URL}")
    
    # Use PostgreSQL if DATABASE_URL is set, otherwise fall back to SQLite
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        # Handle Render's PostgreSQL connection string format if provided
        if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
        print(f"DEBUG: Using PostgreSQL: {SQLALCHEMY_DATABASE_URI}")
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///learnify.db'
        print(f"DEBUG: Using SQLite: {SQLALCHEMY_DATABASE_URI}")
    
    # Configure engine options based on database type
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
        SQLALCHEMY_ENGINE_OPTIONS = {}
        print("DEBUG: Using SQLite engine options")
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,  # Verify connections before use
            'pool_recycle': 3600,   # Recycle connections after an hour
        }
        print("DEBUG: Using PostgreSQL engine options")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    ADMIN_PASSKEY = os.getenv('ADMIN_PASSKEY', 'admin123')
    
    # Debug mode - disabled in production
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # CORS settings - only allow your frontend domain in production
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
