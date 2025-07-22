import psycopg2
import os
from typing import Optional, Tuple, Union

def get_db_connection():
    """Get PostgreSQL database connection"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable not set")
        
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def authenticate_user(username: str, password: str) -> Optional[Tuple]:
    """Authenticate user login"""
    try:
        conn = get_db_connection()
        if not conn:
            return None
            
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, user_type 
            FROM users 
            WHERE username = %s AND password = %s
        """, (username, password))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return user
        
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def register_user(username: str, password: str, email: str, phone: str, location: str, user_type: str) -> Tuple[bool, str]:
    """Register a new user"""
    try:
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed"
            
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Username already exists"
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Email already registered"
        
        # Insert new user
        cursor.execute("""
            INSERT INTO users (username, password, email, phone, location, user_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, password, email, phone, location, user_type))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, f"Account created successfully! Welcome {username}!"
        
    except Exception as e:
        print(f"Registration error: {e}")
        return False, f"Registration failed: {str(e)}"

def change_password(user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
    """Change user password"""
    try:
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed"
            
        cursor = conn.cursor()
        
        # Verify old password
        cursor.execute("SELECT id FROM users WHERE id = %s AND password = %s", (user_id, old_password))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Current password is incorrect"
        
        # Update password
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "Password changed successfully"
        
    except Exception as e:
        print(f"Password change error: {e}")
        return False, f"Failed to change password: {str(e)}"

def get_user_profile(user_id: int) -> Optional[Tuple]:
    """Get user profile information"""
    try:
        conn = get_db_connection()
        if not conn:
            return None
            
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, phone, location, user_type, created_at
            FROM users 
            WHERE id = %s
        """, (user_id,))
        
        profile = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return profile
        
    except Exception as e:
        print(f"Profile fetch error: {e}")
        return None

def update_user_profile(user_id: int, email: str, phone: str, location: str) -> Tuple[bool, str]:
    """Update user profile information"""
    try:
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed"
            
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users 
            SET email = %s, phone = %s, location = %s
            WHERE id = %s
        """, (email, phone, location, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "Profile updated successfully"
        
    except Exception as e:
        print(f"Profile update error: {e}")
        return False, f"Failed to update profile: {str(e)}"