# ------------------------------------- File imports ------------------------------------->
from flask import Flask
from flask import flash
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_chat_app.config.mysqlconnection import connectToMySQL
from flask_chat_app import DATABASE
# bcrypt = Bcrypt(app)
import re
# -------------------- Regex variables --------------------
ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# ------------------------------------- class declaration ------------------------------------->

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.sender = data['sender']
        self.room_id = data['room_id']


# ------------------------------------- @classmethods ------------------------------------->
    @classmethod
    def create_message(cls, data):
        query = """
        INSERT INTO messages (content,user_id, sender_id)
        VALUES (%(content)s, %(user_id)s, %(sender_id)s); 
        """
        print(data)
        return connectToMySQL(DATABASE).query_db(query, data)



# ------------------------------------- @staticmethods ------------------------------------->
