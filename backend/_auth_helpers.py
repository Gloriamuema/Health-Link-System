from functools import wraps
from flask import request, jsonify
import jwt
import os
from models import User

def get_current_user():
    auth = request.headers.get('Authorization', None)
    if not auth:
        return None
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    token = parts[1]
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET', 'secret'), algorithms=['HS256'])
        user_id = payload.get('sub')
        return User.query.get(user_id)
    except Exception:
        return None

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'message': 'Unauthorized'}), 401
        return fn(user, *args, **kwargs)
    return wrapper
