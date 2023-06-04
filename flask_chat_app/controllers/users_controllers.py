# ---------------------- File Imports ---------------------->
from flask_chat_app import app
from flask_chat_app import Flask
from flask import render_template, request, redirect, flash, session
from flask_bcrypt import Bcrypt
from flask_chat_app.models.user_model import User
from flask_chat_app.models.team_model import Team
bcrypt = Bcrypt(app)
# ---------------------- Controllers/Routes for models ---------------------->

@app.route('/')
def index():
# Conditional rendering statement for user reg.
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

# @app.route('/')
# def log_user():
#     if 'user_id' in session:
#         return redirect('/dashboard')
    
#     return render_template('dashboard.html')
    

@app.route('/user/reg', methods=['POST'])
def user_reg():
    print(request.form)
    is_valid = User.user_validator(request.form)
    if not is_valid:
        return redirect('/')
    
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        **request.form,
        'password': hashed_pass
    }
    
    logged_user_id = User.create_user(data)
    session['user_id'] = logged_user_id
    session['username'] = request.form['username']
    return redirect('/dashboard')

@app.route('/user/log', methods=['POST'])
def user_log():
    data = {
        'username': request.form['username']
    }
    potential_user = User.get_user_username(data)
    if not potential_user:
        flash('Invalid Username', 'log')
        print('Username not found')
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash('Invalid password', 'log')
        print('Invalid password')
        
    session['user_id'] = potential_user.id
    session['username'] = potential_user.username
    return redirect('/dashboard')

@app.route('/my_teams')
def my_teams():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    public = Team.public_get_created_by_user_id(user_data)
    return render_template('dashboard.html', logged_user=logged_user, public=public)

@app.route('/api/user/get_logged_user')
def get_logged_user():
    if 'user_id' not in session:
        return redirect('/')
    return User.get_by_id_dict({'id': session['user_id']})

@app.route('/user/logout')
def user_logout():
    del session['user_id']
    del session['username']
    return redirect('/')
