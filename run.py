# ------------------------------------- file imports ------------------------------------->
from flask_chat_app import app, socketio
from flask_chat_app.controllers import chat_controllers, teams_controllers, users_controllers
# ------------------------------------- file imports ------------------------------------->

if __name__ == '__main__':
    socketio.run(app, debug=True)