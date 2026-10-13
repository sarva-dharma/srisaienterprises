from flask import Blueprint, request, jsonify, session
from backend.database import db
from backend.models import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    phone = data.get('phone', '').strip()

    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'An account with this email already exists'}), 400

    user = User(
        name=name,
        email=email,
        phone=phone,
        role='client'
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    session['user_role'] = user.role
    session['user_email'] = user.email

    return jsonify({
        'message': 'Registration successful',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    session['user_id'] = user.id
    session['user_role'] = user.role
    session['user_email'] = user.email

    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    })


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'authenticated': False, 'user': None})

    user = User.query.get(user_id)
    if not user:
        session.clear()
        return jsonify({'authenticated': False, 'user': None})

    return jsonify({
        'authenticated': True,
        'user': user.to_dict()
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})
