#!/usr/bin/python3
"""It’s time to start our API"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


# GET all places from a city
# ============================================================================


@app_views.route('/cities/<city_id>/places',
                 methods=["GET"], strict_slashes=False)
def all_places(city_id):
    """get the list of all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_list = []
    for place in city.place:
        place_list.append(place.to_dict())
    return jsonify(place_list)


# GET a place
# ============================================================================


@app_views.route('/places/<place_id>',
                 methods=["GET"], strict_slashes=False)
def place_object(place_id):
    """get a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

# DELETE a place
# ============================================================================


@app_views.route('/places/<place_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """delete a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


# CREATE a place
# ============================================================================


@app_views.route('cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """creates a place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    user = storage.get(User, request_data['user_id'])
    if user is None:
        abort(404)
    place = Place(**request_data)
    place.save()
    return jsonify(place.to_dict()), 201

# UPDATE a place
# ============================================================================


@app_views.route('/places/<place_id>', methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """updates a place by ID"""
    place_update = storage.get(Place, place_id)
    if place_update is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_update, key, value)
    place_update.save()
    return jsonify(place_update.to_dict()), 200
