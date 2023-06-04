# ------------------------------------- file imports ------------------------------------->
from flask import Flask
from flask_socketio import SocketIO
# from flask_chat_app.static.js import chat

# ------------------------------------- file imports ------------------------------------->


app = Flask(__name__)
app.secret_key = 'my_secret_chat'

socketio = SocketIO(app)
DATABASE = "cah_schema"