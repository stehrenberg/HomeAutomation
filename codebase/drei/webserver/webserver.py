# coding=utf-8
import json

from flask import Flask, request, abort, jsonify
from flask.ext.socketio import SocketIO, emit

from database.database import MockDatabase
from dto.user import User


""" Setup
"""
app = Flask(__name__)
socket = SocketIO(app)
db = MockDatabase()

""" Websockets
"""


def broadcast_change():
    emit('change', {})


""" REST-Endpoints
"""

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


""" Helper functions
"""
def parse_user(user_json):
    user_name = user_json["name"]
    user_mac = user_json["mac"]
    user_sound = user_json["sound"]
    return User(user_mac, user_name, user_sound)


if __name__ == '__main__':
    socket.run(app)
