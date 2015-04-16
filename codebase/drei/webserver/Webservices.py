import json
import logging

from flask import Flask, request, abort
from flask.ext.cors import CORS
from flask.ext.socketio import SocketIO, emit

from dto.user import User
from lib.database.Database import MockDatabase


__author__ = 's.jahreiss'

# Create the webserver with rest services
app = Flask("Drei Webserver")
app.config['SECRET_KEY'] = 'secret!'

# Create cors extension - it allows every request
cors = CORS(app)

# Create socket extension
socket = SocketIO(app)

# Create the database connection
db = MockDatabase()


# ----------- REST definitions -----------
@app.route('/api/users', methods=['GET'])
def get_users():
    # Serialize users
    users = json.dumps([user.__dict__ for user in db.retrieve_users()])
    return users, 200


@app.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        abort(400)
    user = parse_user(request.json)
    created = db.add_user(user)
    return serialize_boolean_response('created', created), 201


@app.route('/api/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.json:
        abort(400)
    user = parse_user(request.json)
    updated = db.update_user(user_id, user)
    return serialize_boolean_response('updated', updated), 202


@app.route('/api/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    deleted = db.delete_user(user_id)
    return serialize_boolean_response('deleted', deleted), 200


# ----------- Websocket definitions -----------
def notify_active_users(event):
    socket.emit('ActiveUsersNotification', json.dumps([user.__dict__ for user in db.retrieve_users()]))


# This function is necessary otherwise the clients
# cannot be addressed by an broadcast
@socket.on('connect')
def welcome_client():
    emit('Connected')


@socket.on('GetActiveUsersEvent')
def get_active_users():
    emit('ActiveUsersNotification', json.dumps([user.__dict__ for user in db.retrieve_users()]))


# ----------- Helpers -----------
def parse_user(user_json):
    name = user_json["name"]
    mac = user_json["mac"]
    sound = user_json["sound"]
    light_color = user_json["light_color"]
    return User(mac, name, sound, None, light_color)


def serialize_boolean_response(key, value):
    return json.dumps({key: value})


def start():
    # Change log level for flask to print only errors.
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # Return the configured flask app
    socket.run(
        app,
        port=8080
    )