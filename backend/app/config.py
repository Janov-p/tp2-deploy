import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        if app.config['FLASK_ENV'] == 'production':
            if not app.config['JWT_SECRET_KEY']:
                raise ValueError("JWT_SECRET_KEY must be set in production environment")
            app.config['JWT_COOKIE_SECURE'] = True
            app.config['JWT_COOKIE_CSRF_PROTECT'] = True
            app.config['JWT_SESSION_COOKIE'] = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 