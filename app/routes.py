from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, LoginManager
from app.models import User

main_routes = Blueprint('main', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_routes.route('/')
def home():
    return render_template('index.html')

@main_routes.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@main_routes.route('/register', methods=['GET'])
def register():
    return render_template('register.html')s