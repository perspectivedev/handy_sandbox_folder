# -------------------- Start File imports --------------------
from flask import Flask
from flask_socketio import SocketIO
# -------------------- End File imports --------------------

app = Flask(__name__)
app.secret_key = "secret_cards"

socketio = SocketIO(app)
DATABASE = "chat_app_flask"