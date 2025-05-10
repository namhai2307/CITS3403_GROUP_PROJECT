"""
Database models for the Web app.

This module defines the `User` and `Event` models, which represent the users
and events in the application. It also includes helper methods for password
management and user loading.
"""

from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """
    Represents the user's data structure in the application.

    Attributes:
        id (int): The primary key for the user.
        username (str): The unique username of the user.
        email (str): The unique email address of the user.
        password_hash (str): The hashed password of the user.
    """
    __tablename__ = 'user' 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Event(db.Model):
    """
    Represents the event data structure in the application.

    Attributes:
        id (int): The primary key for the event.
        title (str): The title of the event.
        description (str): A detailed description of the event.
        start_time (datetime): The start date and time of the event.
        end_time (datetime): The end date and time of the event.
        privacy_level (str): The privacy level of the event (e.g., private, friends).
        user_id (int): The ID of the user who created the event.
        user (User): The user object associated with the event.
    """

    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)  
    end_time = db.Column(db.DateTime, nullable=False)
    
    privacy_level = db.Column(db.String(20), default='private')  
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    

    user = db.relationship('User', foreign_keys=[user_id], backref='events')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_events')

    def __repr__(self):
        return f'<Event {self.title} ({self.start_time} to {self.end_time})>'
    
#Add friend functionality start here  
class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending' or 'accepted'

    user = db.relationship('User', foreign_keys=[user_id], backref='friends')
    friend = db.relationship('User', foreign_keys=[friend_id])

    def __repr__(self):
        return f'<Friendship {self.user_id} -> {self.friend_id} ({self.status})>'
