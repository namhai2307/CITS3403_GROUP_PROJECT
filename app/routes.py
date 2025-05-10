"""
Routes for the Flask application.

This module defines the routes for the application, including user authentication,
event management, and API endpoints. It uses Flask blueprints to organize the routes.
"""

from flask import Blueprint, abort, redirect, render_template, url_for, session, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from . import  db
from .forms import LoginForm, SignUpForm,EventForm  
from .models import User,Event 
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    """
    Render the home page.
    """  
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    If the user is already authenticated, redirect to the dashboard.
    
    Otherwise, validate the login form and authenticate the user.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

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
    """
    Handle user registration.

    Validate the signup form and create a new user account if valid.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('Username or email already exists. Please try again.', 'error')
            return redirect(url_for('main.signup'))
            
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('main.signup'))
            
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
    """
    Render the user profile page.

    Allows searching for other users by username.
    """
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            users = User.query.filter(User.username.ilike(f'%{search_query}%')).all()
            return render_template('profile.html', users=users, search_query=search_query)
    else:
        return render_template('profile.html', users=None)
    
@main.route('/search_users', methods=['POST'])
def search_users():
    """
    API endpoint to search for users by username.

    Returns a JSON response with matching users.
    """
    search_query = request.json.get('search_query', '').strip()
    if search_query:
        users = User.query.filter(User.username.ilike(f'%{search_query}%')).all()
        return jsonify([{'username': user.username, 'email': user.email} for user in users])
    return jsonify([])

@main.route('/logout')
@login_required
def logout():
    """
    Log out the current user and redirect to the home page.
    """
    logout_user()  
    session.pop('logged_in', None) 
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Render the dashboard page.

    Displays calendar events for the selected date and allows users to create new events.
    """
    form = EventForm()
    
    date_str = request.args.get('date')
    try:
        display_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()
    except ValueError:
        display_date = datetime.utcnow().date()

    if form.validate_on_submit():
        try:
            event = Event(
                title=form.title.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                description=form.description.data,
                
                privacy_level=form.privacy_level.data,  
                user_id= current_user.id,
                created_by=current_user.id  # New: Set Creator

            )
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('main.dashboard', date=display_date.strftime('%Y-%m-%d')))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    start_of_day = datetime.combine(display_date, datetime.min.time())
    end_of_day = datetime.combine(display_date, datetime.max.time())

    daily_events = Event.query.filter(
        Event.user_id == current_user.id,
        Event.start_time >= start_of_day,
        Event.start_time <= end_of_day
    ).order_by(Event.start_time).all()

    start_of_month = datetime(display_date.year, display_date.month, 1)
    if display_date.month == 12:
        end_of_month = datetime(display_date.year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end_of_month = datetime(display_date.year, display_date.month + 1, 1) - timedelta(seconds=1)

    monthly_events = Event.query.filter(
        Event.user_id == current_user.id,
        Event.start_time >= start_of_month,
        Event.start_time <= end_of_month
    ).order_by(Event.start_time).all()

    event_durations = {}
    for event in monthly_events:
        day = event.start_time.strftime('%Y-%m-%d')  
        duration = (event.end_time - event.start_time).total_seconds() / 3600  
        if day not in event_durations:
            event_durations[day] = 0
        event_durations[day] += duration

    return render_template(
        'dashboard.html',
        form=form,
        events=daily_events,
        display_date=display_date,
      
        event_durations=event_durations,  # Pass durations instead of counts
        timedelta=timedelta  ,
        current_user_id= current_user.id  #New: Transfer the current user ID to the template

    )

@main.route('/api/events/<date>', methods=['GET'])
@login_required
def get_events_by_date(date):
    """Retrieve the event list for the specified date"""
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        start_of_day = datetime.combine(date_obj, datetime.min.time())
        end_of_day = datetime.combine(date_obj, datetime.max.time())
        
        events = Event.query.filter(
            Event.start_time >= start_of_day,
            Event.start_time <= end_of_day,
            
            Event.user_id == current_user.id  # Only return events for the current user
        ).order_by(Event.start_time).all()
        
        return jsonify([{
            'id': e.id,
            'title': e.title,
            'start_time': e.start_time.isoformat(),
            'end_time': e.end_time.isoformat(),
            'description': e.description,
            'created_by': e.created_by
        } for e in events])
    
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

@main.route('/api/events/<int:event_id>', methods=['PUT'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.created_by != current_user.id:  
        abort(403)
    
    data = request.get_json()  
    print("Received data:", data)  
    
    
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data.get('description')
    if 'start_time' in data:
        event.start_time = datetime.fromisoformat(data['start_time'])
    if 'end_time' in data:
        event.end_time = datetime.fromisoformat(data['end_time'])
    if 'privacy_level' in data:
        event.privacy_level = data['privacy_level']
    
    db.session.commit()  
    return jsonify({'status': 'success'})

@main.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.created_by != current_user.id:
        abort(403)
        
    db.session.delete(event)
    db.session.commit()  
    return jsonify({'status': 'deleted'})




@main.route('/help')
def help():
    """
    Render the help page.

    For users to find assistance and information about the how to get started with calendar web app.
    """
    return render_template('help.html')

@main.route('/visualisation')
@login_required
def visualisation():
    """
    Render the visualisation page.

    Displays a list of friends and their calendar event durations.
    """
    friends = User.query.filter(User.id != current_user.id).all()  
    return render_template('visualisation.html', friends=friends, event_durations={})

@main.route('/api/friend_calendar/<int:friend_id>')
@login_required
def friend_calendar(friend_id):
    """
    API endpoint to retrieve a friend's calendar events for the current month.

    Returns a JSON response with event durations grouped by day.
    """
    friend = User.query.get_or_404(friend_id)

    start_of_month = datetime.now().replace(day=1)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(seconds=1)

    events = Event.query.filter(
        Event.user_id == friend.id,
        Event.start_time >= start_of_month,
        Event.start_time <= end_of_month
    ).all()

    event_durations = {}
    for event in events:
        day = event.start_time.strftime('%Y-%m-%d')
        duration = (event.end_time - event.start_time).total_seconds() / 3600
        event_durations[day] = event_durations.get(day, 0) + duration

    return jsonify({'eventDurations': event_durations})

@main.route('/api/events')
@login_required
def get_events():
    """
    API endpoint to retrieve events for a specific date.

    Returns a JSON response with event details for the selected date.
    """
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date is required'}), 400

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    start_of_day = datetime.combine(selected_date, datetime.min.time())
    end_of_day = datetime.combine(selected_date, datetime.max.time())

    events = Event.query.filter(
        Event.user_id == current_user.id,
        Event.start_time >= start_of_day,
        Event.start_time <= end_of_day
    ).order_by(Event.start_time).all()

    events_data = [
        {
            'title': event.title,
            'start_time': event.start_time.strftime('%H:%M'),
            'end_time': event.end_time.strftime('%H:%M'),
            'description': event.description
        }
        for event in events
    ]

    return jsonify({'events': events_data})