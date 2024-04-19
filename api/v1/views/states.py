#!/usr/bin/python3
"""This module contains the index view for the API"""


from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


# GET all states
# ============================================================================

@app_views.route('/api/v1/states', methods=["GET"], strict_slashes=False)
def all_states():
    """gets the list of all states"""
    state_list = []
    for state in storage.all(State).values():
        state_list.append(state.to_dict())
    return jsonify(state_list)



# GET one state
# ============================================================================

@app_views.route('/api/v1/states/<state_id>',
                 methods=["GET"], strict_slashes=False)
def state_object(state_id):
    """gets a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


# DELETE a state
# ============================================================================

@app_views.route('/api/v1/states/<state_id>',
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

@app_views.route('/api/v1/states', methods=["POST"],
                 strict_slashes=False)
def create_state():
    """creates a new state"""
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    state = State(**request_data)
    state.save()
    return jsonify(state.to_dict()), 201



# UPDATE a state
# ============================================================================

@app_views.route('/api/v1/states/<state_id>', methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """update a state object"""
    state_update = storage.get(State, state_id)
    if not state_update:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_update, key, value)
    state_update.save()
    return jsonify(state_update.to_dict()), 200
