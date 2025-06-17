# routes/__init__.py
import os
import sys
import platform
import datetime
from flask import Blueprint, jsonify, current_app
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.questions import questions_bp
from routes.static import static_bp
from models import db
from flask_cors import cross_origin
import psutil

# Create a health check blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'API is running'})

@health_bp.route('/healthy', methods=['GET'])
def fly_health_check():
    """
    Comprehensive health check for monitoring systems.
    Returns detailed system and application status.
    """
    try:
        # System information
        system_info = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'processor': platform.processor(),
            'ram': f"{round(psutil.virtual_memory().total / (1024.0 ** 3))} GB",
            'cpu_count': psutil.cpu_count(),
            'cpu_usage': f"{psutil.cpu_percent(interval=1)}%"
        }
        
        # Application information
        app_info = {
            'python_version': platform.python_version(),
            'environment': os.getenv('FLASK_ENV', 'production'),
            'debug_mode': os.getenv('DEBUG', 'False'),
            'database_configured': 'Yes' if os.getenv('DATABASE_URL') else 'No'
        }

        return jsonify({
            'status': 'healthy',
            'timestamp': '2024-12-19T12:00:00Z',
            'system': system_info,
            'application': app_info
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# Add manual database initialization route
@health_bp.route('/init-database', methods=['POST'])
@cross_origin()
def manual_init_database():
    """
    Manual database initialization endpoint.
    This can be called to initialize the database if the automatic process fails.
    """
    try:
        from init_db import init_database
        success = init_database()
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Database initialized successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Database initialization failed'
            }), 500
    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': f'Database initialization failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

# Add database test route
@health_bp.route('/test-database', methods=['GET'])
@cross_origin()
def test_database():
    """
    Test database connection and basic operations.
    """
    try:
        from test_db import test_database_connection
        success = test_database_connection()
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Database connection test passed',
                'database_url': os.getenv('DATABASE_URL', 'Not set')[:50] + '...' if os.getenv('DATABASE_URL') else 'Not set'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Database connection test failed',
                'database_url': os.getenv('DATABASE_URL', 'Not set')[:50] + '...' if os.getenv('DATABASE_URL') else 'Not set'
            }), 500
    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': f'Database test failed: {str(e)}',
            'traceback': traceback.format_exc(),
            'database_url': os.getenv('DATABASE_URL', 'Not set')[:50] + '...' if os.getenv('DATABASE_URL') else 'Not set'
        }), 500

def register_blueprints(app, csrf):
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    app.register_blueprint(static_bp, url_prefix='/api/static')

    # Enable CSRF only for admin routes, disable for everything else
    csrf.exempt(health_bp)
    csrf.exempt(auth_bp)
    csrf.exempt(questions_bp)
    csrf.exempt(static_bp)

# Alias for register_blueprints to match the import in app.py
configure_routes = register_blueprints
