#!/usr/bin/python3
"""module contains Amenities view for the API"""


from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


# GET all amenities
# ============================================================================

@app_views.route('/amenities',
                 methods=["GET"], strict_slashes=False)
def all_amenities():
    """get amenities object"""
    amenities = storage.get(Amenity)
    amenity_list = []
    for amenity in amenities.values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


# GET one amenity
# ============================================================================

@app_views.route('/amenities/<amenity_id>',
                 methods=["GET"], strict_slashes=False)
def amenity_object(amenity_id):
    """amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


# DELETE an amenity
# ============================================================================

@app_views.route('/amenities/<amenity_id>',
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

@app_views.route('/amenities', methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """create an amenity object"""
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**request_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


# UPDATE an amenity
# ============================================================================

@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update an amenity object"""
    amenity_update = storage.get(Amenity, amenity_id)
    if not amenity_update:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_update, key, value)
    amenity_update.save()
    return jsonify(amenity_update.to_dict()), 200
