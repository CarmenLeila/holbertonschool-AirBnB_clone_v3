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

@app_views.route('/api/v1/places/<place_id>/reviews',
                 methods=["GET"], strict_slashes=False)
def all_reviews(place_id):
    """gets the list of all reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_list = []
    for review in place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


# GET one review
# ============================================================================

@app_views.route('/api/v1/reviews/<review_id>',
                 methods=["GET"], strict_slashes=False)
def review_object(review_id):
    """gets a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


# DELETE a review
# ============================================================================

@app_views.route('/api/v1/reviews/<review_id>',
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

@app_views.route('/api/v1/places/<place_id>/reviews',
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """creates a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    user = storage.get(User, request_data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request_data:
        abort(400, 'Missing text')
    new_review = Review(**request_data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


# UPDATE a review
# ============================================================================

@app_views.route('/api/v1/reviews/<review_id>',
                 methods=["PUT"], strict_slashes=False)
def update_reviews(review_id):
    """update a review object"""
    review_update = storage.get(Review, review_id)
    if not review_update:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')

    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review_update, key, value)
    review_update.save()
    return jsonify(review_update.to_dict()), 200
