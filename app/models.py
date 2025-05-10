# app/models.py
from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):

    __tablename__ = 'user'  # Clearly specify the table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(128))


    def set_password(self, password):
        """encrypted password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

#User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)  # Include date and time
    end_time = db.Column(db.DateTime, nullable=False)
    
    privacy_level = db.Column(db.String(20), default='private')  # private/friends/specific_users
    
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    

    user = db.relationship('User', foreign_keys=[user_id], backref='events')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_events')

    def __repr__(self):
        return f'<Event {self.title} ({self.start_time} to {self.end_time})>'
    
    
