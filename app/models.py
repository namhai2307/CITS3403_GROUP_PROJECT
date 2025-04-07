from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    achievements = db.relationship('Achievement', backref='user', lazy='dynamic')

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    category = db.Column(db.String(50))  # 健身/学习/咖啡等
    duration = db.Column(db.Integer)     # 持续时间（分钟）
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shared_with = db.Column(db.JSON)     # 存储分享用户ID列表