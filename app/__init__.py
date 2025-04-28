from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    #if you want to test the file locally, need to add your own secret key here [temporary solution]

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    
    # Set login endpoint (using blueprint name prefix)
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    
    #Registration blueprint (key modification: use urlprepaix='/')
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    return app
