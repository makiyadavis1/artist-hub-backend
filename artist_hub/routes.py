
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from artist_hub.extensions import db
from artist_hub.models import User


main = Blueprint("main", __name__)


@main.route("/auth/register", methods=["POST"])
def register():
    # Read JSON request body
    data = request.get_json()

    email = data.get("email") if data else None
    password = data.get("password") if data else None

    # Check required fields
    if not email or not password:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "email and password are required"
        }), 400

    # Check password length
    if len(password) < 8:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "password must be at least 8 characters long"
        }), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "code": "EMAIL_TAKEN",
            "message": "email is already registered"
        }), 409

    # Hash the password
    password_hash = generate_password_hash(password)

    # Create new user
    new_user = User(
        email=email,
        password_hash=password_hash
    )

    # Save user to database
    db.session.add(new_user)
    db.session.commit()

    # Return successful response
    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "created_at": new_user.created_at.isoformat()
    }), 201
