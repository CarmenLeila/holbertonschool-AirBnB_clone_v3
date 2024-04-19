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
    new_amenity = request.get_json(silent=True)
    if not new_amenity:
        return abort(400, {"Not a JSON"})
    if "name" not in new_amenity.keys():
        return abort(400, {"Missing name"})
    new_obj = Amenity(name=new_amenity['name'])
    storage.new(new_obj)
    storage.save()
    return new_obj.to_dict(), 201


# UPDATE an amenity
# ============================================================================

@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity"""
    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})
    old = storage.get(Amenity, amenity_id)
    if not old:
        return abort(404)
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in new.items():
        if key not in ignore:
            setattr(old, key, value)
    storage.save()
    return jsonify(old.to_dict()), 200
