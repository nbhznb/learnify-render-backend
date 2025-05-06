# routes/static.py
from flask import Blueprint, send_from_directory, current_app
from flask_cors import CORS
import os

static_bp = Blueprint('static', __name__)
CORS(static_bp)

@static_bp.route('/static/<path:filename>')
def static_file(filename):
    """
    Serve static files - note that this route is primarily for development.
    On PythonAnywhere, static files should be configured to be served directly
    via the web interface for better performance.
    """
    # Get static directory from the current application
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
    return send_from_directory(static_dir, filename)
