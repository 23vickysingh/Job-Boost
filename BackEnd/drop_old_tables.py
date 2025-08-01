from database import engine
from sqlalchemy import text

print("Dropping old unused tables...")

with engine.connect() as conn:
    # Start a transaction
    trans = conn.begin()
    
    try:
        # Drop the old tables
        conn.execute(text('DROP TABLE IF EXISTS user_information CASCADE'))
        print("✓ Dropped user_information table")
        
        conn.execute(text('DROP TABLE IF EXISTS user_profiles CASCADE'))
        print("✓ Dropped user_profiles table")
        
        # Commit the changes
        trans.commit()
        print("✓ All changes committed successfully")
        
        # Verify tables are gone
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        remaining_tables = [row[0] for row in result]
        print(f"Remaining tables: {remaining_tables}")
        
    except Exception as e:
        trans.rollback()
        print(f"Error: {e}")
        print("Transaction rolled back")
