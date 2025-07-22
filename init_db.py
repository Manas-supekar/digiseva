import sqlite3
import os
from db.schema import create_tables

def initialize_database():
    """Initialize the database with tables and sample data"""
    # Create database directory if it doesn't exist
    os.makedirs('db', exist_ok=True)
    
    # Create database and tables
    create_tables()
    
    # Insert sample services
    conn = sqlite3.connect('db/services.db')
    cursor = conn.cursor()
    
    # Insert default services
    services = [
        ("House Cleaning", "Professional house cleaning service", 50.0),
        ("Plumbing", "Plumbing repairs and installations", 75.0),
        ("Electrical Work", "Electrical repairs and installations", 80.0),
        ("Gardening", "Garden maintenance and landscaping", 40.0),
        ("AC Repair", "Air conditioning repair and maintenance", 90.0),
        ("Painting", "Interior and exterior painting services", 60.0),
        ("Carpentry", "Furniture repair and custom woodwork", 70.0),
        ("Appliance Repair", "Repair of home appliances", 65.0)
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO services (name, description, base_price) 
        VALUES (?, ?, ?)
    """, services)
    
    # Create admin user
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, email, phone, location, user_type) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("admin", "admin123", "admin@homeservices.com", "000-000-0000", "HQ", "admin"))
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
