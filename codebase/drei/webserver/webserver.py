# coding=utf-8
from flask import Flask
from flask.ext.socketio import SocketIO, emit

from database.database import MockDatabase


""" Setup
"""
app = Flask(__name__)
socket = SocketIO(app)
db = MockDatabase()


@socket.on('getUsersRequest')
def get_users(request):
    emit('getUsersResponse', {'users': db.retrieve_users()})


@socket.on('addUserRequest')
def add_user(user):
    db.add_user(user)
    emit('addUserResponse', {'success': True})


if __name__ == '__main__':
    socket.run(app)

