# app.py
from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from routes import register_blueprints
from models import db, bcrypt, jwt
from utils.image_handlers import cleanup_static_folders, ensure_static_folders
from config import Config
import os

def create_app():
    app = Flask(__name__, template_folder='static/templates')
    
    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}}, supports_credentials=True)

    # Load configurations
    app.config.from_object(Config)

    # Ensure static directories exist
    with app.app_context():
        ensure_static_folders()

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    csrf = CSRFProtect(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Create database tables only if not using migrations
    # Comment this out once migrations are set up
    # NOTE: Commented out to prevent database reset on each restart
    # with app.app_context():
    #     db.create_all()

    # Register blueprints
    register_blueprints(app, csrf)

    # Only run cleanup in development environments
    if app.config.get('DEBUG', False):
        with app.app_context():
            cleanup_static_folders()

    # Diagnostic route
    @app.route('/')
    def index():
        return 'Learnify API is running. Go to /api/ for endpoints.'

    return app

# Create a global app variable for gunicorn to use
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
