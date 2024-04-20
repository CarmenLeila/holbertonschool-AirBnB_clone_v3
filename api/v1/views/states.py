#!/usr/bin/python3
"""This module contains the index view for the API"""


from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


# GET all states
# ============================================================================

@app_views.route('/states', methods=["GET"], strict_slashes=False)
def get_all_states():
    """gets the list of all states"""
    states = storage.all(State).values()

    list_states = [state.to_dict() for state in states]

    return jsonify(list_states)


# GET one state
# ============================================================================

@app_views.route('/states/<state_id>',
                 methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """gets a state object"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    return jsonify(state.to_dict())


# DELETE a state
# ============================================================================

@app_views.route('/states/<state_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """deletes a state object"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


# CREATE a state
# ============================================================================

@app_views.route('/states', methods=["POST"],
                 strict_slashes=False)
def create_state():
    """creates a new state"""
    try:
        request_data = request.get_json()
    except Exception as error:
        abort(400,description="Not a JSON: {}".format(str(error)))

    if not request_data:
        abort(400, description="Not a JSON")

    if "name" not in request_data:
        abort(400, description="Missing name")

    state = State(**request_data)
    state.save()
    return jsonify(state.to_dict()), 201


# UPDATE a state
# ============================================================================

@app_views.route('/states/<state_id>', methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """update a state object"""
    state_update = storage.get(State, state_id)

    if state_update is None:
        abort(404)

    try:
        request_data = request.get_json()
    except Exception as error:
        abort(400, description="Not a JSON: {}".format(str(error)))

    if not request_data:
        abort(400, description="Not a JSON")

    if "id" in request_data and request_data["id"] != state_id:
        abort(404, description="error: Not found")

    for key, value in request_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_update, key, value)

    state_update.save()
    return jsonify(state_update.to_dict()), 200
