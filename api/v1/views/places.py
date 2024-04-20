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
def get_all_places(city_id):
    """get the list of all places"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    list_places = [place.to_dict() for place in city.places]

    return jsonify(list_places)


# GET a place
# ============================================================================

@app_views.route('/places/<place_id>',
                 methods=["GET"], strict_slashes=False)
def get_place(place_id):
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

    try:
        data = request.get_json()
    except Exception as error:
        abort(400, description="Not a JSON: {}".format(str(error)))

    if data is None:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    if "name" not in data:
        abort(400, description="Missing name")

    data["city_id"] = city_id
    place = Place(**data)
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

    try:
        data = request.get_json()
    except Exception as error:
        abort(400, description="Not a JSON")

    if "id" in data and data["id"] != place_id:
        abort(404, description="error: Not found")

    for key, value in data.items():
        if key not in ["id", "user_id", "created_at", "updated_at"]:
            setattr(place_update, key, value)

    place_update.save()
    return jsonify(place_update.to_dict()), 200
