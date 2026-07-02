"""
SMART HOSPITAL MANAGEMENT SYSTEM - FULLY INTEGRATED
Frontend + Backend Complete Integration
Team Avengers - Phase 3 (100%)

Run: streamlit run hospital_integrated.py
"""

import streamlit as st
from datetime import date, datetime, time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import the database handler
import sys
sys.path.append('.')
from Hospital_Management.database import HospitalDatabase

# Page Configuration
st.set_page_config(
    page_title="Smart Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (your teal theme)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #17252A 0%, #2B7A78 100%) !important;
        color: #FEFFFF;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-left: 2.0rem;
        padding-right: 2.0rem;
    }
    h1, h2, h3 {
        color: #FEFFFF !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px;
        font-weight: 800;
        color: #FEFFFF !important;
    }
    div[data-testid="stMetricDelta"] {
        font-weight: 700;
        color: #DEF2F1 !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3AAFA9 0%, #2B7A78 100%) !important;
        color: #17252A !important;
        border: none;
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 700;
        box-shadow: 0 6px 12px rgba(43,122,120,0.18);
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 22px rgba(43,122,120,0.28);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #17252A 0%, #2B7A78 100%) !important;
        color: #FEFFFF;
        border-right: 1px solid rgba(255,255,255,0.04);
    }
    .stAlert {
        color: #17252A !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Database Connection
@st.cache_resource
def init_database():
    """Initialize database connection (cached)"""
    db = HospitalDatabase(
        host='localhost',
        database='smart_hospital',
        user='root',
        password='YOUR_MYSQL_PASSWORD'  
    )
    if db.connect():
        return db
    else:
        st.error("❌ Failed to connect to database! Please check your credentials.")
        return None

# Initialize database
db = init_database()

# Sidebar Navigation
st.sidebar.title("🏥 Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Select Module:",
    ["🏠 Dashboard", "👤 Patient Registration", "👨‍⚕ Doctor Schedule",
     "🛏 Bed Management", "💊 Pharmacy Inventory", "💰 Billing System",
     "🚨 Emergency Records", "📊 Analytics & Reports"]
)

# ===== DASHBOARD PAGE =====
if page == "🏠 Dashboard":
    st.title("🏥 Smart Hospital Management Dashboard")
    st.markdown("### Real-time Hospital Overview")
    
    if db:
        # Get real dashboard stats from database
        stats = db.get_dashboard_stats()
        
        # Top Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="👥 Total Patients", 
                     value=stats.get('total_patients', 0))
        with col2:
            st.metric(label="👨‍⚕ Doctors Available", 
                     value=stats.get('available_doctors', 0))
        with col3:
            occupied = stats.get('occupied_beds', 0)
            total = stats.get('total_beds', 1)
            occupancy = int((occupied / total) * 100)
            st.metric(label="🛏 Beds Occupied", 
                     value=f"{occupied}/{total}", 
                     delta=f"{occupancy}%")
        with col4:
            st.metric(label="🚨 Emergencies Today", 
                     value=stats.get('todays_emergencies', 0))
        
        st.markdown("---")
        
        # Charts Section
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Weekly Admissions")
            admissions_data = db.get_weekly_admissions()
            if admissions_data:
                df = pd.DataFrame(admissions_data)
                fig = px.bar(df, x='day_name', y='admission_count',
                           labels={'day_name': 'Day', 'admission_count': 'Admissions'},
                           color_discrete_sequence=['#3AAFA9'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#FEFFFF')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No admission data available for this week")
        
        with col2:
            st.subheader("🏥 Department-wise Patients")
            dept_data = db.get_department_wise_patients()
            if dept_data:
                df = pd.DataFrame(dept_data)
                fig = px.bar(df, x='dept_name', y='patient_count',
                           labels={'dept_name': 'Department', 'patient_count': 'Patients'},
                           color_discrete_sequence=['#2B7A78'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#FEFFFF')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No department data available")
        
        st.markdown("---")
        
        # Bed Occupancy Report
        st.subheader("🛏 Bed Occupancy by Department")
        occupancy_data = db.get_bed_occupancy_report()
        if occupancy_data:
            df = pd.DataFrame(occupancy_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Low Stock Medicines Alert
        st.subheader("⚠ Low Stock Medicines")
        low_stock = db.get_low_stock_medicines()
        if low_stock:
            df = pd.DataFrame(low_stock)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.success("✅ All medicines are adequately stocked!")
    else:
        st.error("Database connection failed. Please check your credentials.")

# ===== PATIENT REGISTRATION =====
elif page == "👤 Patient Registration":
    st.title("👤 Patient Registration System")
    st.markdown("### Register New Patient")
    
    with st.form("patient_registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            first_name = st.text_input("First Name *", placeholder="Enter first name")
            last_name = st.text_input("Last Name *", placeholder="Enter last name")
            dob = st.date_input("Date of Birth *", min_value=date(1920, 1, 1), max_value=date.today())
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            blood_group = st.selectbox("Blood Group *", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        
        with col2:
            st.subheader("Contact Information")
            phone = st.text_input("Phone Number *", placeholder="+91 XXXXX XXXXX")
            email = st.text_input("Email", placeholder="patient@example.com")
            address = st.text_area("Address *", placeholder="Enter full address")
            emergency_contact = st.text_input("Emergency Contact *", placeholder="+91 XXXXX XXXXX")
            emergency_name = st.text_input("Emergency Contact Name *", placeholder="Name")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            admission_type = st.selectbox("Admission Type *", ["OPD", "IPD", "Emergency"])
        
        # Submit button
        submitted = st.form_submit_button("✅ Register Patient", use_container_width=True)
        
        if submitted:
            if db and first_name and last_name and phone and address and emergency_contact and emergency_name:
                patient_id = db.register_patient(
                    first_name=first_name,
                    last_name=last_name,
                    dob=dob,
                    gender=gender,
                    blood_group=blood_group,
                    phone=phone,
                    email=email or None,
                    address=address,
                    emergency_contact_name=emergency_name,
                    emergency_contact_number=emergency_contact,
                    admission_type=admission_type
                )
                
                if patient_id:
                    st.success(f"✅ Patient registered successfully! Patient ID: {patient_id}")
                    st.balloons()
                else:
                    st.error("❌ Failed to register patient. Please try again.")
            else:
                st.error("❌ Please fill all required fields marked with *")
    
    # Show recent patients
    st.markdown("---")
    st.subheader("📋 Recently Registered Patients")
    if db:
        patients = db.get_all_patients()
        if patients:
            df = pd.DataFrame(patients)
            # Show only relevant columns
            display_cols = ['patient_id', 'first_name', 'last_name', 'gender', 
                          'blood_group', 'phone_number', 'admission_type', 'admission_date']
            if all(col in df.columns for col in display_cols):
                st.dataframe(df[display_cols].head(10), use_container_width=True, hide_index=True)
        else:
            st.info("No patients registered yet.")

# ===== DOCTOR SCHEDULE =====
elif page == "👨‍⚕ Doctor Schedule":
    st.title("👨‍⚕ Doctor Schedule Management")
    
    if db:
        # Get all doctors
        doctors = db.get_all_doctors()
        
        if doctors:
            st.subheader("📋 All Doctors")
            df = pd.DataFrame(doctors)
            
            # Status color coding
            def highlight_status(val):
                if val == 'Available':
                    return 'background-color: rgba(58,175,169,0.3)'
                elif val == 'On Leave':
                    return 'background-color: rgba(255,165,0,0.3)'
                return ''
            
            display_cols = ['doctor_id', 'first_name', 'last_name', 'specialization', 
                          'dept_name', 'phone_number', 'status']
            if all(col in df.columns for col in display_cols):
                styled_df = df[display_cols].style.map(
                    highlight_status, subset=['status'] if 'status' in df.columns else []
                )
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
        else:
            st.info("No doctors found in the system.")
        
        st.markdown("---")
        
        # Doctor Workload
        st.subheader("📊 Doctor Workload (Last 7 Days)")
        workload = db.get_doctor_workload()
        if workload:
            df = pd.DataFrame(workload)
            fig = px.bar(df, x='doctor_name', y='total_appointments',
                       color='dept_name',
                       labels={'doctor_name': 'Doctor', 'total_appointments': 'Appointments'},
                       title='Doctor Appointments')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FEFFFF')
            )
            st.plotly_chart(fig, use_container_width=True)

# ===== BED MANAGEMENT =====
elif page == "🛏 Bed Management":
    st.title("🛏 Bed Management System")
    
    if db:
        # Get bed occupancy stats
        occupancy = db.get_bed_occupancy_report()
        
        if occupancy:
            # Summary Cards
            total_beds = sum(int(item['total_beds']) for item in occupancy)
            occupied_beds = sum(int(item['occupied_beds']) for item in occupancy)
            available_beds = sum(int(item['available_beds']) for item in occupancy)

            overall_occupancy = int((occupied_beds / total_beds) * 100) if total_beds > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Beds", int(total_beds))
            with col2:
                st.metric("Occupied", int(occupied_beds), delta=f"{int(overall_occupancy)}%")
            with col3:
                st.metric("Available", int(available_beds))
            with col4:
                st.metric("Under Maintenance", "0")
            
            st.markdown("---")
            
            # Department-wise Bed Status
            st.subheader("🏥 Department-wise Bed Status")
            df = pd.DataFrame(occupancy)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Visualize occupancy
            fig = px.pie(
                df, 
                values='occupied_beds', 
                names='dept_name',
                title='Bed Occupancy Distribution',
                color_discrete_sequence=px.colors.sequential.Teal
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FEFFFF')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No bed data available.")
        
        st.markdown("---")
        
        # Available Beds
        st.subheader("🔍 Available Beds")
        ward_type = st.selectbox(
            "Filter by Ward Type", 
            ["All", "General", "ICU", "Private", "Emergency"]
        )
        
        if ward_type == "All":
            available_beds = db.get_available_beds()
        else:
            available_beds = db.get_available_beds(ward_type=ward_type)
        
        if available_beds:
            df = pd.DataFrame(available_beds)
            display_cols = ['bed_id', 'bed_number', 'ward_type', 'dept_name', 'bed_status']
            if all(col in df.columns for col in display_cols):
                st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
        else:
            st.warning(f"No available beds found for {ward_type}")


# ===== PHARMACY INVENTORY =====
elif page == "💊 Pharmacy Inventory":
    st.title("💊 Pharmacy Inventory Management")
    
    if db:
        # Get inventory data
        inventory = db.get_pharmacy_inventory()
        low_stock = db.get_low_stock_medicines()
        
        # Summary Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Medicines", len(inventory) if inventory else 0)
        with col2:
            st.metric("Low Stock Items", len(low_stock) if low_stock else 0, delta="⚠")
        with col3:
            out_of_stock = len([item for item in inventory if item.get('stock_quantity', 0) == 0])
            st.metric("Out of Stock", out_of_stock, delta="🔴" if out_of_stock > 0 else "✅")
        with col4:
            expiring = db.get_expiring_medicines(days=90)
            st.metric("Expiring Soon (90 days)", len(expiring) if expiring else 0)
        
        st.markdown("---")
        
        # Medicine Inventory Table
        st.subheader("📦 Medicine Inventory")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            search_med = st.text_input("🔍 Search Medicine", placeholder="Enter medicine name...")
        
        if inventory:
            df = pd.DataFrame(inventory)
            
            # Search filter
            if search_med:
                df = df[df['medicine_name'].str.contains(search_med, case=False, na=False)]
            
            # Color code stock status
            def color_stock_status(val):
                if val == 'Out of Stock':
                    return 'background-color: rgba(255,0,0,0.3)'
                elif val == 'Low Stock':
                    return 'background-color: rgba(255,165,0,0.3)'
                return 'background-color: rgba(0,255,0,0.2)'
            
            if 'stock_status' in df.columns:
                styled_df = df.style.map(color_stock_status, subset=['stock_status'])
                st.dataframe(styled_df, use_container_width=True, hide_index=True, height=400)
            else:
                st.dataframe(df, use_container_width=True, hide_index=True, height=400)
        else:
            st.info("No inventory data available.")
        
        st.markdown("---")
        
        # Low Stock Alert
        if low_stock:
            st.warning("⚠ **Low Stock Alert**")
            df_low = pd.DataFrame(low_stock)
            st.dataframe(df_low, use_container_width=True, hide_index=True)
        
        # Expiring Medicines
        if expiring:
            st.error("🔴 **Medicines Expiring Soon**")
            df_exp = pd.DataFrame(expiring)
            st.dataframe(df_exp, use_container_width=True, hide_index=True)

# ===== BILLING SYSTEM =====
elif page == "💰 Billing System":
    st.title("💰 Billing System")
    
    if db:
        # Search Patient
        st.subheader("🔍 Generate Bill for Patient")
        col1, col2 = st.columns(2)
        
        with col1:
            patient_id_input = st.text_input("Enter Patient ID", placeholder="e.g., 1, 2, 3...")
            
            if st.button("Search Patient"):
                if patient_id_input:
                    try:
                        patient_id = int(patient_id_input)
                        patient = db.search_patient_by_id(patient_id)
                        
                        if patient:
                            st.success(f"✅ Patient Found: {patient['first_name']} {patient['last_name']}")
                            st.session_state['current_patient'] = patient
                        else:
                            st.error("❌ Patient not found")
                    except ValueError:
                        st.error("❌ Please enter a valid Patient ID number")
        
        # If patient is found, show billing form
        if 'current_patient' in st.session_state:
            patient = st.session_state['current_patient']
            
            st.markdown("---")
            st.subheader(f"📋 Create Bill for: {patient['first_name']} {patient['last_name']}")
            
            with st.form("billing_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    total_amount = st.number_input("Total Amount (₹)", min_value=0.0, value=0.0, step=100.0)
                    insurance_claim = st.number_input("Insurance Claim (₹)", min_value=0.0, value=0.0, step=100.0)
                    discount = st.number_input("Discount (₹)", min_value=0.0, value=0.0, step=100.0)
                
                with col2:
                    tax = st.number_input("Tax (₹)", min_value=0.0, value=0.0, step=10.0)
                    payment_method = st.selectbox("Payment Method", ["Cash", "Card", "UPI", "Net Banking"])
                    
                    net_amount = total_amount - insurance_claim - discount + tax
                    st.metric("Net Amount", f"₹{net_amount:,.2f}")
                
                submitted = st.form_submit_button("💳 Generate Bill", use_container_width=True)
                
                if submitted:
                    if total_amount > 0:
                        bill_id = db.create_bill(
                            patient_id=patient['patient_id'],
                            total_amount=total_amount,
                            insurance_claim=insurance_claim,
                            discount=discount,
                            tax=tax,
                            payment_method=payment_method
                        )
                        
                        if bill_id:
                            st.success(f"✅ Bill generated successfully! Bill ID: {bill_id}")
                            st.balloons()
                        else:
                            st.error("❌ Failed to generate bill")
                    else:
                        st.error("❌ Total amount must be greater than 0")
        
        st.markdown("---")
        
        # Pending Bills
        st.subheader("📋 Pending Bills")
        pending_bills = db.get_pending_bills()
        if pending_bills:
            df = pd.DataFrame(pending_bills)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No pending bills!")

# ===== EMERGENCY RECORDS =====
elif page == "🚨 Emergency Records":
    st.title("🚨 Emergency Records Management")
    
    if db:
        # Get active emergencies
        emergencies = db.get_active_emergencies()
        
        # Quick Stats
        critical = len([e for e in emergencies if e.get('triage_level') == 'Critical'])
        urgent = len([e for e in emergencies if e.get('triage_level') == 'Urgent'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Emergencies", len(emergencies) if emergencies else 0)
        with col2:
            st.metric("Critical Cases", critical, delta="🔴" if critical > 0 else "✅")
        with col3:
            st.metric("Urgent Cases", urgent, delta="🟠" if urgent > 0 else "✅")
        with col4:
            # Get available doctors for emergency
            available_docs = db.get_available_doctors()
            st.metric("Available Doctors", len(available_docs) if available_docs else 0)
        
        st.markdown("---")
        
        # Active Emergency Cases
        st.subheader("🚑 Active Emergency Cases")
        if emergencies:
            df = pd.DataFrame(emergencies)
            
            # Color code triage levels
            def color_triage(val):
                if val == 'Critical':
                    return 'background-color: rgba(255,0,0,0.3)'
                elif val == 'Urgent':
                    return 'background-color: rgba(255,165,0,0.3)'
                elif val == 'Moderate':
                    return 'background-color: rgba(255,255,0,0.2)'
                return 'background-color: rgba(0,255,0,0.2)'
            
            display_cols = ['emergency_id', 'patient_name', 'age', 'gender', 
                          'condition_description', 'triage_level', 'arrival_time', 'status']
            if all(col in df.columns for col in display_cols):
                styled_df = df[display_cols].style.map(
                    color_triage, subset=['triage_level']
                )
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No active emergency cases")
        
        st.markdown("---")
        
        # Register New Emergency
        st.subheader("➕ Register New Emergency Case")
        with st.form("emergency_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                emg_name = st.text_input("Patient Name *")
                emg_age = st.number_input("Age *", min_value=0, max_value=120, value=0)
                emg_gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            
            with col2:
                emg_condition = st.text_area("Condition/Injury *")
                emg_triage = st.selectbox("Triage Level *", 
                                         ["Critical", "Urgent", "Moderate", "Low"])
            
            with col3:
                emg_arrival = st.time_input("Arrival Time *")
                emg_ambulance = st.checkbox("Arrived by Ambulance")
            
            submitted = st.form_submit_button("🚨 Register Emergency", use_container_width=True)
            
            if submitted:
                if emg_name and emg_age > 0 and emg_condition:
                    emergency_id = db.register_emergency(
                        patient_name=emg_name,
                        age=emg_age,
                        gender=emg_gender,
                        condition=emg_condition,
                        triage_level=emg_triage,
                        arrival_time=emg_arrival,
                        ambulance_used=emg_ambulance
                    )
                    
                    if emergency_id:
                        st.success(f"✅ Emergency registered! ID: {emergency_id}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to register emergency")
                else:
                    st.error("❌ Please fill all required fields")

# ===== ANALYTICS & REPORTS =====
elif page == "📊 Analytics & Reports":
    st.title("📊 Analytics & Reports")
    
    if db: 
        # Revenue Report
        st.subheader("💰 Revenue Report")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date.today().replace(day=1))
        with col2:
            end_date = st.date_input("End Date", value=date.today())
        
        if st.button("Generate Revenue Report"):
            revenue = db.get_revenue_report(start_date, end_date)
            if revenue:
                df = pd.DataFrame(revenue)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Revenue Chart
                fig = px.line(df, x='date', y='net_revenue',
                            title='Daily Revenue Trend',
                            labels={'date': 'Date', 'net_revenue': 'Net Revenue (₹)'})
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#FEFFFF')
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Summary
                total_revenue = df['net_revenue'].sum()
                total_bills = df['total_bills'].sum()
                st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
                st.metric("Total Bills", int(total_bills))
            else:
                st.info("No revenue data for selected period")
        
        st.markdown("---")
        
        # Department Statistics
        st.subheader("🏥 Department-wise Patient Distribution")
        dept_data = db.get_department_wise_patients()
        if dept_data:
            df = pd.DataFrame(dept_data)
            fig = px.pie(df, values='patient_count', names='dept_name',
                       title='Patient Distribution by Department')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FEFFFF')
            )
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:14px; color:rgba(254,255,255,0.8);'>
    <p><strong>Smart Hospital Management System</strong> </p>
    <p> Mimansha Chauhan </p>
    <p>Fully Integrated: Frontend (Streamlit) + Backend (MySQL) + Analytics</p>
</div>
""", unsafe_allow_html=True)