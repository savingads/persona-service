"""
Extensions used by the Persona Service
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
