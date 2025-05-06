# routes/auth.py
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from pytz import utc
from models import User, db, bcrypt
from utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)
CORS(auth_bp)

@auth_bp.route('/user/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json()

    if not all(key in data for key in ['username', 'password']):
        return jsonify({'error': 'Missing credentials'}), 400

    user = User.query.filter_by(username=data['username']).first()
    print("Logging in user:", data["username"])

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        if user.status == 'inactive':
            return jsonify({'error': 'Your account is not approved yet.'}), 403

        current_time = datetime.now(utc)

        if user.approved_until:
            approved_until_utc = utc.localize(user.approved_until)
            if current_time > approved_until_utc:
                user.status = 'expired'
                db.session.commit()
                return jsonify({'error': 'Your subscription has expired.'}), 403

        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.id
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/user/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json()

    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400

    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400

    if not validate_password(data['password']):
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/user/profile', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_profile():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    return jsonify({
        'username': user.username,
        'email': user.email
    }), 200

@auth_bp.route('/user/profile', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_profile():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()

    if 'email' in data:
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        if User.query.filter_by(email=data['email']).first() and data['email'] != user.email:
            return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']

    if 'password' in data:
        if not validate_password(data['password']):
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

@auth_bp.route('/user/profile', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_profile():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200
