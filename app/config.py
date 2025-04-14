"""
Configuration for the Persona Service API
"""
import os
from datetime import timedelta

# Database settings
import os.path
# Use absolute path for SQLite database to avoid path resolution issues
db_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'persona_service.db'))
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", f"sqlite:///{db_path}")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# API settings
API_VERSION = "v1"
API_TITLE = "Persona Service API"
API_DESCRIPTION = "API for managing user personas"

# JWT settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")  # Change in production!
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_HOURS", "1")))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_DAYS", "30")))

# Security settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
