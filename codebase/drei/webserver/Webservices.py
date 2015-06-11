import json
import logging

from flask import Flask, request, abort
from flask.ext.cors import CORS
from flask.ext.socketio import SocketIO, emit

from dto.user import User
from lib.database.SQLiteWrapper import SQLiteWrapper
from lib.dir.Directory import get_file_list


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

# String containing all available sounds
sounds = None


# ----------- REST definitions -----------
@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Returns the list of users as json string.
    :return: Users list as json string.
    """
    # Serialize users
    users = json.dumps([user.__dict__ for user in db.retrieve_users()])
    return users, 200


@app.route('/api/sounds', methods=['GET'])
def get_sounds():
    """
    Returns the list of available sounds as json string.
    :return: Songs list as json string.
    """
    # Return sounds
    return sounds, 200


@app.route('/api/users', methods=['POST'])
def add_user():
    """
    Adds a user to the users list.
    :return: Json object which contains a boolean which indicates whether the user was created.
    """
    if not request.json:
        abort(400)
    user = parse_user(request.json)
    created = db.add_user(user)
    return serialize_key_value_response('created', created), 201


@app.route('/api/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates the user with the specified id.
    :param user_id: The id of the user who will be updated.
    :return: Json object which contains a boolean which indicates whether the user was updated.
    """
    if not request.json:
        abort(400)
    user = parse_user(request.json)
    updated = db.update_user(user_id, user)
    return serialize_key_value_response('updated', updated), 202


@app.route('/api/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes the user with the specified id.
    :param user_id: The id of the user who will be deleted.
    :return: Json object which contains a boolean which indicates whether the user was deleted.
    """
    deleted = db.delete_user(user_id)
    return serialize_key_value_response('deleted', deleted), 200


# ----------- Websocket definitions -----------
def notify_active_users(user_list_new):
    """
    Notifies all clients about changes with the changed user list.
    :param user_list_new: The changed user list which will be sent to the clients.
    """
    global user_list
    user_list = macs_to_users(user_list_new)
    socket.emit('ActiveUsersNotification', json.dumps([user.__dict__ for user in user_list]))


@socket.on('connect')
def welcome_client():
    """
    Welcomes all clients. This function is necessary otherwise the clients cannot be addressed by an broadcast.
    """
    emit('Connected')


@socket.on('GetActiveUsersEvent')
def get_active_users():
    """
    Returns a list with all active users in a json string.
    :return: Json string with a list of all active users.
    """
    global user_list
    emit('ActiveUsersNotification', json.dumps([user.__dict__ for user in user_list]))


# ----------- Helpers -----------
def parse_user(user_json):
    """
    Parses a user object.
    :param user_json: The json string.
    :return: The parsed user object.
    """
    name = user_json["name"]
    mac = user_json["mac"]
    sound = user_json["sound"]
    light_color = user_json["light_color"]
    return User(mac, name, sound, None, light_color)


def macs_to_users(macs):
    """
    Returns a list of users for the specified mac addresses.
    :param macs: The list of mac addresses.
    :return: A list of user objects for the specified mac addresses.
    """
    result_list = []
    for mac in macs:
        result_list.append(db.get_user(mac))
    return result_list


def serialize_key_value_response(key, value):
    """
    Serializes a key value pair where value is the bool into json.
    :param key: The key for the boolean value.
    :param value: The boolean value.
    :return: Returns a json string with the specified key value pair.
    """
    return json.dumps({key: value})


def get_sound_list():
    """
    Returns a list of all available sounds in the file system.
    :return: All available sounds in the filesystem.
    """
    global sounds

    sound_extensions = ["mp3", "wav"]
    sounds = get_file_list("./resources/sounds", sound_extensions)
    return json.dumps(sounds)


def start():
    """
    Starts the Webservices (REST and Websocket).
    """
    global sounds

    # Retrieve the sound files.
    sounds = get_sound_list()

    # Change log level for flask to print only errors.
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # Return the configured flask app
    socket.run(
        app,
        host="0.0.0.0",
        port=8080
    )
