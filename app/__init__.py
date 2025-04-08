from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config



db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Expand initialization
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    
    
    from .models import User
    from app.routes import main 
    app.register_blueprint(main)
    
    return app
