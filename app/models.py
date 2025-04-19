# app/models.py
from flask_login import UserMixin
from sqlalchemy import func
from app import db, login_manager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    timezone = db.Column(db.String(50), default='UTC')
    sent_requests = db.relationship('Friendship',
                                   foreign_keys='Friendship.requester_id',
                                   backref='requester',
                                   lazy='dynamic')
    received_requests = db.relationship('Friendship',
                                      foreign_keys='Friendship.addressee_id',
                                      backref='addressee',
                                      lazy='dynamic')

class CalendarEvent(db.Model):
    __tablename__ = 'calendar_event'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  #Corresponding to the dd/mm/yyyy format in the image
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    attachment_path = db.Column(db.String(200))  #Store the 'Attach File' path in the image
    visibility = db.Column(db.String(10), default='private')  
    __table_args__ = (
        db.CheckConstraint(
            "visibility IN ('private', 'public', 'friends')", 
            name='check_visibility'
        ),
    )

    #The mixed attributes required for cross month display in the image
    @hybrid_property
    def iso_date(self):
        return self.date.strftime('%Y-%m-%d')
    
    @iso_date.expression
    def iso_date(cls):
        return func.strftime('%Y-%m-%d', cls.date)

#Friend Relationship Table (supports friend sharing function )
class Friendship(db.Model):
    __tablename__ = 'friendship'
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    addressee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint('requester_id', 'addressee_id', name='unique_friendship'),  # ✨ 新增
    )

#Event sharing table (implementing the Sharing ->Friends option )
class EventShare(db.Model):
    __tablename__ = 'event_share'
    event_id = db.Column(db.Integer, db.ForeignKey('calendar_event.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    access_level = db.Column(db.Enum('view', 'edit'), default='view')