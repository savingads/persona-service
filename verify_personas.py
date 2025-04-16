#!/usr/bin/env python3
"""
Verify that default personas exist in the database.
"""
import os
import sys
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

# Get the absolute path to the database
db_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data',
    'persona_service.db'
)
db_uri = f"sqlite:///{db_path}"

def main():
    """Main verification function"""
    print("=" * 70)
    print("VERIFYING DEFAULT PERSONAS IN DATABASE")
    print("=" * 70)
    print(f"Database path: {db_path}")
    print(f"Database URI: {db_uri}")
    
    # Create a direct connection to the database
    try:
        engine = create_engine(db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Check persona count
        count_result = session.execute(text("SELECT COUNT(*) FROM personas"))
        count = count_result.scalar()
        print(f"\nTotal personas in database: {count}")
        
        if count > 0:
            # List all personas
            print("\nPersonas in database:")
            result = session.execute(text("SELECT id, name FROM personas"))
            for row in result:
                print(f"ID: {row[0]}, Name: {row[1]}")
            
            # Show full details of first persona
            print("\nDetailed view of first persona:")
            detailed = session.execute(text("""
                SELECT p.id, p.name, d.country, d.city, d.age, d.gender
                FROM personas p
                JOIN demographic_data d ON p.id = d.persona_id
                WHERE p.id = 1
            """))
            for row in detailed:
                print(f"ID: {row[0]}, Name: {row[1]}")
                print(f"Country: {row[2]}, City: {row[3]}")
                print(f"Age: {row[4]}, Gender: {row[5]}")
            
            # Check attribute categories
            print("\nAttribute categories for first persona:")
            attrs = session.execute(text("""
                SELECT category, data FROM persona_attributes 
                WHERE persona_id = 1
            """))
            for row in attrs:
                print(f"Category: {row[0]}")
                print(f"Data: {row[1]}")
                print("-" * 50)
        else:
            print("No personas found in database!")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\nVerification completed successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
