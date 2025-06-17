# routes/admin.py
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, current_app
from flask_cors import CORS
from models import User, db
from sqlalchemy import text
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)
CORS(admin_bp)

@admin_bp.route('/', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        passkey = request.form.get('passkey')
        if passkey == current_app.config.get('ADMIN_PASSKEY'):
            session['admin_authenticated'] = True
            return redirect(url_for('admin.admin_panel'))
        else:
            error = "Invalid passkey"
            return render_template('admin_login.html', error=error)
    if not session.get('admin_authenticated'):
        return render_template('admin_login.html')
    
    try:
        users = User.query.all()
        return render_template('admin.html', users=users)
    except Exception as e:
        # If there's a database error, create tables and try again
        print(f"Error querying users: {e}")
        try:
            db.create_all()
            users = User.query.all()
            return render_template('admin.html', users=users)
        except Exception as e2:
            print(f"Error creating tables: {e2}")
            return jsonify({'error': 'Database error', 'details': str(e2)}), 500

# Add the admin_logout endpoint
@admin_bp.route('/logout', methods=['GET'])
def admin_logout():
    session.pop('admin_authenticated', None)
    return redirect(url_for('admin.admin_panel'))

# Add the admin_approve endpoint
@admin_bp.route('/approve', methods=['POST'])
def admin_approve():
    if not session.get('admin_authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    user_id = data.get('user_id')
    duration = data.get('duration')

    # Restrict durations to a safe set
    allowed_durations = ['1 month', '3 months', '6 months', '1 year']
    if duration not in allowed_durations:
        return jsonify({'error': 'Invalid duration specified'}), 400

    try:
        # Calculate the approved_until date using Python instead of database-specific functions
        duration_map = {
            '1 month': 30,
            '3 months': 90,
            '6 months': 180,
            '1 year': 365
        }
        days_to_add = duration_map[duration]
        approved_until = datetime.utcnow() + timedelta(days=days_to_add)
        
        # Use SQLAlchemy ORM instead of raw SQL to be database-agnostic
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        user.approved_until = approved_until
        user.status = 'active'
        db.session.commit()
        
        return jsonify({'message': 'User approved successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error approving user {user_id}: {e}")
        return jsonify({'error': 'Failed to approve user', 'details': str(e)}), 500

@admin_bp.route('/cancel', methods=['POST'])
def admin_cancel():
    if not session.get('admin_authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    user_id = data.get('user_id')

    try:
        # Use SQLAlchemy ORM instead of raw SQL to be database-agnostic
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        user.approved_until = None
        user.status = 'inactive'
        db.session.commit()
        
        return jsonify({'message': 'Subscription canceled successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error canceling subscription for user {user_id}: {e}")
        return jsonify({'error': 'Failed to cancel subscription', 'details': str(e)}), 500
