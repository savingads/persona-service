#!/usr/bin/env python3
"""
Test the database initialization and default persona creation.
"""
import os
import sys
import time
import shutil
import traceback
from sqlalchemy import text
from app.models import init_db as db_init

# Add the current directory to the path so we can import init_db
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import init_db

def main():
    """Main test function"""
    print("=" * 70)
    print("STARTING DATABASE INITIALIZATION TEST")
    print("=" * 70)
    
    # Setup paths
    backup_path = './data/persona_service.db.backup'
    db_path = './data/persona_service.db'
    
    # Create backup of current database and test initialization
    try:
        # Backup existing database
        if os.path.exists(db_path):
            print(f"Creating backup of existing database to {backup_path}")
            shutil.copy2(db_path, backup_path)
            os.remove(db_path)
            print("Database file removed for testing.")
        
        # Run the initialization process
        print("\nRunning database initialization...")
        try:
            init_db.main()
        except Exception as e:
            print(f"ERROR during database initialization: {str(e)}")
            traceback.print_exc()
    except Exception as e:
        print(f"ERROR setting up test: {str(e)}")
        traceback.print_exc()
        
    # Give SQLite a moment to finalize transactions
    print("\nWaiting for database to be ready...")
    time.sleep(1)  # Short pause
        
    # Verify the results
    try:
        # Verify personas were created
        print("\nVerifying personas were created:")
        
        # Force a new session to ensure we're reading the latest data
        session = db_init()
        
        # Run the query and ensure we fetchall() to get all results
        print("Running verification query...")
        result = session.execute(text('SELECT id, name FROM personas'))
        rows = result.fetchall()
        
        # Display the results
        if not rows:
            print("WARNING: No personas found in database!")
        else:
            print(f"Found {len(rows)} personas in database:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}")
    except Exception as e:
        print(f"ERROR checking personas: {str(e)}")
        traceback.print_exc()
    
    # Restore original database
    try:
        if os.path.exists(backup_path):
            print("\nRestoring original database.")
            if os.path.exists(db_path):
                os.remove(db_path)
            shutil.copy2(backup_path, db_path)
            os.remove(backup_path)
            print("Original database restored.")
    except Exception as e:
        print(f"Error restoring database: {str(e)}")
    
    print("Test completed.")

if __name__ == "__main__":
    main()
