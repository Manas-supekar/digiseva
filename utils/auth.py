import sqlite3
from typing import Optional, Tuple, Union

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect('db/services.db')

def authenticate_user(username: str, password: str) -> Optional[Tuple]:
    """Authenticate user login"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, user_type 
            FROM users 
            WHERE username = ? AND password = ?
        """, (username, password))
        
        user = cursor.fetchone()
        conn.close()
        
        return user
        
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def register_user(username: str, password: str, email: str, phone: str, location: str, user_type: str) -> Tuple[bool, str]:
    """Register a new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, "Username already exists"
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False, "Email already registered"
        
        # Insert new user
        cursor.execute("""
            INSERT INTO users (username, password, email, phone, location, user_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, password, email, phone, location, user_type))
        
        # If professional, we might want to add some default setup here
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return True, f"Account created successfully! Welcome {username}!"
        
    except Exception as e:
        print(f"Registration error: {e}")
        return False, f"Registration failed: {str(e)}"

def change_password(user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
    """Change user password"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify old password
        cursor.execute("SELECT id FROM users WHERE id = ? AND password = ?", (user_id, old_password))
        if not cursor.fetchone():
            conn.close()
            return False, "Current password is incorrect"
        
        # Update password
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
        
        conn.commit()
        conn.close()
        
        return True, "Password changed successfully"
        
    except Exception as e:
        print(f"Password change error: {e}")
        return False, f"Failed to change password: {str(e)}"

def get_user_profile(user_id: int) -> Optional[Tuple]:
    """Get user profile information"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, phone, location, user_type, created_at
            FROM users 
            WHERE id = ?
        """, (user_id,))
        
        profile = cursor.fetchone()
        conn.close()
        
        return profile
        
    except Exception as e:
        print(f"Profile fetch error: {e}")
        return None

def update_user_profile(user_id: int, email: str, phone: str, location: str) -> Tuple[bool, str]:
    """Update user profile information"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users 
            SET email = ?, phone = ?, location = ?
            WHERE id = ?
        """, (email, phone, location, user_id))
        
        conn.commit()
        conn.close()
        
        return True, "Profile updated successfully"
        
    except Exception as e:
        print(f"Profile update error: {e}")
        return False, f"Failed to update profile: {str(e)}"
