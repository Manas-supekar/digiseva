# DigiSeva - Digital Services Platform

## Overview

DigiSeva is a Streamlit-based web application for connecting customers with home service professionals. The platform allows customers to book services, professionals to offer their skills, and administrators to manage the entire system. The application uses SQLite for data storage and provides role-based access control with three distinct user types.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and deployment
- **UI Strategy**: Single-page application with role-based dashboards
- **State Management**: Streamlit session state for user authentication and navigation
- **Styling**: Custom CSS embedded within Streamlit components for branding

### Backend Architecture
- **Language**: Python 3.x
- **Database**: SQLite for local development and simple deployment
- **Authentication**: Simple username/password authentication stored in database
- **Data Access**: Direct SQL queries through sqlite3 module
- **Business Logic**: Separated into utility modules for authentication and database operations

## Key Components

### Database Schema (`db/schema.py`)
- **Users Table**: Stores user credentials and profile information with role-based access (customer, professional, admin)
- **Services Table**: Catalog of available home services with base pricing
- **Professional Services Table**: Junction table linking professionals to services they offer
- **Bookings Table**: Tracks service requests and their status

### Authentication System (`utils/auth.py`)
- Simple credential-based authentication
- User registration with duplicate checking
- Role-based access control (customer, professional, admin)
- Session management through Streamlit state

### Database Operations (`utils/db_ops.py`)
- Service catalog management
- Professional-service matching
- Booking system with status tracking
- User management functions

### Application Entry Point (`main.py`)
- Streamlit application configuration
- Session state initialization
- Database initialization on first run
- Role-based UI routing

## Data Flow

1. **User Registration/Login**: Users authenticate through the login page, establishing session state
2. **Service Discovery**: Customers browse available services and view professionals
3. **Booking Process**: Customers select professionals and create service requests
4. **Professional Response**: Professionals view and respond to booking requests
5. **Admin Oversight**: Administrators monitor users, professionals, and system activity

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework
- **SQLite3**: Built-in Python database interface (no external database required)

### Deployment Considerations
- No external API integrations currently implemented
- Self-contained application with embedded database
- Future considerations may include payment processing and notification services

## Deployment Strategy

### Current Setup
- **Database**: SQLite file-based storage (`db/services.db`)
- **Initialization**: Automatic database creation with sample data
- **Environment**: Designed for local development and simple cloud deployment

### Database Initialization
- Automatic table creation on first run
- Pre-populated with sample services and admin user
- Self-contained setup process through `init_db.py`

### Scalability Considerations
- Current SQLite implementation suitable for small to medium user bases
- Architecture allows for future migration to PostgreSQL or other databases
- Modular design supports adding external services (payment, notifications, etc.)

### Security Notes
- Basic password storage (consider hashing for production)
- No HTTPS enforcement (should be added for production)
- Simple authentication system (consider OAuth for enhanced security)

This architecture prioritizes simplicity and rapid development while maintaining a clear separation of concerns that allows for future enhancements and scaling.