#!/usr/bin/python3
"""This module contains the index view for the API"""


from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


# GET all cities
# ============================================================================

@app_views.route('/states/<state_id>/cities',
                 methods=["GET"], strict_slashes=False)
def get_all_cities(state_id):
    """gets the list of all cities for a state"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


# GET one city
# ============================================================================

@app_views.route('/cities/<city_id>',
                 methods=["GET"], strict_slashes=False)
def get_one_city(city_id):
    """gets a city object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    return jsonify(city.to_dict())


# DELETE a city
# ============================================================================

@app_views.route('/cities/<city_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """deletes a city object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


# CREATE a city
# ============================================================================

@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """creates a new city"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as error:
        abort(400, description="Not a JSON: {}".format(str(error)))

    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    data["state_id"] = state_id

    city = City(**_data)
    city.save()
    return jsonify(city.to_dict()), 201


# UPDATE a city
# ============================================================================

@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """update a city object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    try:
        data = request.get_json()
    except Exception as error:
        abort(400, description="Not a JSON: {}".format(str(error)))

    if not data:
        abort(400, description="Not a JSON")

    if "id" in data and data["id"] != city_id:
        abort(404, description="error: Not found")

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
