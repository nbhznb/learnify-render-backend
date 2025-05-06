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

# Create a health check blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "API is running"}), 200

@health_bp.route('/healthy', methods=['GET'])
def fly_health_check():
    """
    Enhanced health check that provides system status and database connectivity.
    This route is specifically designed for fly.io health checks.
    """
    health_data = {
        "status": "ok",
        "message": "API is running",
        "timestamp": datetime.datetime.now().isoformat(),
        "system": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "environment": os.environ.get("FLASK_ENV", "production")
        }
    }
    
    # Check database connection
    try:
        # Execute a simple query to verify database connectivity
        db_result = db.session.execute("SELECT 1").scalar()
        health_data["database"] = {
            "status": "connected" if db_result == 1 else "error",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_data["database"] = {
            "status": "error",
            "message": str(e)
        }
        health_data["status"] = "degraded"
    
    status_code = 200 if health_data["status"] == "ok" else 500
    return jsonify(health_data), status_code

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
