"""
Persona Service application factory and configuration
"""
import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    """
    Create and configure the Flask application instance
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    if test_config is None:
        app.config.from_object('app.config')
        # Override with instance config if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Ensure the data directory exists
    if not os.path.exists('data'):
        os.makedirs('data', exist_ok=True)
    
    # Set up extensions
    from app.extensions import db, jwt, ma
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    
    # Configure CORS
    origins = app.config.get('CORS_ORIGINS', '*')
    CORS(app, resources={r"/api/*": {"origins": origins}})
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Simple health check endpoint"""
        return {'status': 'ok', 'version': '1.0.0'}

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app
