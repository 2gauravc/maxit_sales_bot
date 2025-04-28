import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "maxit_db",
    "user": "maxit_user",
    "password": "maxit_pass",
    "host": "localhost",
    "port": "5432"
}

class UserLookupService:
    def __init__(self, db_config=DB_CONFIG):
        self.db_config = db_config

    def get_user_role(self, user_id: str):
        """
        Fetch user information (name, email, role, base_location) given a user_id.
        Returns a dictionary or None if not found.
        """
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
            role = cursor.fetchone()
            print (role)
            cursor.close()
            conn.close()
            if role: 
                return role['role']
            return None
        except Exception as e:
            print(f"Error fetching user info: {e}")
            return None
