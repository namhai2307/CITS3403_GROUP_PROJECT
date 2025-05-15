"""
Configuration settings for the Flask application.

This module defines configuration classes for different environments, such as
development and testing. It also sets up default configurations like the secret key
and database settings.
"""

import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'app.db')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"





    
