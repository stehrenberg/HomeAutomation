import json
import logging

from flask import Flask, request, abort

from database.database import MockDatabase
from dto.user import User


__author__ = 's.jahreiss'

app = Flask("Drei Webserver")
db = MockDatabase()


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


def parse_user(user_json):
    name = user_json["name"]
    mac = user_json["mac"]
    sound = user_json["sound"]
    light = user_json["light"]
    return User(mac, name, sound, light)


def serialize_boolean_response(key, value):
    return json.dumps({key: value})


def start_rest_endpoint():
    # Change log level for flask to print only errors.
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # Initialize the rest endpoint
    app.run()