# ------------------- File Imports ------------------->
from flask_chat_app import app
from flask import render_template, request, redirect, flash, session
from flask_bcrypt import Bcrypt
from flask_chat_app.models.user_model import User
from flask_chat_app.models.team_model import Team
bcrypt = Bcrypt(app)
# ------------------- Controllers/Routes for models ------------------->

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    return render_template('dashboard.html', logged_user=logged_user)

