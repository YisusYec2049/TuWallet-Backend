from flask import request, jsonify
from werkzeug.security import check_password_hash
from models.db import db, User
from werkzeug.security import generate_password_hash

def login_route():
    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')

    user = User.query.filter_by(username=phone).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Login successful', 'user_id': user.user_id}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

def register_route():
    data = request.get_json()
    name = data.get('name', 'Default Name')
    surname = data.get('surname', 'Default Surname')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': f'Email {email} already exists'}), 400


    if not email or not phone or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(
        username=phone,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201



def get_balance_route(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'balance': user.balance}), 200

def update_balance_route(user_id):
    data = request.get_json()
    amount = data.get('amount')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.balance += amount
    db.session.commit()
    return jsonify({'message': 'Balance updated successfully', 'balance': user.balance}), 200
