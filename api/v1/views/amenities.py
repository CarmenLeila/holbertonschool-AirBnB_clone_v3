#!/usr/bin/python3
"""module contains Amenities view for the API"""


from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


# GET all amenities
# ============================================================================

@app_views.route("/amenities",
                 methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """get amenities object"""
    amenities = storage.all(Amenity).values()

    amenities_list = [amenity.to_dict() for amenity in amenities]

    return jsonify(amenities_list)


# GET one amenity
# ============================================================================

@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity_object(amenity_id):
    """amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


# DELETE an amenity
# ============================================================================

@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity object if not exist"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


# CREATE an amenity
# ============================================================================

@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """create an amenity object"""

    try:
        data = request.get_json()
    except Exception as error:
        abort(400, description="Not a JSON: {}".format(str(error)))

    if data is None:
        abort(400, description="Missing name")

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


# UPDATE an amenity
# ============================================================================

@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    try:
        data = request.get_json()
    except Exception as error:
        abort(400, description="Not a JSON: {}".format(str(error)))

    if not data:
        abort(400, description="Not a JSON")

    if "id" in data and data["id"] != amenity_id:
        abort(404, description="error: Not found")

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
