import os
 # 加载.env文件

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'csv', 'json'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB限制

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DB_URL')
    