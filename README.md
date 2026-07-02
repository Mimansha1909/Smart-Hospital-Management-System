# 🏥 Smart Hospital Management System

## Overview

The Smart Hospital Management System is a web-based application developed using **Python, Streamlit, and MySQL** to simplify day-to-day hospital operations. The project brings multiple hospital management tasks together into a single interface, allowing users to manage patients, doctors, appointments, beds, pharmacy inventory, billing, emergency cases, and basic hospital analytics.

This project was built as a learning project to understand full-stack application development using Python with a database backend.

---

## Features

### Patient Management
- Register new patients
- Search patients by ID
- View active patient records
- Store emergency contact details

### Doctor Management
- View all registered doctors
- Check doctor availability
- Display department information

### Appointment Management
- Book appointments
- Assign doctors to patients
- Manage department-wise appointments

### Bed Management
- View available beds
- Allocate beds to patients
- Monitor bed occupancy

### Pharmacy Management
- Display medicine inventory
- Detect low stock medicines
- Update medicine quantities
- View medicine expiry details

### Billing System
- Generate patient bills
- Calculate taxes and discounts
- Support insurance claims
- Track pending payments

### Emergency Management
- Register emergency cases
- Assign triage levels
- Record patient vitals
- Update emergency status

### Dashboard & Reports
- Total patients
- Available doctors
- Bed occupancy statistics
- Pending bills
- Emergency case overview
- Department-wise reports
- Weekly admissions
- Revenue reports

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Frontend | Streamlit |
| Database | MySQL |
| Data Handling | Pandas |
| Database Connector | MySQL Connector |
| Visualization | Plotly |

---

## Project Structure

```
Smart-Hospital-Management-System
│
├── database.py
├── hospfrontend.py
├── smart_hospital.sql
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Mimansha1909/Smart-Hospital-Management-System.git
```

### 2. Open the project folder

```bash
cd Smart-Hospital-Management-System
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 5. Install the required packages

```bash
pip install -r requirements.txt
```

### 6. Import the database

Open **MySQL Workbench** and import the provided

```
smart_hospital.sql
```

file.

### 7. Configure the database connection

Update the database credentials inside **database.py**.

Example:

```python
host = "localhost"
database = "smart_hospital"
user = "root"
password = "your_password"
```

### 8. Start the application

```bash
streamlit run hospfrontend.py
```

---

## Screenshots

Screenshots of the application can be added here.

Suggested screenshots:

- Dashboard
- Patient Registration
- Doctor Management
- Pharmacy Inventory
- Bed Management
- Billing
- Emergency Management

---

## What I Learned

Working on this project helped me gain practical experience with:

- Connecting Python applications to MySQL databases
- Performing CRUD operations
- Building interactive web applications using Streamlit
- Organizing backend logic using classes
- Managing relational databases
- Displaying analytics using Python
- Handling real-world data in tabular format

---

## Future Improvements

Some features that can be added in future versions include:

- User authentication
- Role-based access control
- PDF bill generation
- Medical report uploads
- Appointment reminders
- Email notifications
- Improved analytics dashboard
- Search and filtering enhancements

---

## Author

**Mimansha Chauhan**

GitHub:
https://github.com/Mimansha1909

---

## License

This project was created for educational and learning purposes.
