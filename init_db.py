#!/usr/bin/env python3
"""
Initialize the database for the Persona Service.
This script creates the database and necessary tables if they don't exist.
"""
import os
import sys
import traceback
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from app.models import Base, init_db
from app.config import SQLALCHEMY_DATABASE_URI

def create_data_directory():
    """Create the data directory if it doesn't exist"""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    
    try:
        if not os.path.exists(data_dir):
            print(f"Creating data directory: {data_dir}")
            os.makedirs(data_dir)
        
        # Ensure proper permissions
        os.chmod(data_dir, 0o755)
        return True
    except Exception as e:
        print(f"Error creating data directory: {str(e)}")
        return False

def validate_database(engine):
    """Validate that all required tables were created"""
    inspector = inspect(engine)
    required_tables = ['personas', 'demographic_data', 'persona_attributes']
    
    existing_tables = inspector.get_table_names()
    print(f"Existing tables: {', '.join(existing_tables)}")
    
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    if missing_tables:
        print(f"Warning: The following required tables are missing: {', '.join(missing_tables)}")
        return False
    
    return True

def initialize_database():
    """Initialize the database and create all tables"""
    try:
        print(f"Initializing database with URI: {SQLALCHEMY_DATABASE_URI}")
        
        # Create the session and initialize the database
        session = init_db()
        
        # Get the engine from the session
        engine = session.get_bind()
        
        # Validate that all required tables were created
        if validate_database(engine):
            print("Database initialized successfully!")
            return True
        else:
            print("Database initialization incomplete. Some tables may be missing.")
            return False
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error during database initialization: {str(e)}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"Unexpected error during database initialization: {str(e)}")
        traceback.print_exc()
        return False

def check_db_path():
    """Check if the database path is correctly set"""
    if 'sqlite:///' in SQLALCHEMY_DATABASE_URI:
        db_path = SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        db_dir = os.path.dirname(os.path.abspath(db_path))
        
        if not os.path.exists(db_dir):
            print(f"Warning: Database directory does not exist: {db_dir}")
            try:
                os.makedirs(db_dir)
                print(f"Created database directory: {db_dir}")
            except Exception as e:
                print(f"Error creating database directory: {str(e)}")
                return False
        
        # Check if directory is writable
        if not os.access(db_dir, os.W_OK):
            print(f"Warning: Database directory is not writable: {db_dir}")
            return False
    
    return True

def main():
    """Main function to initialize the database"""
    print("Starting database initialization...")
    
    # Create data directory if it doesn't exist
    if not create_data_directory():
        sys.exit(1)
    
    # Check database path
    if not check_db_path():
        sys.exit(1)
    
    # Initialize the database
    if initialize_database():
        print("Database initialization completed successfully.")
        sys.exit(0)
    else:
        print("Database initialization failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
