"""
Application factory and initialization for the Flask application.

This module sets up the Flask application using the factory pattern. It initializes
extensions such as SQLAlchemy, Flask-Migrate, and Flask-Login, and registers blueprints
for routing. The configuration can be dynamically loaded based on the provided
configuration class.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import DevelopmentConfig
from flask_wtf import CSRFProtect
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  
csrf = CSRFProtect()
socketio =SocketIO(async_mode='threading')

def create_app(config_class=None):
    """
    Factory method to create and configure the Flask application.

    This function initializes the Flask application, loads the configuration,
    initializes extensions, and registers blueprints.

    Args:
        config_class (class, optional): The configuration class to use for the app.
            If not provided, defaults to `DevelopmentConfig`.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    return app
