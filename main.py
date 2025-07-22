import streamlit as st
import sqlite3
import os
from utils.auth import authenticate_user, register_user
from utils.db_ops import (
    get_all_services, get_professionals_by_service, 
    book_service, get_user_bookings, get_professional_requests,
    add_professional_service, get_all_users, get_all_professionals,
    accept_booking, decline_booking
)

# Initialize database
if not os.path.exists('db/services.db'):
    import init_db
    init_db.initialize_database()

# Set page config
st.set_page_config(
    page_title="DigiSeva",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None

def show_logo():
    """Display logo in sidebar"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Outer teal circle -->
                <circle cx="50" cy="50" r="48" fill="#4A9B9B" stroke="#ffffff" stroke-width="4"/>
                
                <!-- Inner white circle -->
                <circle cx="50" cy="50" r="38" fill="#ffffff"/>
                
                <!-- Green background for inner content -->
                <circle cx="50" cy="50" r="32" fill="#7FB069"/>
                
                <!-- House outline -->
                <path d="M35 45 L50 32 L65 45 L65 55 L58 55 L58 50 L42 50 L42 55 L35 55 Z" fill="white" stroke="#4A9B9B" stroke-width="1"/>
                
                <!-- Trees -->
                <circle cx="30" cy="42" r="4" fill="#2D5A3D"/>
                <circle cx="32" cy="38" r="3" fill="#2D5A3D"/>
                <circle cx="70" cy="42" r="4" fill="#2D5A3D"/>
                <circle cx="68" cy="38" r="3" fill="#2D5A3D"/>
                
                <!-- People figures -->
                <!-- Center person (larger) -->
                <circle cx="50" cy="65" r="3" fill="#A4D65E"/>
                <ellipse cx="50" cy="72" rx="4" ry="6" fill="#A4D65E"/>
                
                <!-- Left person -->
                <circle cx="42" cy="68" r="2.5" fill="#4A9B9B"/>
                <ellipse cx="42" cy="74" rx="3" ry="5" fill="#4A9B9B"/>
                
                <!-- Right person -->
                <circle cx="58" cy="68" r="2.5" fill="#4A9B9B"/>
                <ellipse cx="58" cy="74" rx="3" ry="5" fill="#4A9B9B"/>
                
                <!-- Far left person -->
                <circle cx="35" cy="70" r="2" fill="#ffffff"/>
                <ellipse cx="35" cy="76" rx="2.5" ry="4" fill="#ffffff"/>
                
                <!-- Far right person -->
                <circle cx="65" cy="70" r="2" fill="#ffffff"/>
                <ellipse cx="65" cy="76" rx="2.5" ry="4" fill="#ffffff"/>
            </svg>
            <div style="margin-top: 10px; font-weight: bold; color: #4A9B9B; font-size: 16px;">DigiSeva</div>
        </div>
        """, unsafe_allow_html=True)

def login_page():
    """Login and registration page"""
    show_logo()
    
    st.title("🏠 DigiSeva")
    st.markdown("### Connect with trusted professionals for all your home service needs")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary"):
            if username and password:
                user_data = authenticate_user(username, password)
                if user_data:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user_data[0]
                    st.session_state.username = user_data[1]
                    st.session_state.user_type = user_data[3]
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("Create New Account")
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_email = st.text_input("Email", key="reg_email")
        reg_phone = st.text_input("Phone", key="reg_phone")
        reg_location = st.text_input("Location", key="reg_location")
        reg_user_type = st.selectbox("Account Type", ["customer", "professional"])
        
        if st.button("Register", type="primary"):
            if all([reg_username, reg_password, reg_email, reg_phone, reg_location]):
                success, message = register_user(
                    reg_username, reg_password, reg_email, 
                    reg_phone, reg_location, reg_user_type
                )
                if success:
                    st.success(message)
                    st.info("Please login with your new account")
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")

