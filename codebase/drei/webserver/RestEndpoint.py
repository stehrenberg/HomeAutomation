import json
import logging

from flask import Flask, request, abort, jsonify

from flask.ext.socketio import SocketIO

from database.database import MockDatabase
from dto.user import User

__author__ = 's.jahreiss'

app = Flask("Drei Webserver")
socket = SocketIO(app)
db = MockDatabase()


@app.route('/api/users', methods=['GET'])
def get_users():
    users = json.dumps([user.__dict__ for user in db.retrieve_users()])
    return users


@app.route('/api/users', methods=['POST'])
def add_user():
    if not request.json or not 'user' in request.json:
        abort(400)
    user = parse_user(request.json['user'])
    return jsonify({'user': db.add_user(user)}), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.json or not 'user' in request.json:
        abort(400)
    user = parse_user(request.json['user'])
    user = db.update_user(user_id, user)
    return {'user': user}


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db.delete_user(user_id)
    return {'Result': True}


def parse_user(user_json):
    name = user_json["name"]
    mac = user_json["mac"]
    sound = user_json["sound"]
    light = user_json["light"]
    return User(mac, name, sound, light)


def start_rest_endpoint():
    # Change log level for flask to print only errors.
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # Initialize the rest endpoint
    socket.run(app)