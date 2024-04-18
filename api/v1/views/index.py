#!/usr/bin/python3
"""It’s time to start your API"""



from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """route that returns a JSON"""
    return jsonify({'status': 'OK'})
