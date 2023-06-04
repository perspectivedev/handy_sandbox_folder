# ------------------- File Imports ------------------->
from flask_chat_app import app
from flask_chat_app.config.mysqlconnection import connectToMySQL
from flask_chat_app import DATABASE
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
# ------------------- Regex Variables ------------------->
ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
# ------------------- Class declaration and constructor init ------------------->

class Team:
    def __init__(self, data):
        self.team_name = data['team_name']
        self.team_score = data['team_score']
        self.create_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.user_id = data['user_id']
        self.room_id = data['room_id']
        self.invite_id = data['invite_id']

# ------------------- @classmethods ------------------->

    @classmethod
    def create_team(cls,data):
        query = """
        INSERT INTO teams (team_name, creator_id)
        VALUES (%(team_name)s,%(creator_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def create_private(cls,data):
        query = """
        INSERT INTO teams (team_name, creator_id, private)
        VALUES (%(team_name)s,%(creator_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_public_team(cls):
        query = """
        SELECT * FORM teams WHERE creator_id = 0;
        """
        query_results = connectToMySQL(DATABASE).query_db(query)
        all_teams = []
        for row in query_results:
            all_teams.append(cls(row))
        return all_teams
    
    @classmethod
    def get_team_by_id(cls,data):
        query = """
        SELECT * FROM teams WHERE id = %(id)s;
        """
        query_results = connectToMySQL(DATABASE).query_db(query,data)
        if query_results:
            return cls(query_results)
        return False
    
    @classmethod
    def public_get_created_by_user_id(cls,data):
        query = """
        SELECT *, COUNT(teams_has_users.user_id) as joined FROM teams
        JOIN users ON users.id = teams.creator_id
        LEFT JOIN teams_has_users ON teams.id = teams_has_users.team_id
        WHERE users.id = %(id)s AND  teams.creator_id = 0
        GROUP BY teams.id;
        """
        query_results = connectToMySQL(DATABASE).query_db(query,data)
        teams = []
        if query_results:
            for row in query_results:
                team = cls(row)
                team.joined = row['joined']
                teams.append(team)
            return teams
        
        @classmethod
        def get_by_team_name(cls,data):
            query = """
            SELECT * FROM teams WHERE team_name = %(id)s;
            """
            query_results = connectToMySQL(DATABASE).query_db(query, data)
            if query_results:
                return cls(query_results[0])
            return False
        
        @classmethod
        def get_history_by_id(cls, data):
            data = {
                **data,
                'format': r"%m/%d/%Y,%r"
            }
            query = """
            SELECT team_name, content, username, DATE_FORMAT(messages.created_at, %(format)s) as created_at FROM teams
            LEFT JOIN messages ON messages.team_id = teams.id
            LEFT JOIN users ON messages.sender_id = users.id
            WHERE teams.id = %(id)s;
            """
            query_results = connectToMySQL(DATABASE).query_db(query, data)
            if query_results[0]['content'] == None:
                return [{'team_name': query_results[0]['team_name'], 'content': 'Start us off!', 'username': 'nothing', 'created_at': 'this time'}]
            return query_results
        
        @classmethod
        def leave_team(cls,data):
            query = """
            DELET FROM teams_has_users
            WHERE team_id = %(team_id)s AND user_id = %(user_id)s;
            """
            return connectToMySQL(DATABASE).query_db(query, data)
        
        @classmethod
        def join_team(cls, data):
            query = """
            INSERT INTO teams_has_users (team_id, user_id)
            VALUES (%(team_id)s,%(user_id)s);
            """
            return connectToMySQL(DATABASE).query_db(query, data)
        
        @classmethod
        def delete_team(cls,data):
            query = """"
            DELETE FROM teams WHERE id = %(id)s;
            """
            return connectToMySQL(DATABASE).query_db(query,data)

# ------------------- @staticmethods ------------------->
