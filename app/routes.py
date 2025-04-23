from flask import Blueprint, redirect, render_template, url_for, session, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from . import  db
from .forms import LoginForm, SignUpForm
from .models import User  # Import User Model
from werkzeug.security import check_password_hash, generate_password_hash

#Initialization blueprint (named main to keep it concise)
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():  
    return render_template('index.html')



@main.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        #Using database validation instead of hard coding
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)  #Flask Login will automatically handle sessions
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email  or password', 'error')

    return render_template('login.html', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = SignUpForm()
    if form.validate_on_submit():
        #Check if the username and email already exist
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('Username or email already exists', 'error')
            return redirect(url_for('main.signup'))
            
        # Verify password match
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match', 'error')
            return redirect(url_for('main.signup'))
            
        # Create User
        user = User(
            username=form.username.data,
            email=form.email.data,  # Add email field
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Account created! Please login.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('sign_up.html', form=form)

@main.route('/dashboard')
@login_required  #Replace manual inspection with a decorator
def dashboard():
    return render_template('dashboard.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/logout')
@login_required
def logout():
    logout_user() #Flask Login will clean up sessions
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
