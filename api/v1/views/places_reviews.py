#!/usr/bin/python3
"""This module contains the index view for the API"""


from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


# GET all reviews
# ============================================================================

@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                  strict_slashes=False)
def get_all_reviews(place_id):
    """gets the list of all reviews"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    review = storage.all(Review).values()
    review_list = [
        review.to_dict() for review in reviews if review.place_id == place_id
    ]
    return jsonify(review_list)


# GET one review
# ============================================================================

@app_views.route('/reviews/<review_id>',
                 methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """gets a review object"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


# DELETE a review
# ============================================================================

@app_views.route('/reviews/<review_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """deletes a review object"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


# CREATE a review
# ============================================================================

@app_views.route('/places/<place_id>/reviews',
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """creates a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        request_data = request.get_json()
    except Exception as error:
        abort(400, description="Not a JSON: {}".format(str(error)))

    if not request_data:
        abort(400, description="Not a JSON")

    if "user_id" not in request_data:
        abort(400, description="Missing user_id")

    user = storage.get(User, request_data["user_id"])
    if user is None:
        abort(404)

    if "text" not in request_data:
        abort(400, description="Missing text")

    request_data["place_id"] = place_id
    review = Review(**request_data)
    review.save()
    return jsonify(review.to_dict()), 201


# UPDATE a review
# ============================================================================

@app_views.route('/reviews/<review_id>',
                 methods=["PUT"], strict_slashes=False)
def update_reviews(review_id):
    """update a review object"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    try:
        request_data = request.get_json()
    except Exception as error:
        abort(400, description="Not a JSON: {}".format(str(error)))

    if not request_data:
        abort(400, description="Not a JSON")

    if "id" in request_data and request_data["id"] != review_id:
        abort(404, description="error: Not found")

    for key, value in request_data.items():
        if key not in ["id",
                       "user_id",
                       "place_id",
                       "created_at",
                       "updated_at"
                       ]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
