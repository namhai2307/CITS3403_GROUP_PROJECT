"""
config.py

Defines configuration classes for the Flask application, supporting multiple environments
such as development and testing.

Classes:

- Config:
    Base configuration class. Loads the SECRET_KEY from environment variables and disables
    SQLAlchemy modification tracking to reduce overhead.

- DevelopmentConfig(Config):
    Extends Config with settings for local development, including a file-based SQLite database.

- TestConfig(Config):
    Extends Config with testing-specific settings, using an in-memory SQLite database and
    enabling Flask's TESTING mode.

The configuration uses relative paths to set the base directory and supports environment-based
flexibility via inheritance.
"""

import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) 

class Config:
    """
    Base configuration class.

    Attributes:
        SECRET_KEY (str): Secret key used for session management and security-related features.
                          Loaded from the environment variable 'SECRET_KEY'.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disables SQLAlchemy's event system to reduce overhead.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Configuration settings for local development.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): SQLite database file located at 'app.db' in the project root.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'app.db')

class TestConfig(Config):
    """
    Configuration settings for running tests.

    Attributes:
        TESTING (bool): Enables Flask's testing mode.
        SQLALCHEMY_DATABASE_URI (str): Uses an in-memory SQLite database for fast, isolated testing.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"





    
