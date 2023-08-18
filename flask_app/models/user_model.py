# -------------------- Start File imports --------------------
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import room_model
from flask import flash
import re
# -------------------- End File imports --------------------

# -------------------- Start Regex variables --------------------
ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# -------------------- End Regex variables --------------------

# -------------------- Start of Class Declaration and Constructor init --------------------
class User:
        def __init__(self, data) -> None:
                self.id = data['id']
                self.first_name = data['first_name']
                self.last_name = data['last_name']
                self.username = data['username']
                self.email = data['email']
                self.password = data['password']
                self.created_at = data['created_at']
                self.updated_at = data['updated_at']
# -------------------- End of Class Declaration and Constructor init --------------------

# -------------------- Start of  @classmethods --------------------
# This classmethod will create the user from the db after reg.
        @classmethod
        def create_user(cls,data):
                query = """
                INSERT INTO users (first_name, last_name, username, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s);
                """
                return connectToMySQL(DATABASE).query_db(query,data)

        # This classmethod will get the user
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
                LEFT JOIN users_join_rooms
                ON users_join_rooms.user_id = users.id
                WHERE id = %(id)s;
                """
                results = connectToMySQL(DATABASE).query_db(query,data)
                if results:
                        user = {
                                'username': results[0]['username'],
                                'id': results[0]['id']
                        }

                user['joined_room_ids'] = []
                for row in results:
                        user['joined_room_ids'].append(row['room_id'])
                        return user
                print(user)
                return False

        @classmethod
        def get_by_id(cls,data):
                query = """
                        SELECT * FROM users 
                        LEFT JOIN users_join_rooms 
                        ON users_join_rooms.user_id = users.id
                        LEFT JOIN rooms
                        ON users_join_rooms.room_id = rooms.id
                        WHERE users.id = %(id)s;
                """
                results = connectToMySQL(DATABASE).query_db(query,data)
                
                if results:
                        user = cls(results[0])
                        user.joined_rooms = []
                        for row in results:
                                if row['rooms.id'] == None:
                                        return user
                                room_data = {
                                        **row,
                                        'id': row['rooms.id'],
                                        'created_at': row['rooms.created_at'],
                                        'updated_at': row['rooms.updated_at']
                                }
                                user.joined_rooms.append(room_model.Room(room_data))
                        return user
                return False
        
        
        
        # This classmethod gets the user email.
        @classmethod
        def get_user_email(cls, data):
                query = """
                SELECT * FROM users WHERE email = %(email)s;
                """
                query_results = connectToMySQL(DATABASE).query_db(query, data)
                
                if query_results:
                        return cls(query_results[0])
                return False

        @classmethod
        def get_by_username(cls, data):
                query = """
                SELECT * FROM users WHERE username = %(username)s;
                """
                query_results = connectToMySQL(DATABASE).query_db(query,data)
                print(query_results)
                if query_results:
                        print(cls(query_results[0]))
                        return cls(query_results[0])
                return False
# -------------------- End of  @classmethods --------------------

# -------------------- Start of  @staticmethods --------------------
        # This staticmethod is used for form validation.
        @staticmethod
        def user_validator(data):
                is_valid = True
                if len(data['first_name']) < 1:
                        is_valid = False
                        flash('First name required', 'reg')
                elif len(data['first_name']) < 2:
                        is_valid = False
                        flash('First name must be 2 characters', 'reg')
                elif not ALPHA.match(data['first_name']):
                        is_valid = False
                        flash('First name must be letter only', 'reg')
                if len(data['last_name']) < 1:
                        is_valid = False
                        flash('Last name required', 'reg')
                elif len(data['last_name']) < 2:
                        is_valid = False
                        flash('Last name must be 2 characters', 'reg')
                elif not ALPHA.match(data['last_name']):
                        is_valid = False
                        flash('Last name must be letter only', 'reg')
                if len(data['username']) < 1:
                        is_valid = False
                        flash('Username required', 'reg')
                elif len(data['username']) < 2:
                        is_valid = False
                        flash('Username must be at least 2 characters', 'reg')
                elif not ALPHA.match(data['username']):
                        is_valid = False
                        flash('Username must be letter only', 'reg')
                else:
                        potential_user = User.get_by_username({'username': data['username']})
                        if potential_user:
                                is_valid = False
                                flash('Username already exist in database', 'reg')
                if len(data['email']) < 1:
                        is_valid = False
                        flash('Email required', 'reg')
                elif not EMAIL_REGEX.match(data['email']):
                        is_valid = False
                        flash('Email must be valid format.', 'reg')
                if len(data['password']) < 1:
                        is_valid = False
                        flash('pass reg', 'reg')
                elif len(data['password']) < 8:
                        is_valid = False
                        flash('Password must be greater than 8 characters', 'reg')
                elif data['password'] != data['confirm_pass']:
                        is_valid = False
                        flash('Password must match', 'reg')
                
                return is_valid
# -------------------- End of  @staticmethods --------------------