#!/usr/bin/python3
"""It’s time to start your API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    """returns 404 status"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def remove_session(exception):
    """calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)