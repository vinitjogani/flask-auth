from flask import Blueprint, render_template, redirect, request, make_response
from .decorators import login_forbidden
from .models import User

auth = Blueprint('auth', __name__, template_folder='templates/auth/')


@login_forbidden
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        token = User.authenticate_user(username, password)
        if token:
            response = make_response(redirect('/dashboard'))
            response.set_cookie('token', token)
            return response
        else:
            return render_template('auth/login.html', error='Login unsuccessful.')
    return render_template('auth/login.html')


@login_forbidden
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        if password != confirm:
            return render_template('auth/register.html', error='Passwords don\'t match.')
        elif User.get_user(username) is not None:
            return render_template('auth/register.html', error='User with that email already exists.')
        else:
            User.create_user(username=username, password=password)
            token = User.authenticate_user(username, password)
            response = make_response(redirect('/'))
            response.set_cookie('token', token)
            return response
    return render_template('auth/register.html')


@auth.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie('token', '')
    return response
