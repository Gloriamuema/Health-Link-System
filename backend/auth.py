from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Role
import jwt
import os
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    body = request.get_json() or {}
    email = body.get('email')
    password = body.get('password')
    name = body.get('name')
    role = body.get('role', 'patient')
    if not email or not password:
        return jsonify({'message': 'email and password required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'email exists'}), 409
    hashed = generate_password_hash(password)
    try:
        user = User(email=email, password=hashed, name=name, role=Role(role))
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'email exists'}), 409
    return jsonify({'message': 'created'}), 201

@bp.route('/login', methods=['POST'])
def login():
    body = request.get_json() or {}
    email = body.get('email')
    password = body.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'invalid credentials'}), 401
    payload = {'sub': user.id, 'exp': datetime.utcnow() + timedelta(hours=12)}
    token = jwt.encode(payload, os.getenv('JWT_SECRET', 'secret'), algorithm='HS256')
    return jsonify({'token': token, 'user': {'id': user.id, 'email': user.email, 'name': user.name, 'role': user.role.value}})
