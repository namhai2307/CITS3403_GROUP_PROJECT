from flask import Blueprint, render_template, jsonify, redirect, request, url_for, flash
from .models import db, User, CalendarEvent, Friendship, EventShare
from .forms import EventForm, FriendRequestForm
from flask_login import login_required, current_user



main = Blueprint('main', __name__)

@main.route('/')
def index():  
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/signup')
def signup():
    return render_template('sign_up_page.html')


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html') 

@main.route('/calendar_data', methods=['GET'])
@login_required
def get_calendar_data():
    friends_ids = [
        f.addressee_id for f in current_user.sent_requests.filter_by(status='accepted')
    ] + [
        f.requester_id for f in current_user.received_requests.filter_by(status='accepted')
    ]
    
    
    start_date = request.args.get('start', '2025-04-01')  
    end_date = request.args.get('end', '2025-04-30')
    
    events = CalendarEvent.query.filter(
        CalendarEvent.date.between(start_date, end_date),
        CalendarEvent.user_id.in_([current_user.id] + friends_ids)
    ).all()
    
    return jsonify([{
        'title': e.title,
        'start': e.iso_date,
        'extendedProps': {
            'description': e.description,
            'is_own': e.user_id == current_user.id  
        }
    } for e in events])

#Submit the 'Add to Calendar' button for processing
@main.route('/create_event', methods=['POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        if form.attachment.data:
            filename = secure_filename(form.attachment.data.filename)  
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.attachment.data.save(filepath)
        else:
            filepath = None

        new_event = CalendarEvent(
            user_id=current_user.id,
            date=form.date.data,
            title=form.title.data,
            description=form.description.data,
            visibility=form.sharing.data
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Event added!', 'success')
    return redirect(url_for('main.dashboard'))