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
    """, ("admin", "admin123", "admin@digiseva.com", "000-000-0000", "HQ", "admin"))
    
    # Create dummy professionals with ratings, experience, and availability
    professionals = [
        ("rajesh_cleaner", "pass123", "rajesh@email.com", "9876543210", "Mumbai", "professional", 4.8, 5, "available"),
        ("priya_plumber", "pass123", "priya@email.com", "9876543211", "Delhi", "professional", 4.5, 8, "available"),
        ("amit_electrician", "pass123", "amit@email.com", "9876543212", "Bangalore", "professional", 4.9, 12, "available"),
        ("sunita_gardener", "pass123", "sunita@email.com", "9876543213", "Pune", "professional", 4.3, 6, "busy"),
        ("kumar_ac_tech", "pass123", "kumar@email.com", "9876543214", "Chennai", "professional", 4.7, 10, "available"),
        ("meera_painter", "pass123", "meera@email.com", "9876543215", "Hyderabad", "professional", 4.6, 7, "available"),
        ("ravi_carpenter", "pass123", "ravi@email.com", "9876543216", "Kolkata", "professional", 4.4, 15, "available"),
        ("anjali_appliance", "pass123", "anjali@email.com", "9876543217", "Ahmedabad", "professional", 4.8, 9, "busy"),
        ("deepak_cleaner", "pass123", "deepak@email.com", "9876543218", "Mumbai", "professional", 4.2, 3, "available"),
        ("kavya_plumber", "pass123", "kavya@email.com", "9876543219", "Delhi", "professional", 4.6, 6, "available"),
        ("suresh_electrician", "pass123", "suresh@email.com", "9876543220", "Bangalore", "professional", 4.9, 14, "available"),
        ("neha_gardener", "pass123", "neha@email.com", "9876543221", "Pune", "professional", 4.1, 4, "available")
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO users (username, password, email, phone, location, user_type, rating, experience_years, availability) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, professionals)
    
    # Link professionals to services they offer
    professional_services = [
        # House Cleaning professionals
        (2, 1), (9, 1),  # rajesh_cleaner, deepak_cleaner
        # Plumbing professionals  
        (3, 2), (10, 2),  # priya_plumber, kavya_plumber
        # Electrical Work professionals
        (4, 3), (11, 3),  # amit_electrician, suresh_electrician
        # Gardening professionals
        (5, 4), (12, 4),  # sunita_gardener, neha_gardener
        # AC Repair professionals
        (6, 5),  # kumar_ac_tech
        # Painting professionals
        (7, 6),  # meera_painter
        # Carpentry professionals
        (8, 7),  # ravi_carpenter
        # Appliance Repair professionals
        (9, 8),  # anjali_appliance
        # Some professionals offer multiple services
        (2, 6), (3, 5), (4, 8), (7, 1)  # Multi-service professionals
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO professional_services (professional_id, service_id, available) 
        VALUES (?, ?, TRUE)
    """, professional_services)
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully with sample professionals!")

if __name__ == "__main__":
    initialize_database()
