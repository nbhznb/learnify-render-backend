#!/usr/bin/env python3
"""
Database connection test script.
Use this to verify your database configuration is working.
"""

import os
import sys
from app import create_app
from models import db, User

def test_database_connection():
    """Test database connection and basic operations."""
    print("=== Database Connection Test ===")
    
    # Print environment variables (safely)
    print(f"DATABASE_URL set: {'Yes' if os.getenv('DATABASE_URL') else 'No'}")
    print(f"RENDER environment: {'Yes' if os.getenv('RENDER') else 'No'}")
    
    try:
        app = create_app()
        
        with app.app_context():
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Test basic connection
            try:
                connection = db.engine.connect()
                print("✓ Database connection successful")
                connection.close()
            except Exception as e:
                print(f"✗ Database connection failed: {e}")
                return False
            
            # Test table creation
            try:
                db.create_all()
                print("✓ Tables created successfully")
            except Exception as e:
                print(f"✗ Table creation failed: {e}")
                return False
            
            # Test basic query
            try:
                user_count = User.query.count()
                print(f"✓ User table accessible, count: {user_count}")
            except Exception as e:
                print(f"✗ User table query failed: {e}")
                return False
            
            # Test creating a user
            try:
                test_user = User.query.filter_by(username='test_user').first()
                if not test_user:
                    test_user = User(
                        username='test_user',
                        email='test@example.com',
                        password='testpass123'
                    )
                    db.session.add(test_user)
                    db.session.commit()
                    print("✓ Test user created successfully")
                else:
                    print("✓ Test user already exists")
                
                # Clean up test user
                db.session.delete(test_user)
                db.session.commit()
                print("✓ Test user cleaned up")
                
            except Exception as e:
                print(f"✗ User creation/deletion test failed: {e}")
                return False
            
            print("=== All Database Tests Passed ===")
            return True
            
    except Exception as e:
        print(f"=== Database Test Failed ===")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_database_connection()
    if not success:
        sys.exit(1)
    else:
        print("Database is ready to use!") 