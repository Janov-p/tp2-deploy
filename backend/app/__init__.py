from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restx import Api

from .config import config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
api = Api(
    title='Flask Authentication API',
    version='1.0',
    description='A secure RESTful API with JWT authentication'
)

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    
    # Add API namespaces
    from .auth.api import api as auth_api
    api.add_namespace(auth_api)
    
    # Initialize API with app
    api.init_app(app)
    
    # Register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')  # Explicitly set url_prefix
    
    # Configure CORS
    CORS(app, 
         resources={r"/*": {
             "origins": ["http://localhost:5173", "https://tp-deploy.web.app"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "expose_headers": ["Content-Type", "Authorization"]
         }}
    )
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app