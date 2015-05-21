import json
import logging
from string import split
from glob import glob

from flask import Flask, request, abort
from flask.ext.cors import CORS
from flask.ext.socketio import SocketIO, emit

from dto.user import User
from lib.database.SQLiteWrapper import SQLiteWrapper


__author__ = 's.jahreiss'

# Create the webserver with rest services
app = Flask("Drei Webserver")
app.config['SECRET_KEY'] = 'secret!'

# Create cors extension - it allows every request
cors = CORS(app)

# Create socket extension
socket = SocketIO(app)

# Create the database connection
db = SQLiteWrapper()

# List containing online users
user_list = []


# ----------- REST definitions -----------
@app.route('/api/users', methods=['GET'])
def get_users():
    # Serialize users
    users = json.dumps([user.__dict__ for user in db.retrieve_users()])
    return users, 200


@app.route('/api/sounds', methods=['GET'])
def get_sounds():
    # Serialize sounds
    test = get_sound_list()
    sounds = json.dumps(test)
    return sounds, 200


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
def notify_active_users(user_list_new):
    global user_list
    user_list = macs_to_users(user_list_new)
    socket.emit('ActiveUsersNotification', json.dumps([user.__dict__ for user in user_list]))


# This function is necessary otherwise the clients
# cannot be addressed by an broadcast
@socket.on('connect')
def welcome_client():
    emit('Connected')


@socket.on('GetActiveUsersEvent')
def get_active_users():
    global user_list
    emit('ActiveUsersNotification', json.dumps([user.__dict__ for user in user_list]))


# ----------- Helpers -----------
def parse_user(user_json):
    name = user_json["name"]
    mac = user_json["mac"]
    sound = user_json["sound"]
    light_color = user_json["light_color"]
    return User(mac, name, sound, None, light_color)


def macs_to_users(macs):
    result_list = []
    users = db.retrieve_users()
    for mac in macs:
        result_list.append(get_user(users, mac))
    return result_list


def get_user(users, user_mac):
        return next(user for user in users if user.mac == user_mac)


def serialize_boolean_response(key, value):
    return json.dumps({key: value})


def get_sound_list():
    sound_list = glob('./lib/periphery/soundFiles/*')
    i = 0
    for sound in sound_list:
        split_list = split(sound, '/')
        sound_list[i] = split_list[len(split_list)-1]
        i += 1
    return sound_list

def start():
    # Change log level for flask to print only errors.
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # Return the configured flask app
    socket.run(
        app,
        host="0.0.0.0",
        port=8080
    )
