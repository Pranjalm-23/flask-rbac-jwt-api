from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps

def role_required(required_role):
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            user = get_jwt_identity()
            if user["role"] != required_role:
                return jsonify({"message": "Access denied"}), 403
            return func(*args, **kwargs)
        return decorated_function
    return wrapper
