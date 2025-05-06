# config.py
import os
import re
from datetime import timedelta

# Flask app configuration
class Config:
    # Get Render-specific values if available
    IS_RENDER = os.getenv('RENDER', False)
    RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL', '')
    
    # Use SQLite by default, but allow override via environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///learnify.db')
    
    # Handle Render's PostgreSQL connection string format if provided
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    # Configure engine options based on database type
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
        SQLALCHEMY_ENGINE_OPTIONS = {}
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,  # Verify connections before use
            'pool_recycle': 3600,   # Recycle connections after an hour
        }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    ADMIN_PASSKEY = os.getenv('ADMIN_PASSKEY', 'admin123')
    
    # Debug mode - disabled in production
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # CORS settings - only allow your frontend domain in production
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
