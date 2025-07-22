import psycopg2
import os
from typing import List, Tuple, Optional, Union

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

def get_all_services() -> List[Tuple]:
    """Get all available services"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, base_price FROM services ORDER BY name")
        services = cursor.fetchall()
        cursor.close()
        conn.close()
        return services
    except Exception as e:
        print(f"Error fetching services: {e}")
        return []

def get_professionals_by_service(service_id: int) -> List[Tuple]:
    """Get all professionals offering a specific service"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT u.id, u.username, u.email, u.location, u.phone, u.rating, 
                   u.experience_years, u.availability, u.full_name, u.bio, u.specializations,
                   u.hourly_rate, u.service_areas, u.languages_spoken
            FROM users u
            JOIN professional_services ps ON u.id = ps.professional_id
            WHERE ps.service_id = %s AND u.user_type = 'professional' AND ps.available = TRUE
            ORDER BY u.rating DESC, u.experience_years DESC
        """, (service_id,))
        professionals = cursor.fetchall()
        cursor.close()
        conn.close()
        return professionals
    except Exception as e:
        print(f"Error fetching professionals: {e}")
        return []

def book_service(customer_id: int, professional_id: int, service_id: int) -> Tuple[bool, str]:
    """Book a service"""
    try:
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed"
            
        cursor = conn.cursor()
        
        # Get service price
        cursor.execute("SELECT base_price FROM services WHERE id = %s", (service_id,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return False, "Service not found"
        
        price = result[0]
        
        # Create booking
        cursor.execute("""
            INSERT INTO bookings (customer_id, professional_id, service_id, price, status)
            VALUES (%s, %s, %s, %s, 'pending')
        """, (customer_id, professional_id, service_id, price))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Service booked successfully! Waiting for professional confirmation."
        
    except Exception as e:
        print(f"Error booking service: {e}")
        return False, f"Error booking service: {str(e)}"

def get_user_bookings(user_id: int) -> List[Tuple]:
    """Get all bookings for a customer"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, s.name, u.username, b.status, b.booking_date, b.price
            FROM bookings b
            JOIN services s ON b.service_id = s.id
            JOIN users u ON b.professional_id = u.id
            WHERE b.customer_id = %s
            ORDER BY b.booking_date DESC
        """, (user_id,))
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
        return bookings
    except Exception as e:
        print(f"Error fetching user bookings: {e}")
        return []

def get_professional_requests(professional_id: int) -> List[Tuple]:
    """Get all service requests for a professional"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, s.name, u.username, b.status, b.booking_date, b.price
            FROM bookings b
            JOIN services s ON b.service_id = s.id
            JOIN users u ON b.customer_id = u.id
            WHERE b.professional_id = %s
            ORDER BY b.booking_date DESC
        """, (professional_id,))
        requests = cursor.fetchall()
        cursor.close()
        conn.close()
        return requests
    except Exception as e:
        print(f"Error fetching professional requests: {e}")
        return []

def accept_booking(booking_id: int) -> bool:
    """Accept a booking request"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE bookings SET status = 'accepted' WHERE id = %s
        """, (booking_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error accepting booking: {e}")
        return False

def decline_booking(booking_id: int) -> bool:
    """Decline a booking request"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE bookings SET status = 'declined' WHERE id = %s
        """, (booking_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error declining booking: {e}")
        return False

def add_professional_service(professional_id: int, service_id: int) -> Tuple[bool, str]:
    """Add a service to professional's offerings"""
    try:
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed"
            
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO professional_services (professional_id, service_id, available)
            VALUES (%s, %s, TRUE)
            ON CONFLICT (professional_id, service_id) 
            DO UPDATE SET available = TRUE
        """, (professional_id, service_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Service added successfully!"
    except Exception as e:
        print(f"Error adding professional service: {e}")
        return False, f"Error adding service: {str(e)}"

def get_all_users() -> List[Tuple]:
    """Get all users for admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, email, phone, location, user_type
            FROM users
            ORDER BY user_type, username
        """)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []

def get_all_professionals() -> List[Tuple]:
    """Get all professionals for admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, email, phone, location, rating, experience_years, availability
            FROM users
            WHERE user_type = 'professional'
            ORDER BY rating DESC, username
        """)
        professionals = cursor.fetchall()
        cursor.close()
        conn.close()
        return professionals
    except Exception as e:
        print(f"Error fetching professionals: {e}")
        return []