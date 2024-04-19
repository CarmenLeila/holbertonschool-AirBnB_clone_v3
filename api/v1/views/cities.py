#!/usr/bin/python3
"""This module contains the index view for the API"""


from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


# GET all cities
# ============================================================================

@app_views.route('/api/v1/states/<state_id>/cities', methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """gets the list of all cities for a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


# GET one city
# ============================================================================

@app_views.route('/api/v1/cities/<city_id>',
                 methods=["GET"], strict_slashes=False)
def state_object(city_id):
    """gets a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


# DELETE a city
# ============================================================================

@app_views.route('/api/v1/cities/<city_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_state(city_id):
    """deletes a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


# CREATE a city
# ============================================================================

@app_views.route('/api/v1/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_state(state_id):
    """creates a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    city = City(**request_data)
    City.save()
    return jsonify(city.to_dict()), 201


# UPDATE a city
# ============================================================================

@app_views.route('/api/v1/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_state(city_id):
    """update a city object"""
    city_update = storage.get(City, city_id)
    if not city_update:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')

    for key, value in request_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_update, key, value)
    city_update.save()
    return jsonify(city_update.to_dict()), 200
