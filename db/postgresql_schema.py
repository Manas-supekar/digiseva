import psycopg2
import os
from typing import Optional

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

def create_tables():
    """Create all necessary database tables in PostgreSQL"""
    
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return False
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                location VARCHAR(255) NOT NULL,
                user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('customer', 'professional', 'admin')),
                password VARCHAR(255) NOT NULL,
                rating DECIMAL(3,2) DEFAULT 0.0,
                experience_years INTEGER DEFAULT 0,
                availability VARCHAR(20) DEFAULT 'available',
                full_name VARCHAR(255),
                bio TEXT,
                specializations TEXT,
                certifications TEXT,
                work_history TEXT,
                portfolio_links TEXT,
                hourly_rate DECIMAL(8,2),
                service_areas TEXT,
                languages_spoken TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Services table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                base_price DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Professional services (junction table)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS professional_services (
                id SERIAL PRIMARY KEY,
                professional_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                custom_price DECIMAL(10,2),
                available BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (professional_id) REFERENCES users (id),
                FOREIGN KEY (service_id) REFERENCES services (id),
                UNIQUE(professional_id, service_id)
            )
        """)
        
        # Bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                professional_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined', 'completed', 'cancelled')),
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                scheduled_date VARCHAR(50),
                notes TEXT,
                price DECIMAL(10,2),
                FOREIGN KEY (customer_id) REFERENCES users (id),
                FOREIGN KEY (professional_id) REFERENCES users (id),
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        """)
        
        # Reviews table (for future enhancement)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                booking_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                professional_id INTEGER NOT NULL,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (booking_id) REFERENCES bookings (id),
                FOREIGN KEY (customer_id) REFERENCES users (id),
                FOREIGN KEY (professional_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("PostgreSQL database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        if conn:
            conn.rollback()
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()
        return False

if __name__ == "__main__":
    create_tables()