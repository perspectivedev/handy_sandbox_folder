# -------------------- Start File imports --------------------
from flask_app import app, socketio
from flask_app.controllers import chat_controller, users_controller, rooms_controller
# -------------------- End File imports --------------------

if __name__ == '__main__':
    socketio.run(app, debug=True)