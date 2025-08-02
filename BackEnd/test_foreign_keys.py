from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Check foreign key constraints
    result = conn.execute(text("""
        SELECT 
            tc.constraint_name, 
            tc.table_name, 
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name 
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='user_profile'
    """))
    
    print("Foreign key constraints for user_profile table:")
    for row in result:
        print(f"  {row[0]}: {row[1]}.{row[2]} -> {row[3]}.{row[4]}")
    
    # Test the relationship
    print("\nTesting foreign key relationship:")
    result = conn.execute(text("""
        SELECT u.id as user_id, u.user_id as email, 
               p.id as profile_id, p.query, p.location, p.resume_location
        FROM users u 
        LEFT JOIN user_profile p ON u.id = p.user_id
        ORDER BY u.id
    """))
    
    for row in result:
        if row[2]:
            print(f"  User {row[0]} ({row[1]}) -> Profile {row[2]}: {row[3]} in {row[4]}, Resume: {row[5] or 'None'}")
        else:
            print(f"  User {row[0]} ({row[1]}) -> No profile")
