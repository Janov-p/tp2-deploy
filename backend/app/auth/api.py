from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from app import db
from app.auth.models import User
from app.auth.utils import token_blocklist

api = Namespace('auth', description='Authentication operations')

# API Models
user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'email': fields.String(required=True, description='User email'),
    'name': fields.String(required=True, description='User name'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

register_model = api.model('Register', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'name': fields.String(required=True, description='User name')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

token_model = api.model('Token', {
    'access_token': fields.String(description='Access token'),
    'refresh_token': fields.String(description='Refresh token')
})

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    @api.response(201, 'User successfully registered', user_model)
    @api.response(400, 'Validation error')
    def post(self):
        """Register a new user"""
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already registered'}, 400

        try:
            user = User(
                email=data['email'],
                password=data['password'],
                name=data['name']
            )
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': 'Error creating user'}, 500

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful', token_model)
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Login user and return tokens"""
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return {'error': 'Invalid credentials'}, 401

        try:
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }, 200
        except Exception as e:
            return {'error': 'Error creating tokens'}, 500

@api.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    @api.response(200, 'Token refreshed', token_model)
    def post(self):
        """Refresh access token"""
        try:
            current_user = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user)
            return {'access_token': new_access_token}, 200
        except Exception as e:
            return {'error': 'Error refreshing token'}, 500

@api.route('/logout')
class Logout(Resource):
    @jwt_required()
    @api.response(200, 'Successfully logged out')
    def post(self):
        """Logout user"""
        try:
            jti = get_jwt()["jti"]
            token_blocklist.add(jti)
            return {'message': 'Successfully logged out'}, 200
        except Exception as e:
            return {'error': 'Error logging out'}, 500

@api.route('/me')
class Me(Resource):
    @jwt_required()
    @api.response(200, 'User info retrieved', user_model)
    @api.response(404, 'User not found')
    def get(self):
        """Get current user info"""
        try:
            current_user_email = get_jwt_identity()
            user = User.query.filter_by(email=current_user_email).first()
            if not user:
                return {'error': 'User not found'}, 404
            return user.to_dict(), 200
        except Exception as e:
            return {'error': 'Error fetching user data'}, 500 