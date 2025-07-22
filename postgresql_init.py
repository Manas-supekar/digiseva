import os
from db.postgresql_schema import create_tables, get_db_connection

def initialize_postgresql_database():
    """Initialize PostgreSQL database with tables and sample data"""
    
    print("Creating PostgreSQL tables...")
    if not create_tables():
        print("Failed to create tables")
        return False
    
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database for data initialization")
        return False
        
    try:
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
            INSERT INTO services (name, description, base_price) 
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, services)
        
        # Create admin user
        cursor.execute("""
            INSERT INTO users (username, password, email, phone, location, user_type) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
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
            INSERT INTO users (username, password, email, phone, location, user_type, rating, experience_years, availability) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
        """, professionals)
        
        # Link professionals to services they offer
        # First, get the user IDs for professionals
        cursor.execute("SELECT id, username FROM users WHERE user_type = 'professional' ORDER BY id")
        prof_users = cursor.fetchall()
        
        cursor.execute("SELECT id, name FROM services ORDER BY id")
        services_data = cursor.fetchall()
        
        if prof_users and services_data:
            # Create mapping of service names to IDs
            service_map = {name: sid for sid, name in services_data}
            user_map = {username: uid for uid, username in prof_users}
            
            # Link professionals to services
            professional_services = []
            
            # House Cleaning professionals
            if 'rajesh_cleaner' in user_map and 'House Cleaning' in service_map:
                professional_services.append((user_map['rajesh_cleaner'], service_map['House Cleaning']))
            if 'deepak_cleaner' in user_map and 'House Cleaning' in service_map:
                professional_services.append((user_map['deepak_cleaner'], service_map['House Cleaning']))
            
            # Plumbing professionals  
            if 'priya_plumber' in user_map and 'Plumbing' in service_map:
                professional_services.append((user_map['priya_plumber'], service_map['Plumbing']))
            if 'kavya_plumber' in user_map and 'Plumbing' in service_map:
                professional_services.append((user_map['kavya_plumber'], service_map['Plumbing']))
            
            # Electrical Work professionals
            if 'amit_electrician' in user_map and 'Electrical Work' in service_map:
                professional_services.append((user_map['amit_electrician'], service_map['Electrical Work']))
            if 'suresh_electrician' in user_map and 'Electrical Work' in service_map:
                professional_services.append((user_map['suresh_electrician'], service_map['Electrical Work']))
            
            # Gardening professionals
            if 'sunita_gardener' in user_map and 'Gardening' in service_map:
                professional_services.append((user_map['sunita_gardener'], service_map['Gardening']))
            if 'neha_gardener' in user_map and 'Gardening' in service_map:
                professional_services.append((user_map['neha_gardener'], service_map['Gardening']))
            
            # AC Repair professionals
            if 'kumar_ac_tech' in user_map and 'AC Repair' in service_map:
                professional_services.append((user_map['kumar_ac_tech'], service_map['AC Repair']))
            
            # Painting professionals
            if 'meera_painter' in user_map and 'Painting' in service_map:
                professional_services.append((user_map['meera_painter'], service_map['Painting']))
            
            # Carpentry professionals
            if 'ravi_carpenter' in user_map and 'Carpentry' in service_map:
                professional_services.append((user_map['ravi_carpenter'], service_map['Carpentry']))
            
            # Appliance Repair professionals
            if 'anjali_appliance' in user_map and 'Appliance Repair' in service_map:
                professional_services.append((user_map['anjali_appliance'], service_map['Appliance Repair']))
            
            # Multi-service professionals
            if 'rajesh_cleaner' in user_map and 'Painting' in service_map:
                professional_services.append((user_map['rajesh_cleaner'], service_map['Painting']))
            if 'priya_plumber' in user_map and 'AC Repair' in service_map:
                professional_services.append((user_map['priya_plumber'], service_map['AC Repair']))
            if 'amit_electrician' in user_map and 'Appliance Repair' in service_map:
                professional_services.append((user_map['amit_electrician'], service_map['Appliance Repair']))
            if 'meera_painter' in user_map and 'House Cleaning' in service_map:
                professional_services.append((user_map['meera_painter'], service_map['House Cleaning']))
            
            if professional_services:
                cursor.executemany("""
                    INSERT INTO professional_services (professional_id, service_id, available) 
                    VALUES (%s, %s, TRUE)
                    ON CONFLICT (professional_id, service_id) DO NOTHING
                """, professional_services)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("PostgreSQL database initialized successfully with sample professionals!")
        return True
        
    except Exception as e:
        print(f"Error initializing database data: {e}")
        if conn:
            conn.rollback()
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()
        return False

if __name__ == "__main__":
    initialize_postgresql_database()