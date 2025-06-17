#!/usr/bin/env python3
"""
Database initialization script.

This script initializes the database with tables and initial data.
It can be run either locally or in the Render environment.

Usage:
    python init_db.py
"""

import os
import sys
from app import create_app
from models import db, User
from flask_migrate import upgrade, init, migrate

def init_database():
    """Initialize database with tables and initial data."""
    print("=== Database Initialization Started ===")
    
    try:
        app = create_app()
        
        with app.app_context():
            # Print database configuration for debugging
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Test database connection
            try:
                db.engine.connect()
                print("✓ Database connection successful")
            except Exception as e:
                print(f"✗ Database connection failed: {e}")
                print("This might be normal if the database doesn't exist yet")
            
            # Check if migrations directory exists
            migrations_dir = os.path.join(os.getcwd(), 'migrations')
            if not os.path.exists(migrations_dir):
                print("Initializing Flask-Migrate...")
                try:
                    init()
                    print("✓ Flask-Migrate initialized")
                except Exception as e:
                    print(f"✗ Flask-Migrate initialization failed: {e}")
                    # Continue anyway, as this might not be critical
                
                print("Creating initial migration...")
                try:
                    migrate(message="Initial migration")
                    print("✓ Initial migration created")
                except Exception as e:
                    print(f"✗ Migration creation failed: {e}")
                    print("Falling back to direct table creation...")
                    # If migrations fail, create tables directly
                    db.create_all()
                    print("✓ Tables created directly")
            else:
                print("Flask-Migrate already initialized")
            
            # Apply migrations
            print("Applying migrations...")
            try:
                upgrade()
                print("✓ Migrations applied successfully")
            except Exception as e:
                print(f"✗ Migration upgrade failed: {e}")
                print("Falling back to direct table creation...")
                try:
                    db.create_all()
                    print("✓ Tables created directly")
                except Exception as e2:
                    print(f"✗ Direct table creation also failed: {e2}")
                    raise e2
            
            # Verify tables exist
            try:
                # Try to query the users table to ensure it exists
                User.query.count()
                print("✓ User table exists and is accessible")
            except Exception as e:
                print(f"✗ User table verification failed: {e}")
                print("Attempting to create tables directly...")
                db.create_all()
                print("✓ Tables created directly")
            
            # Create an admin user if none exists
            try:
                existing_admin = User.query.filter_by(username='admin').first()
                if not existing_admin:
                    print("Creating admin user...")
                    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
                    admin_password = os.getenv('ADMIN_PASSWORD', 'Admin123!')
                    
                    print(f"Admin email: {admin_email}")
                    
                    admin = User(
                        username='admin',
                        email=admin_email,
                        password=admin_password
                    )
                    admin.status = 'active'
                    db.session.add(admin)
                    db.session.commit()
                    print("✓ Admin user created successfully")
                else:
                    print("✓ Admin user already exists")
            except Exception as e:
                print(f"✗ Admin user creation failed: {e}")
                # This is critical, so re-raise the exception
                raise e
        
        print("=== Database Initialization Complete ===")
        return True
        
    except Exception as e:
        print(f"=== Database Initialization Failed ===")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = init_database()
    if not success:
        sys.exit(1) 