#!/usr/bin/python3
"""This module contains the index view for the API"""


from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


# GET all users
# ============================================================================

@app_views.route('/api/v1/users', methods=["GET"], strict_slashes=False)
def all_users():
    """gets the list of all users"""
    user_list = []
    for user in storage.all(User).values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


# GET one user
# ============================================================================

@app_views.route('/api/v1/users/<user_id>',
                 methods=["GET"], strict_slashes=False)
def user_object(user_id):
    """gets a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


# DELETE an user
# ============================================================================

@app_views.route('/api/v1/users/<user_id>',
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

@app_views.route('/api/v1/users', methods=["POST"], strict_slashes=False)
def create_user():
    """creates a new user"""
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'email' not in request_data:
        abort(400, 'Missing email')
    if 'password' not in request_data:
        abort(400, 'Missing password')
    user = User(**request_data)
    user.save()
    return jsonify(user.to_dict()), 201


# UPDATE an user
# ============================================================================

@app_views.route('/api/v1/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """update an user object"""
    user_update = storage.get(User, user_id)
    if not user_update:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')

    for key, value in request_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_update, key, value)
    user_update.save()
    return jsonify(user_update.to_dict()), 200
