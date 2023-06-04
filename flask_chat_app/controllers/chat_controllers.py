# --------------------------------------- File Imports --------------------------------------->
from flask import Flask
from flask_socketio import SocketIO
from flask_chat_app import app, socketio
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, request, flash, session
from flask_chat_app.config.mysqlconnection import connectToMySQL
from flask_chat_app import DATABASE
from flask_chat_app.models.user_model import User
from flask_chat_app.models.team_model import Team
from flask_chat_app.models.message_model import Message
from flask_socketio import emit, join_room, leave_room, send
# --------------------------------------- Socketio/Routes --------------------------------------->


@socketio.on('message')
def handle_message(message):
    message.emit('message', message, broadcast=True)

# --------------------------------------- File Imports --------------------------------------->
# --------------------------------------- File Imports --------------------------------------->
# --------------------------------------- File Imports --------------------------------------->