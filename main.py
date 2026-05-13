import streamlit as st
import os
from utils.postgresql_auth import authenticate_user, register_user, get_professional_profile, update_professional_profile
from utils.postgresql_db_ops import (
    get_all_services, get_professionals_by_service, 
    book_service, get_user_bookings, get_professional_requests,
    add_professional_service, get_all_users, get_all_professionals,
    accept_booking, decline_booking
)

# Initialize PostgreSQL database
@st.cache_resource
def initialize_database():
    """Initialize PostgreSQL database once"""
    import postgresql_init
    return postgresql_init.initialize_postgresql_database()

# Initialize database on first load
initialize_database()

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
        st.markdown(
            '<div style="text-align: center; padding: 20px;">'
            '<svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
            '<circle cx="50" cy="50" r="48" fill="#4A9B9B" stroke="#ffffff" stroke-width="4"/>'
            '<circle cx="50" cy="50" r="38" fill="#ffffff"/>'
            '<circle cx="50" cy="50" r="32" fill="#7FB069"/>'
            '<path d="M35 45 L50 32 L65 45 L65 55 L58 55 L58 50 L42 50 L42 55 L35 55 Z" fill="white" stroke="#4A9B9B" stroke-width="1"/>'
            '<circle cx="30" cy="42" r="4" fill="#2D5A3D"/>'
            '<circle cx="32" cy="38" r="3" fill="#2D5A3D"/>'
            '<circle cx="70" cy="42" r="4" fill="#2D5A3D"/>'
            '<circle cx="68" cy="38" r="3" fill="#2D5A3D"/>'
            '<circle cx="50" cy="65" r="3" fill="#A4D65E"/>'
            '<ellipse cx="50" cy="72" rx="4" ry="6" fill="#A4D65E"/>'
            '<circle cx="42" cy="68" r="2.5" fill="#4A9B9B"/>'
            '<ellipse cx="42" cy="74" rx="3" ry="5" fill="#4A9B9B"/>'
            '<circle cx="58" cy="68" r="2.5" fill="#4A9B9B"/>'
            '<ellipse cx="58" cy="74" rx="3" ry="5" fill="#4A9B9B"/>'
            '<circle cx="35" cy="70" r="2" fill="#ffffff"/>'
            '<ellipse cx="35" cy="76" rx="2.5" ry="4" fill="#ffffff"/>'
            '<circle cx="65" cy="70" r="2" fill="#ffffff"/>'
            '<ellipse cx="65" cy="76" rx="2.5" ry="4" fill="#ffffff"/>'
            '</svg>'
            '<div style="margin-top: 10px; font-weight: bold; color: #4A9B9B; font-size: 16px;">DigiSeva</div>'
            '</div>',
            unsafe_allow_html=True
        )
        
        # About DigiSeva section
        st.markdown("---")
        st.markdown("### About DigiSeva")
        st.markdown("""
        **DigiSeva** is your trusted digital platform connecting homeowners with verified service professionals.
        
        **Our Mission:**
        Making home services accessible, reliable, and affordable for everyone.
        
        **What We Offer:**
        - 🏠 House Cleaning
        - 🔧 Plumbing & Repairs  
        - ⚡ Electrical Services
        - 🌿 Gardening & Landscaping
        - ❄️ AC Repair & Maintenance
        - 🎨 Painting Services
        - 🪚 Carpentry & Furniture
        - 📱 Appliance Repairs
        - 👨‍🍳 Cooking Service
        
        **Why Choose DigiSeva:**
        - ⭐ Rated professionals with verified experience
        - 📍 Location-based service matching
        - 💰 Transparent pricing
        - 🛡️ Quality assurance
        """)
        st.markdown("---")

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
        
        # Basic Information
        st.markdown("**Basic Information**")
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_email = st.text_input("Email", key="reg_email")
        reg_phone = st.text_input("Phone", key="reg_phone")
        reg_location = st.text_input("Location", key="reg_location")
        reg_user_type = st.selectbox("Account Type", ["customer", "professional"])
        
        # Professional-specific fields
        professional_data = {}
        if reg_user_type == "professional":
            st.markdown("---")
            st.markdown("**Professional Information**")
            
            col1, col2 = st.columns(2)
            with col1:
                professional_data['full_name'] = st.text_input("Full Name", key="prof_full_name")
                professional_data['experience_years'] = st.number_input("Years of Experience", min_value=0, max_value=50, value=1, key="prof_exp")
                professional_data['hourly_rate'] = st.number_input("Hourly Rate ($)", min_value=10.0, max_value=500.0, value=25.0, step=5.0, key="prof_rate")
            
            with col2:
                professional_data['availability'] = st.selectbox("Availability Status", ["available", "busy", "unavailable"], key="prof_availability")
                professional_data['languages_spoken'] = st.text_input("Languages Spoken (comma-separated)", placeholder="English, Hindi, Spanish", key="prof_languages")
                professional_data['service_areas'] = st.text_input("Service Areas (comma-separated)", placeholder="Downtown, Suburbs, City Center", key="prof_areas")
            
            professional_data['bio'] = st.text_area("Professional Bio", placeholder="Tell customers about yourself and your expertise...", key="prof_bio")
            professional_data['specializations'] = st.text_area("Specializations & Skills", placeholder="List your key skills and specializations...", key="prof_skills")
            professional_data['work_history'] = st.text_area("Work History", placeholder="Previous employers, projects, or relevant experience...", key="prof_history")
            professional_data['certifications'] = st.text_area("Certifications & Licenses", placeholder="Professional certifications, licenses, or training...", key="prof_certs")
            professional_data['portfolio_links'] = st.text_area("Portfolio Links", placeholder="Website, social media, or portfolio URLs...", key="prof_portfolio")
        
        if st.button("Register", type="primary"):
            basic_fields = [reg_username, reg_password, reg_email, reg_phone, reg_location]
            
            # Validate basic fields
            if not all(basic_fields):
                st.error("Please fill in all basic information fields")
                return
            
            # Validate professional fields if professional account
            if reg_user_type == "professional":
                required_prof_fields = [professional_data.get('full_name'), professional_data.get('bio')]
                if not all(required_prof_fields):
                    st.error("Please fill in Full Name and Bio for professional accounts")
                    return
            
            success, message = register_user(
                reg_username, reg_password, reg_email, 
                reg_phone, reg_location, reg_user_type,
                professional_data if reg_user_type == "professional" else None
            )
            if success:
                st.success(message)
                st.info("Please login with your new account")
            else:
                st.error(message)

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
                            # Professional card layout
                            col1, col2, col3 = st.columns([2, 1, 1])
                            
                            with col1:
                                # Display full name if available, otherwise username
                                display_name = prof[8] if prof[8] else prof[1].title()
                                st.markdown(f"**{display_name}**")
                                st.markdown(f"📍 {prof[3]} | 📞 {prof[4]}")
                                
                                # Show bio if available
                                if prof[9]:  # bio
                                    st.markdown(f"*{prof[9][:100]}{'...' if len(prof[9]) > 100 else ''}*")
                                
                                # Show specializations
                                if prof[10]:  # specializations
                                    st.markdown(f"**Skills:** {prof[10][:80]}{'...' if len(prof[10]) > 80 else ''}")
                            
                            with col2:
                                rating_stars = "⭐" * int(prof[5]) + "☆" * (5 - int(prof[5]))
                                st.markdown(f"**Rating:** {prof[5]}/5.0")
                                st.markdown(f"{rating_stars}")
                                
                                # Show hourly rate if available
                                if prof[11]:  # hourly_rate
                                    st.markdown(f"**Rate:** ${prof[11]}/hr")
                            
                            with col3:
                                availability_color = "🟢" if prof[7] == "available" else "🔴"
                                st.markdown(f"**Experience:** {prof[6]} years")
                                st.markdown(f"**Status:** {availability_color} {prof[7].title()}")
                                
                                # Show languages if available
                                if prof[13]:  # languages_spoken
                                    st.markdown(f"**Languages:** {prof[13]}")
                            
                            # Show service areas if available
                            if prof[12]:  # service_areas
                                st.markdown(f"**Service Areas:** {prof[12]}")
                            
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
        page = st.selectbox("Navigation", ["Service Requests", "My Profile", "My Services", "Add Service"])
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
    
    elif page == "My Profile":
        st.subheader("Professional Profile")
        
        # Get current professional data
        profile_data = get_professional_profile(st.session_state.user_id)
        
        if profile_data:
            st.markdown("### Current Profile Information")
            
            # Display current profile in a nice format
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Full Name:** {profile_data.get('full_name', 'Not set')}")
                st.markdown(f"**Username:** {profile_data.get('username', '')}")
                st.markdown(f"**Email:** {profile_data.get('email', '')}")
                st.markdown(f"**Phone:** {profile_data.get('phone', '')}")
                st.markdown(f"**Location:** {profile_data.get('location', '')}")
            
            with col2:
                st.markdown(f"**Experience:** {profile_data.get('experience_years', 0)} years")
                st.markdown(f"**Rating:** {profile_data.get('rating', 0.0)}/5.0 ⭐")
                st.markdown(f"**Hourly Rate:** ${profile_data.get('hourly_rate', 0.0)}")
                st.markdown(f"**Availability:** {profile_data.get('availability', 'available').title()}")
                st.markdown(f"**Languages:** {profile_data.get('languages_spoken', 'Not specified')}")
            
            st.markdown(f"**Bio:** {profile_data.get('bio', 'No bio provided')}")
            st.markdown(f"**Specializations:** {profile_data.get('specializations', 'Not specified')}")
            st.markdown(f"**Service Areas:** {profile_data.get('service_areas', 'Not specified')}")
            
            if profile_data.get('work_history'):
                st.markdown("**Work History:**")
                st.text_area("", value=profile_data.get('work_history', ''), disabled=True, height=100, key="display_history")
            
            if profile_data.get('certifications'):
                st.markdown("**Certifications:**")
                st.text_area("", value=profile_data.get('certifications', ''), disabled=True, height=100, key="display_certs")
            
            if profile_data.get('portfolio_links'):
                st.markdown("**Portfolio Links:**")
                st.text_area("", value=profile_data.get('portfolio_links', ''), disabled=True, height=60, key="display_portfolio")
            
            st.markdown("---")
            
            # Profile editing form
            if st.button("Edit Profile"):
                st.session_state.edit_profile = True
            
            if st.session_state.get('edit_profile', False):
                st.markdown("### Edit Profile")
                
                with st.form("edit_profile_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_full_name = st.text_input("Full Name", value=profile_data.get('full_name', ''))
                        new_experience = st.number_input("Years of Experience", min_value=0, max_value=50, 
                                                       value=int(profile_data.get('experience_years', 1)))
                        new_hourly_rate = st.number_input("Hourly Rate ($)", min_value=10.0, max_value=500.0, 
                                                        value=float(profile_data.get('hourly_rate', 25.0)), step=5.0)
                    
                    with col2:
                        new_availability = st.selectbox("Availability Status", ["available", "busy", "unavailable"], 
                                                       index=["available", "busy", "unavailable"].index(profile_data.get('availability', 'available')))
                        new_languages = st.text_input("Languages Spoken", value=profile_data.get('languages_spoken', ''))
                        new_service_areas = st.text_input("Service Areas", value=profile_data.get('service_areas', ''))
                    
                    new_bio = st.text_area("Professional Bio", value=profile_data.get('bio', ''), height=100)
                    new_specializations = st.text_area("Specializations & Skills", value=profile_data.get('specializations', ''), height=100)
                    new_work_history = st.text_area("Work History", value=profile_data.get('work_history', ''), height=120)
                    new_certifications = st.text_area("Certifications", value=profile_data.get('certifications', ''), height=100)
                    new_portfolio_links = st.text_area("Portfolio Links", value=profile_data.get('portfolio_links', ''), height=80)
                    
                    submitted = st.form_submit_button("Update Profile")
                    
                    if submitted:
                        update_data = {
                            'full_name': new_full_name,
                            'bio': new_bio,
                            'specializations': new_specializations,
                            'certifications': new_certifications,
                            'work_history': new_work_history,
                            'portfolio_links': new_portfolio_links,
                            'hourly_rate': new_hourly_rate,
                            'service_areas': new_service_areas,
                            'languages_spoken': new_languages,
                            'experience_years': new_experience,
                            'availability': new_availability
                        }
                        
                        success, message = update_professional_profile(st.session_state.user_id, update_data)
                        if success:
                            st.success(message)
                            st.session_state.edit_profile = False
                            st.rerun()
                        else:
                            st.error(message)
                
                if st.button("Cancel"):
                    st.session_state.edit_profile = False
                    st.rerun()
        else:
            st.error("Could not load profile data")
    
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
