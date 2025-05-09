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


#start_time/end_time uses the DATE type (storing both date and time)
#
# 
#privacey_level reserved for subsequent permission control
class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)  # Include date and time
    end_time = db.Column(db.DateTime, nullable=False)
    
    privacy_level = db.Column(db.String(20), default='private')  # private/friends/specific_users
    shared_with = db.Column(db.String(255), nullable=True) #friends ID
    
    # Associated users
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('events', lazy=True))

    def __repr__(self):
        return f'<Event {self.title} ({self.start_time} to {self.end_time})>'
    
#Add friend functionality start here  
class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='friends')
    friend = db.relationship('User', foreign_keys=[friend_id])

    def __repr__(self):
        return f'<Friendship {self.user_id} -> {self.friend_id}>'
    
