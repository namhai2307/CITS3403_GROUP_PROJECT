import os


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-123!'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    

    