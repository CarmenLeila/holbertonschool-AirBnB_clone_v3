#!/usr/bin/python3
"""This module contains the index view for the API"""


from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


# GET all users
# ============================================================================

@app_views.route('/users', methods=["GET"], strict_slashes=False)
def get_all_users():
    """gets the list of all users"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


# GET one user
# ============================================================================

@app_views.route('/users/<user_id>',
                 methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """gets a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


# DELETE an user
# ============================================================================

@app_views.route('/users/<user_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """deletes an user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


# CREATE an user
# ============================================================================

@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """creates a new user"""
    try:
        data = request.get_json()
    except Exception as error:
        abort(400, desciption="Not a JSON: {}".format(str(error)))

    if not data:
        abort(400, desciption="Not a JSON")

    if "email" not in data:
        abort(400, desciption="Missing email")

    if "password" not in data:
        abort(400, desciption="Missing password")

    new_user = User(**request.json)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


# UPDATE an user
# ============================================================================

@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """update an user object"""
    user_update = storage.get(User, user_id)
    if not user_update:
        abort(404)

    try:
        data = request.get_json()
    except Exception as error:
        abort(400, desciption="Not a JSON: {}".format(str(error)))

    if not data:
        abort(400, desciption="Not a JSON")

    if "id" in data and data["id"] != user_id:
        abort(404, description="error: Not found")

    ignore_key = ["id", "email", "created_at", "updated_at"]
    for key, value in request.json.items():
        if key not in ignore_key:
            setattr(user_update, key, value)
    user_update.save()
    return jsonify(user_update.to_dict()), 200
