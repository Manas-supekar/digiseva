import sqlite3
import os

def create_tables():
    """Create all necessary database tables"""
    
    # Ensure db directory exists
    os.makedirs('db', exist_ok=True)
    
    conn = sqlite3.connect('db/services.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            user_type TEXT NOT NULL CHECK (user_type IN ('customer', 'professional', 'admin')),
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Services table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            base_price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Professional services (junction table)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professional_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professional_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            custom_price REAL,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            professional_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined', 'completed', 'cancelled')),
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scheduled_date TEXT,
            notes TEXT,
            price REAL,
            FOREIGN KEY (customer_id) REFERENCES users (id),
            FOREIGN KEY (professional_id) REFERENCES users (id),
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    """)
    
    # Reviews table (for future enhancement)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    conn.close()
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
