# election_app/extensions.py
from flask_pymongo import PyMongo
# extensions.py
from flask_mail import Mail
from flask_socketio import SocketIO

mail = Mail()
socketio = SocketIO()
# Initialize the mongo instance
mongo = PyMongo()
