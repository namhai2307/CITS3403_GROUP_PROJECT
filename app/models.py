"""
Database models for the Web app.

This module defines the `User` and `Event` models, which represent the users
and events in the application. It also includes helper methods for password
management and user loading.
"""

from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime
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
    Represents a calendar event in the system.

    Attributes:
        __tablename__ (str): Name of the table in the database ('events').
        id (int): Primary key for the event.
        title (str): Title of the event (required, max 100 characters).
        description (str): Optional detailed description of the event.
        start_time (datetime): Datetime when the event starts (required).
        end_time (datetime): Datetime when the event ends (required).
        privacy_level (str): Visibility of the event ('private' by default).
        user_id (int): Foreign key referencing the User the event is associated with.
        created_by (int): Foreign key referencing the User who created the event.

    Relationships:
        user (User): The user the event is for (via user_id).
        creator (User): The user who created the event (via created_by).

    Methods:
        __repr__(): Returns a string representation of the event with title and times.
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
    
class Friendship(db.Model):
    """
    Represents a friendship relationship between two users.

    Attributes:
        __tablename__ (str): Name of the table in the database ('friendships').
        id (int): Primary key for the friendship.
        user_id (int): Foreign key referencing the user initiating the friendship.
        friend_id (int): Foreign key referencing the user who is the friend.
        status (str): Status of the friendship request (default is 'pending').

    Relationships:
        user (User): The user who initiated the friendship (via user_id).
        friend (User): The user being added as a friend (via friend_id).

    Methods:
        __repr__(): Returns a string representation of the friendship instance.
    """
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending') 

    user = db.relationship('User', foreign_keys=[user_id], backref='friends')
    friend = db.relationship('User', foreign_keys=[friend_id])

    def __repr__(self):
        return f'<Friendship {self.user_id} -> {self.friend_id} ({self.status})>'

class Message(db.Model):
    """
    Represents a message sent between two users.

    Attributes:
        id (int): Primary key for the message.
        sender_id (int): Foreign key referencing the user who sent the message.
        recipient_id (int): Foreign key referencing the user who received the message.
        content (str): The body text of the message (required).
        timestamp (datetime): Time the message was sent (default is the current time).
        read (bool): Whether the message has been read (default is False).
        room (str): Optional name or ID of the chat room the message belongs to.

    Relationships:
        sender (User): The user who sent the message (via sender_id).
        recipient (User): The user who received the message (via recipient_id).
    """
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    read = db.Column(db.Boolean, default=False)
    room = db.Column(db.String(100), nullable=True)  

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')