def customer_dashboard():
    """Customer dashboard with service booking functionality"""
    show_logo()
    
    st.title(f"Welcome, {st.session_state.username}! 👋")
    st.markdown("### Book Home Services")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("---")
        page = st.selectbox("Navigation", ["Browse Services", "My Bookings"])
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    if page == "Browse Services":
        st.subheader("Available Services")
        
        services = get_all_services()
        if services:
            service_names = [service[1] for service in services]
            selected_service = st.selectbox("Select a Service", service_names)
            
            if selected_service:
                # Get service details
                service_id = next(service[0] for service in services if service[1] == selected_service)
                service_details = next(service for service in services if service[0] == service_id)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {service_details[2]}")
                    st.markdown(f"**Base Price:** ${service_details[3]}")
                
                with col2:
                    if st.button("Book This Service", type="primary"):
                        # Get available professionals
                        professionals = get_professionals_by_service(service_id)
                        if professionals:
                            # Book with first available professional (can be enhanced)
                            professional_id = professionals[0][0]
                            success, message = book_service(st.session_state.user_id, professional_id, service_id)
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
                        else:
                            st.error("No professionals available for this service")
                
                # Show available professionals
                st.subheader("Available Professionals")
                professionals = get_professionals_by_service(service_id)
                if professionals:
                    for prof in professionals:
                        with st.container():
                            # Create columns for better layout
                            col1, col2, col3 = st.columns([2, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{prof[1].title()}**")
                                st.markdown(f"📍 {prof[3]} | 📞 {prof[4]}")
                            
                            with col2:
                                rating_stars = "⭐" * int(prof[5]) + "☆" * (5 - int(prof[5]))
                                st.markdown(f"**Rating:** {prof[5]}/5.0")
                                st.markdown(f"{rating_stars}")
                            
                            with col3:
                                availability_color = "🟢" if prof[7] == "available" else "🔴"
                                st.markdown(f"**Experience:** {prof[6]} years")
                                st.markdown(f"**Status:** {availability_color} {prof[7].title()}")
                            
                            st.markdown("---")
                else:
                    st.info("No professionals currently available for this service")
        else:
            st.info("No services available at the moment")
    
    elif page == "My Bookings":
        st.subheader("Your Service Bookings")
        
        bookings = get_user_bookings(st.session_state.user_id)
        if bookings:
            for booking in bookings:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**Service:** {booking[1]}")
                        st.write(f"**Professional:** {booking[2]}")
                    with col2:
                        st.write(f"**Status:** {booking[3]}")
                    with col3:
                        st.write(f"**Date:** {booking[4]}")
                    st.markdown("---")
        else:
            st.info("You haven't made any bookings yet")

def professional_dashboard():
    """Professional dashboard for managing services and requests"""
    show_logo()
    
    st.title(f"Professional Dashboard - {st.session_state.username} 👨‍🔧")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("---")
        page = st.selectbox("Navigation", ["Service Requests", "My Services", "Add Service"])
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    if page == "Service Requests":
        st.subheader("Incoming Service Requests")
        
        requests = get_professional_requests(st.session_state.user_id)
        if requests:
            for request in requests:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**Service:** {request[1]}")
                        st.write(f"**Customer:** {request[2]}")
                        st.write(f"**Status:** {request[3]}")
                    with col2:
                        if request[3] == 'pending':
                            if st.button(f"Accept", key=f"accept_{request[0]}"):
                                accept_booking(request[0])
                                st.success("Booking accepted!")
                                st.rerun()
                    with col3:
                        if request[3] == 'pending':
                            if st.button(f"Decline", key=f"decline_{request[0]}"):
                                decline_booking(request[0])
                                st.info("Booking declined")
                                st.rerun()
                    st.markdown("---")
        else:
            st.info("No service requests at the moment")
    
    elif page == "My Services":
        st.subheader("Services You Offer")
        st.info("Service management feature coming soon")
    
    elif page == "Add Service":
        st.subheader("Add New Service")
        
        # Get available services to add
        all_services = get_all_services()
        if all_services:
            service_names = [service[1] for service in all_services]
            selected_service = st.selectbox("Select Service to Offer", service_names)
            
            if st.button("Add Service"):
                service_id = next(service[0] for service in all_services if service[1] == selected_service)
                success, message = add_professional_service(st.session_state.user_id, service_id)
                if success:
                    st.success(message)
                else:
                    st.error(message)

def admin_dashboard():
    """Admin dashboard for system management"""
    show_logo()
    
    st.title(f"Admin Dashboard - {st.session_state.username} 👑")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("---")
        page = st.selectbox("Navigation", ["Users Overview", "Professionals", "System Stats"])
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    if page == "Users Overview":
        st.subheader("All Users")
        
        users = get_all_users()
        if users:
            col1, col2, col3, col4 = st.columns(4)
            col1.write("**Username**")
            col2.write("**Email**")
            col3.write("**Location**")
            col4.write("**Type**")
            
            for user in users:
                col1, col2, col3, col4 = st.columns(4)
                col1.write(user[1])
                col2.write(user[2])
                col3.write(user[4])
                col4.write(user[5])
        else:
            st.info("No users found")
    
    elif page == "Professionals":
        st.subheader("All Professionals")
        
        professionals = get_all_professionals()
        if professionals:
            # Create header columns
            col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1, 1, 1])
            col1.write("**Name & Contact**")
            col2.write("**Location**")
            col3.write("**Rating**")
            col4.write("**Experience**")
            col5.write("**Status**")
            st.markdown("---")
            
            for prof in professionals:
                col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1, 1, 1])
                
                with col1:
                    st.write(f"**{prof[1].title()}**")
                    st.write(f"📧 {prof[2]}")
                    st.write(f"📞 {prof[3]}")
                
                with col2:
                    st.write(f"📍 {prof[4]}")
                
                with col3:
                    rating_stars = "⭐" * int(prof[5]) + "☆" * (5 - int(prof[5]))
                    st.write(f"{prof[5]}/5.0")
                    st.write(rating_stars)
                
                with col4:
                    st.write(f"{prof[6]} years")
                
                with col5:
                    availability_color = "🟢" if prof[7] == "available" else "🔴"
                    st.write(f"{availability_color} {prof[7].title()}")
                
                st.markdown("---")
        else:
            st.info("No professionals registered")
    
    elif page == "System Stats":
        st.subheader("System Statistics")
        
        # Basic stats
        users = get_all_users()
        professionals = get_all_professionals()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", len(users) if users else 0)
        
        with col2:
            st.metric("Total Professionals", len(professionals) if professionals else 0)
        
        with col3:
            customer_count = len([u for u in users if u[5] == 'customer']) if users else 0
            st.metric("Customers", customer_count)

def main():
    """Main application logic"""
    if not st.session_state.authenticated:
        login_page()
    else:
        if st.session_state.user_type == 'customer':
            customer_dashboard()
        elif st.session_state.user_type == 'professional':
            professional_dashboard()
        elif st.session_state.user_type == 'admin':
            admin_dashboard()
        else:
            st.error("Invalid user type")

if __name__ == "__main__":
    main()
