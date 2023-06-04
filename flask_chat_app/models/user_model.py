# ---------------------- File Imports ---------------------->
from flask_chat_app import app
from flask_chat_app.config.mysqlconnection import connectToMySQL
from flask_chat_app import  DATABASE
from flask_chat_app.models import team_model
from flask_bcrypt import Bcrypt
from flask import flash 
bcrypt = Bcrypt(app)
import re
# -------------------- Regex variables --------------------
ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# -------------------- class declaration and constructor init --------------------

class User:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
# -------------------- @classmethods --------------------

# This classmethod will create the user from the db after reg.
    @classmethod
    def create_user(cls,data):
        query = """
        INSERT INTO users (username, email, password)
        VALUES (%(username)s, %(email)s, %(password)s)
        """
        print('This is the print statement for user_reg:',data)
        return connectToMySQL(DATABASE).query_db(query, data)

# This classmethod will get the user by id.
    @classmethod
    def get_one_user_by_id(cls, data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        query_results = connectToMySQL(DATABASE).query_db(query, data)
        if query_results:
            return cls(query_results[0])
        return False 

    # This classmethod will create a dictionary by the users assigned id in the db.
    @classmethod
    def get_by_id_dict(cls,data):
        query = """
            SELECT * FROM users 
            LEFT JOIN teams_has_users 
            ON teams_has_users.user_id = users.id
            WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            user = {
                'username': results[0]['username'],
                'id': results[0]['id']
            }
            user['joined_team_ids'] = []
            for row in results:
                user['joined_team_ids'].append(row['team_id'])
            return user
        return False

    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM users 
            LEFT JOIN teams_has_users 
            ON teams_has_users.user_id = users.id
            LEFT JOIN teams
            ON teams_has_users.team_id = teams.id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            user = cls(results[0])
            user.joined_rooms = []
            for row in results:
                if row['teams.id'] == None:
                    return user
                team_data = {
                    **row,
                    'id': row['teams.id'],
                    'created_at': row['teams.created_at'],
                    'updated_at': row['teams.updated_at']
                }
                user.joined_rooms.append(team_model.Team(team_data))
            return user
        return False

# This classmethod gets all the users in the db
    @classmethod
    def get_all_users(cls,data):
        query = """
        SELECT * FROM users;
        """
        users_from_db = connectToMySQL(DATABASE).query_db(query, data)
        users = []
        for self_user in users_from_db:
            users.append(cls(self_user))
        return users

# This classmethod gets the user email.
    @classmethod
    def get_user_username(cls, data):
        query = """
        SELECT * FROM users WHERE username = %(username)s;
        """
        query_results = connectToMySQL(DATABASE).query_db(query,data)
        
        if query_results:
            return cls(query_results[0])
        return False

# -------------------- @staticmethods --------------------

    @staticmethod
    def user_validator(data):
        is_valid = True
        if len(data['username']) < 1:
            is_valid = False
            flash('Username required', 'reg')
        elif len(data['username']) < 2:
            is_valid = False
            flash('Username must be at least 2 Character', 'reg')
        elif not ALPHA.match(data['username']):
            is_valid = False
            flash('Username must be letters only', 'reg')
        if len(data['email']) < 1:
            is_valid = False
            flash('Email required', 'reg')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Email must be valid format', 'reg')
        else:
            potential_user = User.get_user_email({'email': data['email']})
            if potential_user:
                is_valid = False
                flash('Email must be valid format', 'reg')
        if len(data['password']) < 1:
            flash('pass req', 'reg')
            is_valid = False
        elif len(data['password']) < 8:
            flash('pass must be > 8 char', 'reg')
            is_valid = False
            
        return is_valid
    
