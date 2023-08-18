# -------------------- Start File imports --------------------
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.room_model import Room
bcrypt = Bcrypt(app)
# -------------------- End File imports --------------------

# -------------------- Start Controllers/Routes for models --------------------
# This route is to establish the index page
@app.route('/')
def index():
# Conditional rendering statement for user reg.
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

# This route deals with the post method of the html form. route should match the action on the form.
@app.route('/users/registration', methods=['POST'])
def user_registration():
    print(request.form)
    potential_user = User.user_validator(request.form)
    if not potential_user:
        return redirect('/')
    
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        **request.form,
        'password': hashed_pass,
        'confirm_pass': hashed_pass
    }
    logged_user_id = User.create_user(data)
    session['user_id'] = logged_user_id
    return redirect('/dashboard')

# This deals with the "my_rooms.html"
@app.route('/my_rooms')
def my_rooms():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    public = Room.public_get_created_by_user_id(user_data)
    return render_template('my_rooms.html', logged_user=logged_user, public=public)

# This route deal with the post method of the user login. Action on the form should match.
@app.route('/users/login', methods=['POST'])
def user_login():
    data = {
        'username': request.form['username']
    }
    potential_user = User.get_by_username(data)
    if not potential_user:
        flash('Invalid credentials', 'log')
        print('User not found')
        return redirect('/')
    
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash('Invalid credentials', 'log')
        print('invlid pss')
        return redirect('/')
    session['user_id'] = potential_user.id
    return redirect('/dashboard')

# This route handles the logged in user.
@app.route('/api/users/get_logged_user')
def get_logged_user():
    if 'user_id' not in session:
        return redirect('/')
    return User.get_by_id_dict({'id': session['user_id']})

# This route logout's the user from the session.
@app.route('/users/logout')
def user_logout():
    del session['user_id']
    return redirect('/')
# -------------------- End Controllers/Routes for models --------------------

# -------------------- Start of Class Declaration and Constructor init --------------------

# -------------------- End of Class Declaration and Constructor init --------------------

# -------------------- Start of  @classmethods --------------------

# -------------------- End of  @classmethods --------------------

# -------------------- Start of  @staticmethods --------------------

# -------------------- End of  @staticmethods --------------------