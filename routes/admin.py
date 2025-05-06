# routes/admin.py
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, current_app
from flask_cors import CORS
from models import User, db
from sqlalchemy import text

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
    users = User.query.all()
    return render_template('admin.html', users=users)

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
        # Map durations to SQLite datetime modifiers
        duration_map = {
            '1 month': '+1 month',
            '3 months': '+3 months',
            '6 months': '+6 months',
            '1 year': '+1 year'
        }
        sqlite_duration = duration_map[duration]
        
        # Use SQLite's datetime function instead of PostgreSQL interval
        update_query = text(
            "UPDATE users SET approved_until = datetime('now', :duration), status = 'active' WHERE id = :user_id"
        )
        db.session.execute(update_query, {'duration': sqlite_duration, 'user_id': user_id})
        db.session.commit()
        return jsonify({'message': 'User approved successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error approving user {user_id}: {e}")
        return jsonify({'error': 'Failed to approve user'}), 500

@admin_bp.route('/cancel', methods=['POST'])
def admin_cancel():
    if not session.get('admin_authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    user_id = data.get('user_id')

    try:
        cancel_query = text(
            "UPDATE users SET approved_until = NULL, status = 'inactive' WHERE id = :user_id"
        )
        db.session.execute(cancel_query, {'user_id': user_id})
        db.session.commit()
        return jsonify({'message': 'Subscription canceled successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error canceling subscription for user {user_id}: {e}")
        return jsonify({'error': 'Failed to cancel subscription'}), 500
