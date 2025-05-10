from flask import Blueprint, redirect, render_template, url_for, session, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from . import  db

from .forms import LoginForm, SignUpForm,EventForm  
from .models import User,Event, Friendship  # Import User Model

from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
import os

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

        #Check that user ane password from the database match
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True) 
            session['logged_in'] = True 
            flash('Login successful! Welcome back, {}.'.format(user.username), 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = SignUpForm()
    if form.validate_on_submit():
        # Check if the username and email already exist
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('Username or email already exists. Please try again.', 'error')
            return redirect(url_for('main.signup'))
            
        #Verify password match
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('main.signup'))
            
        #Create User
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('sign_up.html', form=form)



@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            # Query the database for users matching the search query
            users = User.query.filter(User.username.ilike(f'%{search_query}%')).all()
            return render_template('profile.html', users=users, search_query=search_query)
    else:
        # Render the page without search results
        return render_template('profile.html', users=None)
    
@main.route('/search_users', methods=['POST'])
def search_users():
    search_query = request.json.get('search_query', '').strip()
    if search_query:
        users = User.query.filter(User.username.ilike(f'%{search_query}%')).all()
        return jsonify([{'username': user.username, 'email': user.email} for user in users])
    return jsonify([])

@main.route('/logout')
@login_required
def logout():
    logout_user()  
    session.pop('logged_in', None) #reset the session to none, since user logged out
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = EventForm()
    
    # Retrieve the date parameter from the request (default is today)
    date_str = request.args.get('date')
    try:
        display_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()
    except ValueError:
        display_date = datetime.utcnow().date()


    # Process form submission
    if form.validate_on_submit():
        try:
            
            event = Event(
                title=form.title.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                description=form.description.data,
                
                privacy_level=form.privacy_level.data,  
                user_id=current_user.id
            )
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    # Query the events of the day
    start_of_day = datetime.combine(display_date, datetime.min.time())
    end_of_day = datetime.combine(display_date, datetime.max.time())

    events = Event.query.filter(
        Event.user_id == current_user.id,
        Event.start_time >= start_of_day,
        Event.start_time <= end_of_day
    ).order_by(Event.start_time).all()



    # When GET request or verification fails
    return render_template('dashboard.html', form=form, 
                         events=events,
                         display_date=display_date)

@main.route('/help')
def help():
    return render_template('help.html')

#Add friend section
@main.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    friend_id = request.form.get('friend_id')
    if friend_id:
        # Check if the friendship already exists
        existing_friendship = Friendship.query.filter_by(user_id=current_user.id, friend_id=friend_id).first()
        if not existing_friendship:
            # Add the friendship
            friendship = Friendship(user_id=current_user.id, friend_id=friend_id)
            db.session.add(friendship)
            db.session.commit()
            flash('Friend added successfully!', 'success')
        else:
            flash('You are already friends with this user.', 'info')
    else:
        flash('Invalid friend ID.', 'error')
    return redirect(url_for('main.profile'))