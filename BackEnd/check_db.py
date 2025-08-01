from database import engine
from sqlalchemy import text

# Check what columns exist in user_profile table
with engine.connect() as conn:
    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'user_profile' ORDER BY ordinal_position"))
    print('user_profile columns:')
    for row in result:
        print(f'  {row[0]}: {row[1]}')
    
    # Check if there's any data in the old tables
    result = conn.execute(text('SELECT COUNT(*) FROM user_information'))
    print(f'user_information records: {result.scalar()}')
    
    result = conn.execute(text('SELECT COUNT(*) FROM user_profiles'))
    print(f'user_profiles records: {result.scalar()}')
    
    result = conn.execute(text('SELECT COUNT(*) FROM user_profile'))
    print(f'user_profile records: {result.scalar()}')

    # Check if there's any job preferences data in user_profile
    result = conn.execute(text("SELECT id, user_id, query, location, mode_of_job, work_experience FROM user_profile WHERE query IS NOT NULL"))
    print('\nJob preferences data in user_profile:')
    for row in result:
        print(f'  User {row[1]}: {row[2]} in {row[3]}, {row[4]}, {row[5]}')
