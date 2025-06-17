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
    print("=== Creating Flask Application ===")
    app = Flask(__name__, template_folder='static/templates')
    
    # Load configurations
    app.config.from_object(Config)
    print(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}}, supports_credentials=True)

    # Ensure static directories exist
    with app.app_context():
        ensure_static_folders()

    # Initialize extensions
    print("Initializing database...")
    try:
        db.init_app(app)
        print("✓ Database initialized")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        raise e
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    csrf = CSRFProtect(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Always ensure database tables exist
    print("Ensuring database tables exist...")
    with app.app_context():
        try:
            # Test if tables exist by trying a simple query
            from models import User
            User.query.count()
            print("✓ Database tables already exist")
        except Exception as e:
            print(f"Database tables don't exist or are inaccessible: {e}")
            print("Creating database tables...")
            try:
                db.create_all()
                print("✓ Database tables created successfully")
                
                # Verify table creation worked
                User.query.count()
                print("✓ Database tables verified and accessible")
            except Exception as e2:
                print(f"✗ Database table creation failed: {e2}")
                raise e2

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

    # Add a database health check route
    @app.route('/db-health')
    def db_health():
        try:
            # Test database connection
            db.engine.connect()
            from models import User
            user_count = User.query.count()
            return {
                'status': 'healthy',
                'database': 'connected',
                'user_count': user_count,
                'database_uri': app.config['SQLALCHEMY_DATABASE_URI'][:50] + '...'  # Truncate for security
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e),
                'database_uri': app.config['SQLALCHEMY_DATABASE_URI'][:50] + '...'  # Truncate for security
            }, 500

    print("=== Flask Application Created Successfully ===")
    return app

# Create a global app variable for gunicorn to use
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
