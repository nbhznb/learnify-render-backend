#!/usr/bin/env python3
"""
Database initialization script.

This script initializes the database with tables and initial data.
It can be run either locally or in the Render environment.

Usage:
    python init_db.py
"""

import os
from app import create_app
from models import db, User
from flask_migrate import upgrade, init, migrate

def init_database():
    """Initialize database with tables and initial data."""
    print("Initializing database...")
    
    app = create_app()
    with app.app_context():
        # Check if migrations directory exists
        if not os.path.exists('migrations'):
            print("Initializing migrations...")
            init()
            print("Creating initial migration...")
            migrate(message="Initial migration")
        
        print("Applying migrations...")
        upgrade()
        
        # Create an admin user if none exists
        if not User.query.filter_by(username='admin').first():
            print("Creating admin user...")
            admin = User(
                username='admin',
                email=os.getenv('ADMIN_EMAIL', 'admin@example.com'),
                password=os.getenv('ADMIN_PASSWORD', 'Admin123!')
            )
            admin.status = 'active'
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully.")
        
    print("Database initialization complete.")

if __name__ == '__main__':
    init_database() 