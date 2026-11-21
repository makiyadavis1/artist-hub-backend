
from datetime import datetime, timedelta, timezone

import jwt

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from artist_hub.extensions import db
from artist_hub.models import User

from functools import wraps
from flask import g

main = Blueprint("main", __name__)

def token_required(view_function):
    @wraps(view_function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "code": "AUTHENTICATION_REQUIRED",
                "message": "A valid Bearer token is required"
            }), 401

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
                options={"require": ["sub", "exp"]}
            )

            user_id = int(payload["sub"])

        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            return jsonify({
                "code": "INVALID_TOKEN",
                "message": "Invalid or expired token"
            }), 401

        user = db.session.get(User, user_id)

        if user is None:
            return jsonify({
                "code": "INVALID_TOKEN",
                "message": "Invalid or expired token"
            }), 401

        g.user_id = user.id

        return view_function(*args, **kwargs)

    return decorated

@main.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    email = data.get("email") if isinstance(data, dict) else None
    password = data.get("password") if isinstance(data, dict) else None

    if not email or not password:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "email and password are required"
        }), 400

    if not isinstance(password, str) or len(password) < 8:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "password must be at least 8 characters long"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "code": "EMAIL_TAKEN",
            "message": "email is already registered"
        }), 409

    password_hash = generate_password_hash(password)

    new_user = User(
        email=email,
        password_hash=password_hash
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "created_at": new_user.created_at.isoformat()
    }), 201


@main.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    email = data.get("email") if isinstance(data, dict) else None
    password = data.get("password") if isinstance(data, dict) else None

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({
            "code": "INVALID_CREDENTIALS",
            "message": "Invalid email or password"
        }), 401

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({
            "code": "INVALID_CREDENTIALS",
            "message": "Invalid email or password"
        }), 401

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user.id),
        "role": user.role,
        "exp": now + timedelta(
            seconds=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        )
    }

    access_token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer"
}), 200

@main.route("/profile", methods=["GET"])
@token_required
def get_profile():
    user = db.session.get(User, g.user_id)

    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat()
    }), 200

    
