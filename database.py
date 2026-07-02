"""
SMART HOSPITAL MANAGEMENT SYSTEM
Backend Database Logic - Phase 2
Team Avengers

"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
import pandas as pd

class HospitalDatabase:
    """Database handler for Smart Hospital Management System"""
    
    def __init__(self, host='localhost', database='smart_hospital', 
                 user='root', password='YOUR_MYSQL_PASSWORD'):
        """Initialize database connection"""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("✅ Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")
    
    # ==========================================
    # PATIENT OPERATIONS 
    # ==========================================
    
    def register_patient(self, first_name, last_name, dob, gender, blood_group,
                        phone, email, address, emergency_contact_name, 
                        emergency_contact_number, admission_type):
        """Register a new patient"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO patients 
                (first_name, last_name, date_of_birth, gender, blood_group,
                 phone_number, email, address, emergency_contact_name,
                 emergency_contact_number, admission_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, dob, gender, blood_group,
                     phone, email, address, emergency_contact_name,
                     emergency_contact_number, admission_type)
            
            cursor.execute(query, values)
            self.connection.commit()
            patient_id = cursor.lastrowid
            cursor.close()
            
            print(f"✅ Patient registered successfully! Patient ID: {patient_id}")
            return patient_id
        except Error as e:
            print(f"❌ Error registering patient: {e}")
            return None
    
    def get_all_patients(self):
        """Retrieve all patients"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM patients WHERE status = 'Active' ORDER BY admission_date DESC"
            cursor.execute(query)
            patients = cursor.fetchall()
            cursor.close()
            return patients
        except Error as e:
            print(f"❌ Error fetching patients: {e}")
            return []
    
    def search_patient_by_id(self, patient_id):
        """Search patient by ID"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM patients WHERE patient_id = %s"
            cursor.execute(query, (patient_id,))
            patient = cursor.fetchone()
            cursor.close()
            return patient
        except Error as e:
            print(f"❌ Error searching patient: {e}")
            return None
    
    def create_appointment(self, patient_id, doctor_id, dept_id, 
                          appointment_date, appointment_time, reason):
        """Create a new appointment"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO appointments 
                (patient_id, doctor_id, dept_id, appointment_date, appointment_time, reason)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (patient_id, doctor_id, dept_id, appointment_date, appointment_time, reason)
            cursor.execute(query, values)
            self.connection.commit()
            appointment_id = cursor.lastrowid
            cursor.close()
            
            print(f"✅ Appointment created! Appointment ID: {appointment_id}")
            return appointment_id
        except Error as e:
            print(f"❌ Error creating appointment: {e}")
            return None
    
    # ==========================================
    # DOCTOR OPERATIONS 
    # ==========================================
    
    def get_all_doctors(self):
        """Get all doctors with department info"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT d.*, dept.dept_name 
                FROM doctors d
                LEFT JOIN departments dept ON d.dept_id = dept.dept_id
                ORDER BY d.first_name
            """
            cursor.execute(query)
            doctors = cursor.fetchall()
            cursor.close()
            return doctors
        except Error as e:
            print(f"❌ Error fetching doctors: {e}")
            return []
    
    def get_available_doctors(self, specialization=None):
        """Get available doctors, optionally filtered by specialization"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if specialization:
                query = """
                    SELECT d.*, dept.dept_name 
                    FROM doctors d
                    LEFT JOIN departments dept ON d.dept_id = dept.dept_id
                    WHERE d.status = 'Available' AND d.specialization LIKE %s
                """
                cursor.execute(query, (f'%{specialization}%',))
            else:
                query = """
                    SELECT d.*, dept.dept_name 
                    FROM doctors d
                    LEFT JOIN departments dept ON d.dept_id = dept.dept_id
                    WHERE d.status = 'Available'
                """
                cursor.execute(query)
            
            doctors = cursor.fetchall()
            cursor.close()
            return doctors
        except Error as e:
            print(f"❌ Error fetching available doctors: {e}")
            return []
     
    # ==========================================
    # BED MANAGEMENT 
    # ==========================================
    
    def get_available_beds(self, ward_type=None):
        """Get available beds, optionally filtered by ward type"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if ward_type:
                query = """
                    SELECT b.*, d.dept_name 
                    FROM beds b
                    LEFT JOIN departments d ON b.dept_id = d.dept_id
                    WHERE b.bed_status = 'Available' AND b.ward_type = %s
                """
                cursor.execute(query, (ward_type,))
            else:
                query = """
                    SELECT b.*, d.dept_name 
                    FROM beds b
                    LEFT JOIN departments d ON b.dept_id = d.dept_id
                    WHERE b.bed_status = 'Available'
                """
                cursor.execute(query)
            
            beds = cursor.fetchall()
            cursor.close()
            return beds
        except Error as e:
            print(f"❌ Error fetching beds: {e}")
            return []
    
    def allocate_bed(self, bed_id, patient_id):
        """Allocate a bed to a patient"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO bed_allocations (bed_id, patient_id)
                VALUES (%s, %s)
            """
            cursor.execute(query, (bed_id, patient_id))
            self.connection.commit()
            cursor.close()
            
            print(f"✅ Bed allocated successfully!")
            return True
        except Error as e:
            print(f"❌ Error allocating bed: {e}")
            return False
    
    def get_bed_occupancy_report(self):
        """Get bed occupancy statistics by department"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    d.dept_name,
                    COUNT(b.bed_id) AS total_beds,
                    SUM(CASE WHEN b.bed_status = 'Occupied' THEN 1 ELSE 0 END) AS occupied_beds,
                    SUM(CASE WHEN b.bed_status = 'Available' THEN 1 ELSE 0 END) AS available_beds,
                    ROUND((SUM(CASE WHEN b.bed_status = 'Occupied' THEN 1 ELSE 0 END) / 
                           COUNT(b.bed_id)) * 100, 2) AS occupancy_percentage
                FROM beds b
                JOIN departments d ON b.dept_id = d.dept_id
                GROUP BY d.dept_name
                ORDER BY occupancy_percentage DESC
            """
            cursor.execute(query)
            report = cursor.fetchall()
            cursor.close()
            return report
        except Error as e:
            print(f"❌ Error generating bed occupancy report: {e}")
            return []
    
    # ==========================================
    # PHARMACY OPERATIONS 
    # ==========================================
    
    def get_pharmacy_inventory(self):
        """Get complete pharmacy inventory"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    m.medicine_id,
                    m.medicine_name,
                    m.category,
                    pi.batch_number,
                    pi.stock_quantity,
                    pi.min_stock_level,
                    pi.unit_price,
                    pi.expiry_date,
                    CASE 
                        WHEN pi.stock_quantity = 0 THEN 'Out of Stock'
                        WHEN pi.stock_quantity < pi.min_stock_level THEN 'Low Stock'
                        ELSE 'In Stock'
                    END AS stock_status
                FROM medicines m
                JOIN pharmacy_inventory pi ON m.medicine_id = pi.medicine_id
                ORDER BY stock_status DESC, pi.stock_quantity ASC
            """
            cursor.execute(query)
            inventory = cursor.fetchall()
            cursor.close()
            return inventory
        except Error as e:
            print(f"❌ Error fetching inventory: {e}")
            return []
    
    def get_low_stock_medicines(self):
        """Get medicines with low stock"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    m.medicine_name,
                    pi.stock_quantity,
                    pi.min_stock_level,
                    pi.expiry_date
                FROM pharmacy_inventory pi
                JOIN medicines m ON pi.medicine_id = m.medicine_id
                WHERE pi.stock_quantity < pi.min_stock_level
                ORDER BY pi.stock_quantity ASC
            """
            cursor.execute(query)
            low_stock = cursor.fetchall()
            cursor.close()
            return low_stock
        except Error as e:
            print(f"❌ Error fetching low stock medicines: {e}")
            return []
    
    def update_medicine_stock(self, medicine_id, new_quantity):
        """Update medicine stock quantity"""
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE pharmacy_inventory 
                SET stock_quantity = %s, last_updated = NOW()
                WHERE medicine_id = %s
            """
            cursor.execute(query, (new_quantity, medicine_id))
            self.connection.commit()
            cursor.close()
            
            print(f"✅ Stock updated successfully!")
            return True
        except Error as e:
            print(f"❌ Error updating stock: {e}")
            return False
    
    # ==========================================
    # BILLING OPERATIONS 
    # ==========================================
    
    def create_bill(self, patient_id, total_amount, insurance_claim=0, 
                   discount=0, tax=0, payment_method='Cash'):
        """Create a new bill for a patient"""
        try:
            net_amount = total_amount - insurance_claim - discount + tax
            cursor = self.connection.cursor()
            query = """
                INSERT INTO billing 
                (patient_id, bill_date, total_amount, insurance_claim_amount,
                 discount_amount, tax_amount, net_amount, payment_method)
                VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, %s)
            """
            values = (patient_id, total_amount, insurance_claim, discount, 
                     tax, net_amount, payment_method)
            cursor.execute(query, values)
            self.connection.commit()
            bill_id = cursor.lastrowid
            cursor.close()
            
            print(f"✅ Bill created successfully! Bill ID: {bill_id}")
            return bill_id
        except Error as e:
            print(f"❌ Error creating bill: {e}")
            return None
     
    def add_bill_item(self, bill_id, item_type, description, quantity, rate):
        """Add item to bill"""
        try:
            amount = quantity * rate
            cursor = self.connection.cursor()
            query = """
                INSERT INTO bill_details 
                (bill_id, item_type, item_description, quantity, rate, amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (bill_id, item_type, description, quantity, rate, amount))
            self.connection.commit()
            cursor.close()
            
            print(f"✅ Bill item added!")
            return True
        except Error as e:
            print(f"❌ Error adding bill item: {e}")
            return False
    
    def get_patient_bill(self, patient_id):
        """Get complete bill details for a patient"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Get bill header
            query1 = """
                SELECT b.*, p.first_name, p.last_name
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                WHERE b.patient_id = %s
                ORDER BY b.bill_date DESC
                LIMIT 1
            """
            cursor.execute(query1, (patient_id,))
            bill_header = cursor.fetchone()
            
            if bill_header:
                # Get bill items
                query2 = """
                    SELECT * FROM bill_details
                    WHERE bill_id = %s
                """
                cursor.execute(query2, (bill_header['bill_id'],))
                bill_items = cursor.fetchall()
                cursor.close()
                
                return {'header': bill_header, 'items': bill_items}
            
            cursor.close()
            return None
        except Error as e:
            print(f"❌ Error fetching bill: {e}")
            return None
    
    def get_pending_bills(self):
        """Get all pending bills"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT b.bill_id, b.bill_date, b.net_amount, b.payment_status,
                       CONCAT(p.first_name, ' ', p.last_name) AS patient_name
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                WHERE b.payment_status IN ('Pending', 'Partial')
                ORDER BY b.bill_date DESC
            """
            cursor.execute(query)
            bills = cursor.fetchall()
            cursor.close()
            return bills
        except Error as e:
            print(f"❌ Error fetching pending bills: {e}")
            return []
    
    # ==========================================
    # EMERGENCY OPERATIONS 
    # ========  ==================================
    
    def register_emergency(self, patient_name, age, gender, condition, 
                          triage_level, arrival_time, ambulance_used=False):
        """Register a new emergency case"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO emergency_records 
                (patient_name, age, gender, condition_description, triage_level,
                 arrival_time, ambulance_used)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (patient_name, age, gender, condition, triage_level, 
                     arrival_time, ambulance_used)
            cursor.execute(query, values)
            self.connection.commit()
            emergency_id = cursor.lastrowid
            cursor.close()
            
            print(f"✅ Emergency registered! Emergency ID: {emergency_id}")
            return emergency_id
        except Error as e:
            print(f"❌ Error registering emergency: {e}")
            return None
    
    def get_active_emergencies(self):
        """Get all active emergency cases"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT er.*, CONCAT(d.first_name, ' ', d.last_name) AS doctor_name
                FROM emergency_records er
                LEFT JOIN doctors d ON er.attending_doctor_id = d.doctor_id
                WHERE er.status NOT IN ('Discharged', 'Deceased')
                ORDER BY FIELD(er.triage_level, 'Critical', 'Urgent', 'Moderate', 'Low'),
                         er.arrival_time DESC
            """
            cursor.execute(query)
            emergencies = cursor.fetchall()
            cursor.close()
            return emergencies
        except Error as e:
            print(f"❌ Error fetching emergencies: {e}")
            return []
    
    def update_emergency_status(self, emergency_id, new_status, doctor_id=None):
        """Update emergency case status"""
        try:
            cursor = self.connection.cursor()
            if doctor_id:
                query = """
                    UPDATE emergency_records 
                    SET status = %s, attending_doctor_id = %s
                    WHERE emergency_id = %s
                """
                cursor.execute(query, (new_status, doctor_id, emergency_id))
            else:
                query = """
                    UPDATE emergency_records 
                    SET status = %s
                    WHERE emergency_id = %s
                """
                cursor.execute(query, (new_status, emergency_id))
            
            self.connection.commit()
            cursor.close()
            
            print(f"✅ Emergency status updated!")
            return True
        except Error as e:
            print(f"❌ Error updating emergency: {e}")
            return False
    
    def record_vitals(self, patient_id, bp_sys, bp_dia, heart_rate, 
                     temperature, oxygen_sat, respiratory_rate, 
                     blood_sugar=None, notes=None):
        """Record patient vitals"""
        try:
            cursor = self.connection.cursor()
            
            # Determine alert status
            alert_status = 'Normal'
            if (bp_sys > 140 or bp_dia > 90 or heart_rate > 100 or 
                temperature > 38.0 or oxygen_sat < 90):
                alert_status = 'Warning'
            if (bp_sys > 180 or bp_dia > 120 or heart_rate > 120 or 
                temperature > 39.5 or oxygen_sat < 85):
                alert_status = 'Critical'
            
            query = """
                INSERT INTO vitals_monitoring 
                (patient_id, blood_pressure_systolic, blood_pressure_diastolic,
                 heart_rate, temperature, oxygen_saturation, respiratory_rate,
                 blood_sugar, notes, alert_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (patient_id, bp_sys, bp_dia, heart_rate, temperature,
                     oxygen_sat, respiratory_rate, blood_sugar, notes, alert_status)
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            
            print(f"✅ Vitals recorded! Status: {alert_status}")
            return alert_status
        except Error as e:
            print(f"❌ Error recording vitals: {e}")
            return None
    
    # ==========================================
    # ANALYTICS & REPORTS 
    # ==========================================
    
    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            stats = {}
            
            # Total active patients
            cursor.execute("SELECT COUNT(*) as count FROM patients WHERE status = 'Active'")
            stats['total_patients'] = cursor.fetchone()['count']
            
            # Available doctors
            cursor.execute("SELECT COUNT(*) as count FROM doctors WHERE status = 'Available'")
            stats['available_doctors'] = cursor.fetchone()['count']
            
            # Total beds and occupied beds
            cursor.execute("SELECT COUNT(*) as count FROM beds")
            stats['total_beds'] = cursor.fetchone()['count']
            cursor.execute("SELECT COUNT(*) as count FROM beds WHERE bed_status = 'Occupied'")
            stats['occupied_beds'] = cursor.fetchone()['count']
            
            # Today's emergencies
            cursor.execute("""
                SELECT COUNT(*) as count FROM emergency_records 
                WHERE DATE(arrival_time) = CURDATE()
            """)
            stats['todays_emergencies'] = cursor.fetchone()['count']
            
            # Pending bills
            cursor.execute("""
                SELECT COUNT(*) as count FROM billing 
                WHERE payment_status IN ('Pending', 'Partial')
            """)
            stats['pending_bills'] = cursor.fetchone()['count']
            
            cursor.close()
            return stats
        except Error as e:
            print(f"❌ Error fetching dashboard stats: {e}")
            return {}
    
    def get_department_wise_patients(self):
        """Get patient distribution by department"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT d.dept_name, COUNT(DISTINCT a.patient_id) as patient_count
                FROM departments d
                LEFT JOIN appointments a ON d.dept_id = a.dept_id
                WHERE a.appointment_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY d.dept_name
                ORDER BY patient_count DESC
            """
            cursor.execute(query)
            distribution = cursor.fetchall()
            cursor.close()
            return distribution
        except Error as e:
            print(f"❌ Error fetching department distribution: {e}")
            return []
    
    def get_weekly_admissions(self):
        """Get weekly admission statistics"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    DAYNAME(admission_date) as day_name,
                    COUNT(*) as admission_count
                FROM patients
                WHERE admission_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY DAYOFWEEK(admission_date), DAYNAME(admission_date)
                ORDER BY DAYOFWEEK(admission_date)
            """
            cursor.execute(query)
            admissions = cursor.fetchall()
            cursor.close()
            return admissions
        except Error as e:
            print(f"❌ Error fetching weekly admissions: {e}")
            return []
    
    def get_doctor_workload(self):
        """Get doctor workload statistics"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
                    dept.dept_name,
                    COUNT(a.appointment_id) AS total_appointments,
                    d.status
                FROM doctors d
                LEFT JOIN appointments a ON d.doctor_id = a.doctor_id 
                    AND a.appointment_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                LEFT JOIN departments dept ON d.dept_id = dept.dept_id
                GROUP BY d.doctor_id
                ORDER BY total_appointments DESC
                LIMIT 10
            """
            cursor.execute(query)
            workload = cursor.fetchall()
            cursor.close()
            return workload
        except Error as e:
            print(f"❌ Error fetching doctor workload: {e}")
            return []
    
    def get_expiring_medicines(self, days=90):
        """Get medicines expiring within specified days"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    m.medicine_name,
                    pi.batch_number,
                    pi.stock_quantity,
                    pi.expiry_date,
                    DATEDIFF(pi.expiry_date, CURDATE()) AS days_to_expiry
                FROM pharmacy_inventory pi
                JOIN medicines m ON pi.medicine_id = m.medicine_id
                WHERE pi.expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
                ORDER BY pi.expiry_date ASC
            """
            cursor.execute(query, (days,))
            expiring = cursor.fetchall()
            cursor.close()
            return expiring
        except Error as e:
            print(f"❌ Error fetching expiring medicines: {e}")
            return []
    
    def get_revenue_report(self, start_date=None, end_date=None):
        """Get revenue report for specified date range"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if not start_date:
                start_date = datetime.now().replace(day=1).date()
            if not end_date:
                end_date = datetime.now().date()
            
            query = """
                SELECT 
                    DATE(bill_date) as date,
                    COUNT(*) as total_bills,
                    SUM(total_amount) as total_revenue,
                    SUM(insurance_claim_amount) as insurance_claims,
                    SUM(net_amount) as net_revenue
                FROM billing
                WHERE bill_date BETWEEN %s AND %s
                GROUP BY DATE(bill_date)
                ORDER BY date DESC
            """
            cursor.execute(query, (start_date, end_date))
            revenue = cursor.fetchall()
            cursor.close()
            return revenue
        except Error as e:
            print(f"❌ Error fetching revenue report: {e}")
            return []


# ==========================================
# EXAMPLE USAGE & TESTING
# ==========================================

def test_database():
    """Test database functions"""
    print("=" * 50)
    print("TESTING HOSPITAL DATABASE SYSTEM")
    print("=" * 50)
    
    # Initialize database
    db = HospitalDatabase(
        host='localhost',
        database='smart_hospital',
        user='root',
        password='YOUR_MYSQL_PASSWORD'  
    )
    
    # Connect
    if not db.connect():
        print("Failed to connect to database!")
        return
    
    print("\n1. Testing Dashboard Stats...")
    stats = db.get_dashboard_stats()
    print(f"   Total Patients: {stats.get('total_patients', 0)}")
    print(f"   Available Doctors: {stats.get('available_doctors', 0)}")
    print(f"   Beds: {stats.get('occupied_beds', 0)}/{stats.get('total_beds', 0)}")
    
    print("\n2. Testing Patient Registration...")
    patient_id = db.register_patient(
        first_name="Test",
        last_name="Patient",
        dob=date(1990, 1, 1),
        gender="Male",
        blood_group="B+",
        phone="9999999999",
        email="test@hospital.com",
        address="Test Address",
        emergency_contact_name="Emergency Contact",
        emergency_contact_number="8888888888",
        admission_type="OPD"
    )
    
    print("\n3. Testing Available Doctors...")
    doctors = db.get_available_doctors()
    print(f"   Found {len(doctors)} available doctors")
    
    print("\n4. Testing Low Stock Medicines...")
    low_stock = db.get_low_stock_medicines()
    print(f"   Found {len(low_stock)} low stock items")
    for item in low_stock[:3]:
        print(f"   - {item['medicine_name']}: {item['stock_quantity']} units")
    
    print("\n5. Testing Bed Occupancy Report...")
    occupancy = db.get_bed_occupancy_report()
    for dept in occupancy:
        print(f"   {dept['dept_name']}: {dept['occupancy_percentage']}% occupied")
    
    print("\n6. Testing Active Emergencies...")
    emergencies = db.get_active_emergencies()
    print(f"   Found {len(emergencies)} active emergency cases")
    
    # Disconnect
    db.disconnect()
    
    print("\n" + "=" * 50)
    print("TESTING COMPLETED!")
    print("=" * 50)


if __name__ == "__main__":
    # Run tests when file is executed directly
    test_database()