import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    csrf.init_app(app)
    #Set login endpoint (using blueprint name prefix)
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    #Registration blueprint (key modification: use urlprepaix='/')
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    return app
