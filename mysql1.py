import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
import datetime
import random
from heapq import heappush, heappop

class PatientRecordSystem:
    def __init__(self):
        """Initialize the database connection and create tables if they don't exist"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='arshdeep12' meditrack
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                
                # Create database if not exists
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS meditrack")
                self.cursor.execute("USE meditrack")
                
                # Create patients table if not exists
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    date_of_birth DATE NOT NULL,
                    gender ENUM('Male', 'Female', 'Other') NOT NULL,
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    address TEXT,
                    last_visit_date DATE,
                    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
                
                # Create medical_history table if not exists
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS medical_history (
                    history_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    entry_date DATE NOT NULL,
                    diagnosis VARCHAR(255) NOT NULL,
                    treatment TEXT,
                    notes TEXT,
                    severity INT COMMENT '1-10 scale',
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
                )
                """)
                
                # Create appointments table if not exists
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    appointment_date DATE NOT NULL,
                    start_time TIME NOT NULL,
                    end_time TIME NOT NULL,
                    purpose VARCHAR(255),
                    status ENUM('Scheduled', 'Completed', 'Cancelled', 'No-show') DEFAULT 'Scheduled',
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
                )
                """)
                
                self.connection.commit()
                print("Database connection established and tables verified.")
                
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
    
    # Patient CRUD operations
    def add_patient(self, first_name, last_name, date_of_birth, gender, 
                   phone=None, email=None, address=None, blood_type=None):
        """Add a new patient to the database"""
        try:
            query = """
            INSERT INTO patients 
            (first_name, last_name, date_of_birth, gender, phone, email, address, blood_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, date_of_birth, gender, 
                      phone, email, address, blood_type)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding patient: {e}")
            return None
    
    def update_patient(self, patient_id, **kwargs):
        """Update patient information"""
        if not kwargs:
            return False
            
        try:
            set_clause = ", ".join([f"{key} = %s" for key in kwargs])
            query = f"UPDATE patients SET {set_clause} WHERE patient_id = %s"
            values = tuple(kwargs.values()) + (patient_id,)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating patient: {e}")
            return False
    
    def delete_patient(self, patient_id):
        """Delete a patient from the database"""
        try:
            query = "DELETE FROM patients WHERE patient_id = %s"
            self.cursor.execute(query, (patient_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Database Error", f"Error deleting patient: {e}")
            return False
    
    def get_patient(self, patient_id):
        """Retrieve a single patient by ID"""
        try:
            query = "SELECT * FROM patients WHERE patient_id = %s"
            self.cursor.execute(query, (patient_id,))
            result = self.cursor.fetchone()
            
            if result:
                return self._format_patient(result)
            return None
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving patient: {e}")
            return None
    
    def get_all_patients(self):
        """Retrieve all patients from the database"""
        try:
            query = "SELECT * FROM patients"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            return [self._format_patient(row) for row in results]
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving patients: {e}")
            return []
    
    # Medical History CRUD operations
    def add_medical_history(self, patient_id, diagnosis, entry_date=None, 
                          treatment=None, notes=None, severity=None):
        """Add a medical history entry for a patient"""
        if entry_date is None:
            entry_date = datetime.date.today()
            
        try:
            query = """
            INSERT INTO medical_history 
            (patient_id, entry_date, diagnosis, treatment, notes, severity)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (patient_id, entry_date, diagnosis, treatment, notes, severity)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding medical history: {e}")
            return None
    
    def get_medical_history(self, patient_id):
        """Get all medical history entries for a patient"""
        try:
            query = """
            SELECT * FROM medical_history 
            WHERE patient_id = %s
            ORDER BY entry_date DESC
            """
            self.cursor.execute(query, (patient_id,))
            results = self.cursor.fetchall()
            
            return [self._format_medical_history(row) for row in results]
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving medical history: {e}")
            return []
    
    def update_medical_history(self, history_id, **kwargs):
        """Update a medical history entry"""
        if not kwargs:
            return False
            
        try:
            set_clause = ", ".join([f"{key} = %s" for key in kwargs])
            query = f"UPDATE medical_history SET {set_clause} WHERE history_id = %s"
            values = tuple(kwargs.values()) + (history_id,)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating medical history: {e}")
            return False
    
    def delete_medical_history(self, history_id):
        """Delete a medical history entry"""
        try:
            query = "DELETE FROM medical_history WHERE history_id = %s"
            self.cursor.execute(query, (history_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Database Error", f"Error deleting medical history: {e}")
            return False
    
    # Appointment CRUD operations
    def add_appointment(self, patient_id, appointment_date, start_time, 
                       end_time, purpose=None, status='Scheduled', notes=None):
        """Add a new appointment"""
        try:
            query = """
            INSERT INTO appointments 
            (patient_id, appointment_date, start_time, end_time, purpose, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (patient_id, appointment_date, start_time, end_time, 
                     purpose, status, notes)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding appointment: {e}")
            return None
    
    def get_appointments(self, date=None, patient_id=None):
        """Get appointments, optionally filtered by date or patient"""
        try:
            query = """
            SELECT a.*, p.first_name, p.last_name 
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            """
            
            conditions = []
            values = []
            
            if date:
                conditions.append("a.appointment_date = %s")
                values.append(date)
            
            if patient_id:
                conditions.append("a.patient_id = %s")
                values.append(patient_id)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY a.appointment_date, a.start_time"
            
            self.cursor.execute(query, tuple(values))
            results = self.cursor.fetchall()
            
            return [self._format_appointment(row) for row in results]
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving appointments: {e}")
            return []
    
    def update_appointment(self, appointment_id, **kwargs):
        """Update an appointment"""
        if not kwargs:
            return False
            
        try:
            set_clause = ", ".join([f"{key} = %s" for key in kwargs])
            query = f"UPDATE appointments SET {set_clause} WHERE appointment_id = %s"
            values = tuple(kwargs.values()) + (appointment_id,)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating appointment: {e}")
            return False
    
    def delete_appointment(self, appointment_id):
        """Delete an appointment"""
        try:
            query = "DELETE FROM appointments WHERE appointment_id = %s"
            self.cursor.execute(query, (appointment_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Database Error", f"Error deleting appointment: {e}")
            return False
    
    # Sorting algorithms
    def quick_sort_patients(self, patients, key, reverse=False):
        """Quick sort implementation for patient records"""
        if len(patients) <= 1:
            return patients
        
        pivot = patients[len(patients) // 2]           #arsh's code
        
        # Handle different key types (date fields need special handling)
        if key in ['date_of_birth', 'last_visit_date']:
            pivot_val = self._parse_date(pivot[key])
            less = [p for p in patients if self._parse_date(p[key]) < pivot_val]
            equal = [p for p in patients if self._parse_date(p[key]) == pivot_val]
            greater = [p for p in patients if self._parse_date(p[key]) > pivot_val]
        else:
            pivot_val = pivot[key] if pivot[key] is not None else ""
            less = [p for p in patients if (p[key] or "") < pivot_val]
            equal = [p for p in patients if (p[key] or "") == pivot_val]
            greater = [p for p in patients if (p[key] or "") > pivot_val]
        
        if reverse:
            return self.quick_sort_patients(greater, key, reverse) + equal + self.quick_sort_patients(less, key, reverse)
        else:
            return self.quick_sort_patients(less, key, reverse) + equal + self.quick_sort_patients(greater, key, reverse)
    
    def heap_sort_medical_history(self, history_entries, key='entry_date', reverse=False):
        """Heap sort implementation for medical history entries"""
        if not history_entries:
            return []
        
        # Create a max heap or min heap based on reverse flag 
        heap = []
        for entry in history_entries:                                   #Arsh's code
            # Handle different key types
            if key == 'entry_date':
                value = self._parse_date(entry[key])
            elif key == 'severity':
                value = entry[key] if entry[key] is not None else 0
            else:
                value = entry[key] if entry[key] is not None else ""
            
            # For reverse (descending) sort, we invert the value
            if reverse:
                heappush(heap, (-value, entry))
            else:
                heappush(heap, (value, entry))
        
        # Extract elements from the heap in sorted order
        sorted_history = []
        while heap:
            val, entry = heappop(heap)
            if reverse:
                sorted_history.append(entry)
            else:
                sorted_history.append(entry)
        
        return sorted_history
    
    def merge_sort_appointments(self, appointments, key='start_time', reverse=False):
        """Merge sort implementation for appointments"""
        if len(appointments) <= 1:
            return appointments
        
        mid = len(appointments) // 2
        left = self.merge_sort_appointments(appointments[:mid], key, reverse)
        right = self.merge_sort_appointments(appointments[mid:], key, reverse)
        
        return self._merge_appointments(left, right, key, reverse)
    
    def _merge_appointments(self, left, right, key, reverse):
        """Merge helper function for merge sort"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            # Handle different comparison types
            if key in ['appointment_date', 'entry_date']:
                left_val = self._parse_date(left[i][key])
                right_val = self._parse_date(right[j][key])
            elif key in ['start_time', 'end_time']:
                left_val = self._parse_time(left[i][key])
                right_val = self._parse_time(right[j][key])
            else:
                left_val = left[i][key] if left[i][key] is not None else ""
                right_val = right[j][key] if right[j][key] is not None else ""
            
            if reverse:
                if left_val > right_val:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            else:
                if left_val < right_val:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    # Helper methods
    def _format_patient(self, row):
        """Format a database row into a patient dictionary"""
        columns = [
            'patient_id', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'phone', 'email', 'address', 'last_visit_date', 'blood_type', 'registration_date'
        ]
        return dict(zip(columns, row))
    
    def _format_medical_history(self, row):
        """Format a database row into a medical history dictionary"""
        columns = [
            'history_id', 'patient_id', 'entry_date', 'diagnosis',
            'treatment', 'notes', 'severity'
        ]
        return dict(zip(columns, row))
    
    def _format_appointment(self, row):
        """Format a database row into an appointment dictionary"""
        columns = [
            'appointment_id', 'patient_id', 'appointment_date', 'start_time',
            'end_time', 'purpose', 'status', 'notes', 'first_name', 'last_name'
        ]
        return dict(zip(columns, row))
    
    def _parse_date(self, date_str):
        """Helper method to parse date strings into datetime objects for comparison"""
        if isinstance(date_str, datetime.date):
            return date_str
        if date_str is None:
            return datetime.date.min
        return datetime.datetime.strptime(str(date_str), '%Y-%m-%d').date()
    
    def _parse_time(self, time_str):
        """Helper method to parse time strings into time objects for comparison"""
        if isinstance(time_str, datetime.time):
            return time_str
        if time_str is None:
            return datetime.time.min
        return datetime.datetime.strptime(str(time_str), '%H:%M:%S').time()
    
    def record_last_visit(self, patient_id, visit_date=None):
        """Record a patient's last visit date"""
        if visit_date is None:
            visit_date = datetime.date.today()
        return self.update_patient(patient_id, last_visit_date=visit_date)
    
    def generate_sample_data(self, num_patients=20):
        """Generate sample patient data for testing"""
        first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", 
                      "Robert", "Jennifer", "William", "Lisa", "James", "Jessica"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", 
                     "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', None]
        diagnoses = [
            "Hypertension", "Diabetes Type 2", "Asthma", "Migraine", 
            "Arthritis", "Bronchitis", "Influenza", "Allergic Rhinitis",
            "Hyperlipidemia", "GERD", "Anxiety Disorder", "Depression"
        ]
        treatments = [
            "Medication prescribed", "Physical therapy recommended",
            "Lifestyle changes advised", "Scheduled follow-up",
            "Referred to specialist", "Surgery recommended",
            "Dietary changes suggested", "Monitoring required"
        ]
        purposes = [
            "Routine checkup", "Follow-up visit", "Vaccination",
            "Test results review", "Consultation", "Treatment"
        ]
        
        for _ in range(num_patients):
            first = random.choice(first_names)
            last = random.choice(last_names)
            dob = datetime.date(
                year=random.randint(1940, 2020),
                month=random.randint(1, 12),
                day=random.randint(1, 28)
            )
            gender = random.choice(['Male', 'Female', 'Other'])
            phone = f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
            email = f"{first.lower()}.{last.lower()}@example.com"
            address = f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple'])} St."
            blood = random.choice(blood_types)
            
            # Add patient
            patient_id = self.add_patient(
                first_name=first,
                last_name=last,
                date_of_birth=dob,
                gender=gender,
                phone=phone,
                email=email,
                address=address,
                blood_type=blood
            )
            
            # Add medical history (1-5 entries per patient)
            for _ in range(random.randint(1, 5)):
                entry_date = datetime.date(
                    year=random.randint(2018, 2023),
                    month=random.randint(1, 12),
                    day=random.randint(1, 28)
                )
                diagnosis = random.choice(diagnoses)
                treatment = random.choice(treatments)
                notes = "Sample note for testing purposes" if random.random() > 0.5 else None
                severity = random.randint(1, 10) if random.random() > 0.3 else None
                
                self.add_medical_history(
                    patient_id=patient_id,
                    entry_date=entry_date,
                    diagnosis=diagnosis,
                    treatment=treatment,
                    notes=notes,
                    severity=severity
                )
            
            # Add appointments (1-3 per patient)
            for _ in range(random.randint(1, 3)):
                appointment_date = datetime.date(
                    year=2023,
                    month=random.randint(1, 12),
                    day=random.randint(1, 28)
                )
                
                # Generate random time between 9:00 and 17:00 (5PM)
                hour = random.randint(9, 16)
                minute = random.choice([0, 15, 30, 45])
                start_time = datetime.time(hour, minute)
                end_time = datetime.time(hour, minute + 30)
                
                purpose = random.choice(purposes)
                status = random.choice(['Scheduled', 'Completed', 'Cancelled', 'No-show'])
                notes = "Sample appointment note" if random.random() > 0.7 else None
                
                self.add_appointment(
                    patient_id=patient_id,
                    appointment_date=appointment_date,
                    start_time=start_time,
                    end_time=end_time,
                    purpose=purpose,
                    status=status,
                    notes=notes
                )
            
            # Randomly decide if this patient has visited before
            if random.random() > 0.3:  # 70% chance they've visited
                last_visit = datetime.date(
                    year=random.randint(2018, 2023),
                    month=random.randint(1, 12),
                    day=random.randint(1, 28)
                )
                self.record_last_visit(patient_id, last_visit)
    
    def close(self):
        """Close the database connection"""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()


class MediTrackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MediTrack Healthcare Management System")
        self.root.geometry("1200x700")
        
        # Initialize database system
        self.system = PatientRecordSystem()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_patient_tab()
        self.create_medical_history_tab()
        self.create_appointment_tab()
        
        # Create status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status("Ready")
        
        # Load initial data
        self.refresh_patient_list()
        self.refresh_appointment_list()
    
    def create_menu_bar(self):
        """Create the menu bar with all commands"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Generate Sample Data", command=self.generate_sample_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Patient menu
        patient_menu = tk.Menu(menubar, tearoff=0)
        patient_menu.add_command(label="Add New Patient", command=self.add_patient)
        patient_menu.add_command(label="Edit Selected Patient", command=self.edit_patient)
        patient_menu.add_command(label="Delete Selected Patient", command=self.delete_patient)
        patient_menu.add_separator()
        patient_menu.add_command(label="Record Visit", command=self.record_visit)
        menubar.add_cascade(label="Patient", menu=patient_menu)
        
        # Medical History menu
        history_menu = tk.Menu(menubar, tearoff=0)
        history_menu.add_command(label="Add History Entry", command=self.add_medical_history)
        history_menu.add_command(label="Edit History Entry", command=self.edit_medical_history)
        history_menu.add_command(label="Delete History Entry", command=self.delete_medical_history)
        menubar.add_cascade(label="Medical History", menu=history_menu)
        
        # Appointment menu
        appointment_menu = tk.Menu(menubar, tearoff=0)
        appointment_menu.add_command(label="Schedule Appointment", command=self.schedule_appointment)
        appointment_menu.add_command(label="Edit Appointment", command=self.edit_appointment)
        appointment_menu.add_command(label="Cancel Appointment", command=self.cancel_appointment)
        appointment_menu.add_separator()
        appointment_menu.add_command(label="Mark as Completed", command=self.complete_appointment)
        menubar.add_cascade(label="Appointments", menu=appointment_menu)
        
        # Sort menu
        sort_menu = tk.Menu(menubar, tearoff=0)
        
        # Patient sorting
        patient_sort_menu = tk.Menu(sort_menu, tearoff=0)
        patient_sort_menu.add_command(label="By Last Name (A-Z)", command=lambda: self.sort_patients('last_name'))
        patient_sort_menu.add_command(label="By Last Name (Z-A)", command=lambda: self.sort_patients('last_name', True))
        patient_sort_menu.add_separator()
        patient_sort_menu.add_command(label="By Date of Birth (Oldest First)", command=lambda: self.sort_patients('date_of_birth'))
        patient_sort_menu.add_command(label="By Date of Birth (Youngest First)", command=lambda: self.sort_patients('date_of_birth', True))
        patient_sort_menu.add_separator()
        patient_sort_menu.add_command(label="By Last Visit (Recent First)", command=lambda: self.sort_patients('last_visit_date', True))
        patient_sort_menu.add_command(label="By Last Visit (Oldest First)", command=lambda: self.sort_patients('last_visit_date'))
        sort_menu.add_cascade(label="Patients", menu=patient_sort_menu)
        
        # Medical History sorting
        history_sort_menu = tk.Menu(sort_menu, tearoff=0)
        history_sort_menu.add_command(label="By Date (Recent First)", command=lambda: self.sort_medical_history('entry_date', True))
        history_sort_menu.add_command(label="By Date (Oldest First)", command=lambda: self.sort_medical_history('entry_date'))
        history_sort_menu.add_separator()
        history_sort_menu.add_command(label="By Severity (High First)", command=lambda: self.sort_medical_history('severity', True))
        history_sort_menu.add_command(label="By Severity (Low First)", command=lambda: self.sort_medical_history('severity'))
        history_sort_menu.add_separator()
        history_sort_menu.add_command(label="By Diagnosis (A-Z)", command=lambda: self.sort_medical_history('diagnosis'))
        history_sort_menu.add_command(label="By Diagnosis (Z-A)", command=lambda: self.sort_medical_history('diagnosis', True))
        sort_menu.add_cascade(label="Medical History", menu=history_sort_menu)
        
        # Appointment sorting
        appointment_sort_menu = tk.Menu(sort_menu, tearoff=0)
        appointment_sort_menu.add_command(label="By Date (Chronological)", command=lambda: self.sort_appointments('appointment_date'))
        appointment_sort_menu.add_command(label="By Date (Reverse)", command=lambda: self.sort_appointments('appointment_date', True))
        appointment_sort_menu.add_separator()
        appointment_sort_menu.add_command(label="By Time (Earliest First)", command=lambda: self.sort_appointments('start_time'))
        appointment_sort_menu.add_command(label="By Time (Latest First)", command=lambda: self.sort_appointments('start_time', True))
        appointment_sort_menu.add_separator()
        appointment_sort_menu.add_command(label="By Patient Name (A-Z)", command=lambda: self.sort_appointments('last_name'))
        appointment_sort_menu.add_command(label="By Patient Name (Z-A)", command=lambda: self.sort_appointments('last_name', True))
        sort_menu.add_cascade(label="Appointments", menu=appointment_sort_menu)
        
        menubar.add_cascade(label="Sort", menu=sort_menu)
        
        self.root.config(menu=menubar)
    
    def create_patient_tab(self):
        """Create the patient management tab"""
        self.patient_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.patient_tab, text="Patient Management")
        
        # Create search frame
        search_frame = ttk.LabelFrame(self.patient_tab, text="Search Patients", padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search entry
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=0, column=1, padx=(0, 5))
        self.search_entry.bind("<KeyRelease>", self.on_search_changed)
        
        # Search options
        self.search_by_var = tk.StringVar(value="last_name")
        ttk.Radiobutton(
            search_frame, 
            text="Last Name", 
            variable=self.search_by_var, 
            value="last_name"
        ).grid(row=0, column=2, padx=(10, 5))
        ttk.Radiobutton(
            search_frame, 
            text="First Name", 
            variable=self.search_by_var, 
            value="first_name"
        ).grid(row=0, column=3, padx=(0, 5))
        ttk.Radiobutton(
            search_frame, 
            text="Patient ID", 
            variable=self.search_by_var, 
            value="patient_id"
        ).grid(row=0, column=4, padx=(0, 5))
        
        # Buttons
        ttk.Button(
            search_frame, 
            text="Clear", 
            command=self.clear_search
        ).grid(row=0, column=5, padx=(10, 0))
        
        # Create patient list treeview
        self.create_patient_list()
    
    def create_medical_history_tab(self):
        """Create the medical history management tab"""
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="Medical History")
        
        # Create patient selection frame
        selection_frame = ttk.Frame(self.history_tab, padding="10")
        selection_frame.pack(fill=tk.X)
        
        ttk.Label(selection_frame, text="Select Patient:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.patient_combobox = ttk.Combobox(
            selection_frame,
            state="readonly",
            width=40
        )
        self.patient_combobox.pack(side=tk.LEFT, padx=(0, 10))
        self.patient_combobox.bind("<<ComboboxSelected>>", self.on_patient_selected)
        
        # Create history list treeview
        self.create_history_list()
    
    def create_appointment_tab(self):
        """Create the appointment management tab"""
        self.appointment_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.appointment_tab, text="Appointments")
        
        # Create filter frame
        filter_frame = ttk.Frame(self.appointment_tab, padding="10")
        filter_frame.pack(fill=tk.X)
        
        # Date filter
        ttk.Label(filter_frame, text="Filter by Date:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.appointment_date_var = tk.StringVar()
        self.appointment_date_entry = ttk.Entry(filter_frame, textvariable=self.appointment_date_var, width=15)
        self.appointment_date_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.appointment_date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
        
        ttk.Button(
            filter_frame, 
            text="Apply", 
            command=self.filter_appointments_by_date
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            filter_frame, 
            text="Show All", 
            command=self.show_all_appointments
        ).pack(side=tk.LEFT)
        
        # Status filter
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=(20, 5))
        
        self.status_filter_var = tk.StringVar(value="All")
        ttk.Combobox(
            filter_frame,
            textvariable=self.status_filter_var,
            values=["All", "Scheduled", "Completed", "Cancelled", "No-show"],
            state="readonly",
            width=12
        ).pack(side=tk.LEFT, padx=(0, 10))
        self.status_filter_var.trace('w', self.filter_appointments_by_status)
        
        # Create appointment list treeview
        self.create_appointment_list()
    
    def create_patient_list(self):
        """Create the treeview widget to display patients"""
        # Create frame for treeview and scrollbars
        tree_frame = ttk.Frame(self.patient_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        self.patient_tree = ttk.Treeview(
            tree_frame,
            columns=('id', 'last_name', 'first_name', 'dob', 'gender', 'last_visit', 'blood_type'),
            show='headings'
        )
        
        # Define columns
        self.patient_tree.heading('id', text='ID', anchor=tk.W)
        self.patient_tree.heading('last_name', text='Last Name', anchor=tk.W)
        self.patient_tree.heading('first_name', text='First Name', anchor=tk.W)
        self.patient_tree.heading('dob', text='Date of Birth', anchor=tk.W)
        self.patient_tree.heading('gender', text='Gender', anchor=tk.W)
        self.patient_tree.heading('last_visit', text='Last Visit', anchor=tk.W)
        self.patient_tree.heading('blood_type', text='Blood Type', anchor=tk.W)
        
        # Set column widths
        self.patient_tree.column('id', width=50, minwidth=50)
        self.patient_tree.column('last_name', width=120, minwidth=120)
        self.patient_tree.column('first_name', width=120, minwidth=120)
        self.patient_tree.column('dob', width=100, minwidth=100)
        self.patient_tree.column('gender', width=80, minwidth=80)
        self.patient_tree.column('last_visit', width=100, minwidth=100)
        self.patient_tree.column('blood_type', width=80, minwidth=80)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.patient_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.patient_tree.xview)
        self.patient_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.patient_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double click to edit patient
        self.patient_tree.bind("<Double-1>", self.edit_patient)
    
    def create_history_list(self):
        """Create the treeview widget to display medical history"""
        # Create frame for treeview and scrollbars
        tree_frame = ttk.Frame(self.history_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create treeview
        self.history_tree = ttk.Treeview(
            tree_frame,
            columns=('id', 'date', 'diagnosis', 'treatment', 'severity'),
            show='headings'
        )
        
        # Define columns
        self.history_tree.heading('id', text='ID', anchor=tk.W)
        self.history_tree.heading('date', text='Date', anchor=tk.W)
        self.history_tree.heading('diagnosis', text='Diagnosis', anchor=tk.W)
        self.history_tree.heading('treatment', text='Treatment', anchor=tk.W)
        self.history_tree.heading('severity', text='Severity', anchor=tk.W)
        
        # Set column widths
        self.history_tree.column('id', width=50, minwidth=50)
        self.history_tree.column('date', width=100, minwidth=100)
        self.history_tree.column('diagnosis', width=250, minwidth=250)
        self.history_tree.column('treatment', width=300, minwidth=300)
        self.history_tree.column('severity', width=80, minwidth=80)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.history_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.history_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double click to edit history entry
        self.history_tree.bind("<Double-1>", self.edit_medical_history)
    
    def create_appointment_list(self):
        """Create the treeview widget to display appointments"""
        # Create frame for treeview and scrollbars
        tree_frame = ttk.Frame(self.appointment_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create treeview
        self.appointment_tree = ttk.Treeview(
            tree_frame,
            columns=('id', 'date', 'time', 'patient', 'purpose', 'status'),
            show='headings'
        )
        
        # Define columns
        self.appointment_tree.heading('id', text='ID', anchor=tk.W)
        self.appointment_tree.heading('date', text='Date', anchor=tk.W)
        self.appointment_tree.heading('time', text='Time', anchor=tk.W)
        self.appointment_tree.heading('patient', text='Patient', anchor=tk.W)
        self.appointment_tree.heading('purpose', text='Purpose', anchor=tk.W)
        self.appointment_tree.heading('status', text='Status', anchor=tk.W)
        
        # Set column widths
        self.appointment_tree.column('id', width=50, minwidth=50)
        self.appointment_tree.column('date', width=100, minwidth=100)
        self.appointment_tree.column('time', width=100, minwidth=100)
        self.appointment_tree.column('patient', width=200, minwidth=200)
        self.appointment_tree.column('purpose', width=250, minwidth=250)
        self.appointment_tree.column('status', width=100, minwidth=100)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.appointment_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.appointment_tree.xview)
        self.appointment_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.appointment_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double click to edit appointment
        self.appointment_tree.bind("<Double-1>", self.edit_appointment)
    
    def refresh_patient_list(self, patients=None):
        """Refresh the patient list in the treeview"""
        if patients is None:
            patients = self.system.get_all_patients()
        
        # Clear current items
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        
        # Add new items
        for patient in patients:
            self.patient_tree.insert('', 'end', values=(
                patient['patient_id'],
                patient['last_name'],
                patient['first_name'],
                patient['date_of_birth'],
                patient['gender'],
                patient['last_visit_date'] or 'Never',
                patient['blood_type'] or 'Unknown'
            ))
        
        # Update patient combobox in history tab
        patient_options = [
            f"{p['patient_id']}: {p['last_name']}, {p['first_name']}" 
            for p in patients
        ]
        self.patient_combobox['values'] = patient_options
        
        self.update_status(f"Showing {len(patients)} patients")
    
    def refresh_history_list(self, patient_id=None):
        """Refresh the medical history list in the treeview"""
        if patient_id is None:
            # Clear the history list
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            return
        
        history_entries = self.system.get_medical_history(patient_id)
        
        # Clear current items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add new items
        for entry in history_entries:
            self.history_tree.insert('', 'end', values=(
                entry['history_id'],
                entry['entry_date'],
                entry['diagnosis'],
                (entry['treatment'] or '')[:100] + ('...' if len(entry['treatment'] or '') > 100 else ''),
                entry['severity'] or 'N/A'
            ))
        
        self.update_status(f"Showing {len(history_entries)} history entries for selected patient")
    
    def refresh_appointment_list(self, appointments=None):
        """Refresh the appointment list in the treeview"""
        if appointments is None:
            appointments = self.system.get_appointments()
        
        # Clear current items
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
        
        # Add new items
        for appt in appointments:
            self.appointment_tree.insert('', 'end', values=(
                appt['appointment_id'],
                appt['appointment_date'],
                f"{appt['start_time']} - {appt['end_time']}",
                f"{appt['last_name']}, {appt['first_name']}",
                appt['purpose'] or '',
                appt['status']
            ))
        
        self.update_status(f"Showing {len(appointments)} appointments")
    
    def on_search_changed(self, event=None):
        """Handle search text changes"""
        search_text = self.search_var.get().lower()
        search_by = self.search_by_var.get()
        
        if not search_text:
            self.refresh_patient_list()
            return
        
        all_patients = self.system.get_all_patients()
        filtered_patients = []
        
        for patient in all_patients:
            field_value = str(patient.get(search_by, '')).lower()
            if search_text in field_value:
                filtered_patients.append(patient)
        
        self.refresh_patient_list(filtered_patients)
    
    def on_patient_selected(self, event=None):
        """Handle patient selection in the history tab"""
        selection = self.patient_combobox.get()
        if not selection:
            return
        
        patient_id = int(selection.split(':')[0])
        self.refresh_history_list(patient_id)
    
    def filter_appointments_by_date(self):
        """Filter appointments by the selected date"""
        date_str = self.appointment_date_var.get()
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            appointments = self.system.get_appointments(date=date_str)
            self.refresh_appointment_list(appointments)
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
    
    def filter_appointments_by_status(self, *args):
        """Filter appointments by status"""
        status = self.status_filter_var.get()
        date_str = self.appointment_date_var.get()
        
        try:
            if status == "All":
                appointments = self.system.get_appointments(date=date_str if date_str else None)
            else:
                # Get all appointments and filter by status
                appointments = self.system.get_appointments(date=date_str if date_str else None)
                appointments = [a for a in appointments if a['status'] == status]
            
            self.refresh_appointment_list(appointments)
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
    
    def show_all_appointments(self):
        """Show all appointments regardless of date"""
        self.appointment_date_var.set("")
        appointments = self.system.get_appointments()
        self.refresh_appointment_list(appointments)
    
    def clear_search(self):
        """Clear the search box and reset the patient list"""
        self.search_var.set("")
        self.refresh_patient_list()
    
    # Sorting methods
    def sort_patients(self, key, reverse=False):
        """Sort patients by the specified key"""
        patients = self.system.get_all_patients()
        sorted_patients = self.system.quick_sort_patients(patients, key, reverse)
        self.refresh_patient_list(sorted_patients)
    
    def sort_medical_history(self, key, reverse=False):
        """Sort medical history by the specified key"""
        selection = self.patient_combobox.get()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a patient first")
            return
        
        patient_id = int(selection.split(':')[0])
        history_entries = self.system.get_medical_history(patient_id)
        sorted_history = self.system.heap_sort_medical_history(history_entries, key, reverse)
        self.refresh_history_list_with_data(sorted_history)
    
    def sort_appointments(self, key, reverse=False):
        """Sort appointments by the specified key"""
        appointments = self.system.get_appointments()
        sorted_appointments = self.system.merge_sort_appointments(appointments, key, reverse)
        self.refresh_appointment_list(sorted_appointments)
    
    def refresh_history_list_with_data(self, history_entries):
        """Refresh history list with provided data (used after sorting)"""
        # Clear current items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add new items
        for entry in history_entries:
            self.history_tree.insert('', 'end', values=(
                entry['history_id'],
                entry['entry_date'],
                entry['diagnosis'],
                (entry['treatment'] or '')[:100] + ('...' if len(entry['treatment'] or '') > 100 else ''),
                entry['severity'] or 'N/A'
            ))
    
    # Patient operations
    def get_selected_patient_id(self):
        """Get the ID of the currently selected patient"""
        selection = self.patient_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a patient first")
            return None
        
        selected_item = self.patient_tree.item(selection[0])
        return selected_item['values'][0]  # First value is patient_id
    
    def add_patient(self):
        """Open dialog to add a new patient"""
        dialog = PatientDialog(self.root, "Add New Patient")
        if dialog.result:
            patient_id = self.system.add_patient(**dialog.result)
            if patient_id:
                messagebox.showinfo("Success", f"Patient added successfully with ID {patient_id}")
                self.refresh_patient_list()
    
    def edit_patient(self, event=None):
        """Open dialog to edit selected patient"""
        patient_id = self.get_selected_patient_id()
        if patient_id is None:
            return
        
        patient = self.system.get_patient(patient_id)
        if not patient:
            messagebox.showerror("Error", "Could not retrieve patient data")
            return
        
        dialog = PatientDialog(self.root, "Edit Patient", **patient)
        if dialog.result:
            if self.system.update_patient(patient_id, **dialog.result):
                messagebox.showinfo("Success", "Patient updated successfully")
                self.refresh_patient_list()
    
    def delete_patient(self):
        """Delete the selected patient after confirmation"""
        patient_id = self.get_selected_patient_id()
        if patient_id is None:
            return
        
        if messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete patient ID {patient_id}? This cannot be undone."
        ):
            if self.system.delete_patient(patient_id):
                messagebox.showinfo("Success", "Patient deleted successfully")
                self.refresh_patient_list()
    
    def record_visit(self):
        """Record a visit for the selected patient"""
        patient_id = self.get_selected_patient_id()
        if patient_id is None:
            return
        
        if self.system.record_last_visit(patient_id):
            messagebox.showinfo("Success", "Visit recorded successfully")
            self.refresh_patient_list()
    
    # Medical History operations
    def get_selected_history_id(self):
        """Get the ID of the currently selected history entry"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a history entry first")
            return None
        
        selected_item = self.history_tree.item(selection[0])
        return selected_item['values'][0]  # First value is history_id
    
    def add_medical_history(self):
        """Open dialog to add a new medical history entry"""
        patient_id = self.get_selected_patient_id()
        if patient_id is None:
            return
        
        dialog = MedicalHistoryDialog(self.root, "Add Medical History Entry")
        if dialog.result:
            history_id = self.system.add_medical_history(patient_id, **dialog.result)
            if history_id:
                messagebox.showinfo("Success", "Medical history entry added successfully")
                self.refresh_history_list(patient_id)
    
    def edit_medical_history(self, event=None):
        """Open dialog to edit selected medical history entry"""
        history_id = self.get_selected_history_id()
        if history_id is None:
            return
        
        # Get the full history entry
        try:
            query = "SELECT * FROM medical_history WHERE history_id = %s"
            self.system.cursor.execute(query, (history_id,))
            result = self.system.cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "Could not retrieve history entry")
                return
            
            history_entry = self.system._format_medical_history(result)
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving history entry: {e}")
            return
        
        dialog = MedicalHistoryDialog(self.root, "Edit Medical History Entry", **history_entry)
        if dialog.result:
            if self.system.update_medical_history(history_id, **dialog.result):
                messagebox.showinfo("Success", "History entry updated successfully")
                
                # Refresh both lists since we might have changed dates that affect sorting
                patient_id = history_entry['patient_id']
                self.refresh_history_list(patient_id)
                
                # Also refresh patient list if we changed the last visit date
                if 'entry_date' in dialog.result:
                    self.refresh_patient_list()
    
    def delete_medical_history(self):
        """Delete the selected medical history entry after confirmation"""
        history_id = self.get_selected_history_id()
        if history_id is None:
            return
        
        if messagebox.askyesno(
            "Confirm Delete", 
            "Are you sure you want to delete this medical history entry? This cannot be undone."
        ):
            if self.system.delete_medical_history(history_id):
                messagebox.showinfo("Success", "History entry deleted successfully")
                
                # Get the patient ID to refresh the correct history
                selection = self.patient_combobox.get()
                if selection:
                    patient_id = int(selection.split(':')[0])
                    self.refresh_history_list(patient_id)
    
    # Appointment operations
    def get_selected_appointment_id(self):
        """Get the ID of the currently selected appointment"""
        selection = self.appointment_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an appointment first")
            return None
        
        selected_item = self.appointment_tree.item(selection[0])
        return selected_item['values'][0]  # First value is appointment_id
    
    def schedule_appointment(self):
        """Open dialog to schedule a new appointment"""
        patient_id = self.get_selected_patient_id()
        if patient_id is None:
            return
        
        dialog = AppointmentDialog(self.root, "Schedule Appointment")
        if dialog.result:
            appointment_id = self.system.add_appointment(patient_id, **dialog.result)
            if appointment_id:
                messagebox.showinfo("Success", "Appointment scheduled successfully")
                self.refresh_appointment_list()
    
    def edit_appointment(self, event=None):
        """Open dialog to edit selected appointment"""
        appointment_id = self.get_selected_appointment_id()
        if appointment_id is None:
            return
        
        # Get the full appointment details
        try:
            query = """
            SELECT * FROM appointments 
            WHERE appointment_id = %s
            """
            self.system.cursor.execute(query, (appointment_id,))
            result = self.system.cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "Could not retrieve appointment")
                return
            
            appointment = self.system._format_appointment(result)
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving appointment: {e}")
            return
        
        dialog = AppointmentDialog(self.root, "Edit Appointment", **appointment)
        if dialog.result:
            if self.system.update_appointment(appointment_id, **dialog.result):
                messagebox.showinfo("Success", "Appointment updated successfully")
                self.refresh_appointment_list()
    
    def cancel_appointment(self):
        """Cancel the selected appointment"""
        appointment_id = self.get_selected_appointment_id()
        if appointment_id is None:
            return
        
        if messagebox.askyesno(
            "Confirm Cancel", 
            "Are you sure you want to cancel this appointment?"
        ):
            if self.system.update_appointment(appointment_id, status='Cancelled'):
                messagebox.showinfo("Success", "Appointment cancelled successfully")
                self.refresh_appointment_list()
    
    def complete_appointment(self):
        """Mark the selected appointment as completed"""
        appointment_id = self.get_selected_appointment_id()
        if appointment_id is None:
            return
        
        if messagebox.askyesno(
            "Confirm Complete", 
            "Mark this appointment as completed?"
        ):
            if self.system.update_appointment(appointment_id, status='Completed'):
                messagebox.showinfo("Success", "Appointment marked as completed")
                self.refresh_appointment_list()
    
    def generate_sample_data(self):
        """Generate sample patient data"""
        if messagebox.askyesno(
            "Confirm", 
            "This will generate sample patient records with medical histories and appointments. Continue?"
        ):
            self.system.generate_sample_data()
            self.refresh_patient_list()
            self.refresh_appointment_list()
            messagebox.showinfo("Success", "Sample data generated successfully")
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_var.set(message)
    
    def on_closing(self):
        """Handle window closing event"""
        self.system.close()
        self.root.destroy()


class Patient(tk.Toplevel):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x500")
        self.resizable(False, False)
        
        self.result = None
        
        # Form fields
        ttk.Label(self, text="First Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.first_name_var = tk.StringVar(value=kwargs.get('first_name', ''))
        ttk.Entry(self, textvariable=self.first_name_var).grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Last Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.last_name_var = tk.StringVar(value=kwargs.get('last_name', ''))
        ttk.Entry(self, textvariable=self.last_name_var).grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Date of Birth (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.dob_var = tk.StringVar(value=kwargs.get('date_of_birth', ''))
        ttk.Entry(self, textvariable=self.dob_var).grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Gender:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.gender_var = tk.StringVar(value=kwargs.get('gender', 'Male'))
        ttk.Combobox(
            self, 
            textvariable=self.gender_var, 
            values=['Male', 'Female', 'Other'],
            state='readonly'
        ).grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Phone:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.phone_var = tk.StringVar(value=kwargs.get('phone', ''))
        ttk.Entry(self, textvariable=self.phone_var).grid(row=4, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Email:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        self.email_var = tk.StringVar(value=kwargs.get('email', ''))
        ttk.Entry(self, textvariable=self.email_var).grid(row=5, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Address:").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        self.address_var = tk.StringVar(value=kwargs.get('address', ''))
        ttk.Entry(self, textvariable=self.address_var).grid(row=6, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Blood Type:").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
        self.blood_type_var = tk.StringVar(value=kwargs.get('blood_type', ''))
        ttk.Combobox(
            self, 
            textvariable=self.blood_type_var, 
            values=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', ''],
            state='readonly'
        ).grid(row=7, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Save", 
            command=self.on_save
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Cancel", 
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Center the window
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
    
    def on_save(self):
        """Handle save button click"""
        # Validate required fields
        if not self.first_name_var.get():
            messagebox.showerror("Error", "First name is required")
            return
        
        if not self.last_name_var.get():
            messagebox.showerror("Error", "Last name is required")
            return
        
        if not self.dob_var.get():
            messagebox.showerror("Error", "Date of birth is required")
            return
        
        try:
            datetime.datetime.strptime(self.dob_var.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Date of birth must be in YYYY-MM-DD format")
            return
        
        # Prepare result dictionary
        self.result = {
            'first_name': self.first_name_var.get(),
            'last_name': self.last_name_var.get(),
            'date_of_birth': self.dob_var.get(),
            'gender': self.gender_var.get(),
            'phone': self.phone_var.get() or None,
            'email': self.email_var.get() or None,
            'address': self.address_var.get() or None,
            'blood_type': self.blood_type_var.get() or None
        }
        
        self.destroy()


class MedicalHistoryDialog(tk.Toplevel):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x400")
        self.resizable(False, False)
        
        self.result = None
        
        # Form fields
        ttk.Label(self, text="Entry Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.date_var = tk.StringVar(value=kwargs.get('entry_date', datetime.date.today()))
        ttk.Entry(self, textvariable=self.date_var).grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Diagnosis:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.diagnosis_var = tk.StringVar(value=kwargs.get('diagnosis', ''))
        ttk.Entry(self, textvariable=self.diagnosis_var).grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Treatment:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.treatment_var = tk.StringVar(value=kwargs.get('treatment', ''))
        ttk.Entry(self, textvariable=self.treatment_var).grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Notes:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.notes_text = tk.Text(self, width=40, height=5)
        self.notes_text.grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)
        if 'notes' in kwargs and kwargs['notes']:
            self.notes_text.insert('1.0', kwargs['notes'])
        
        ttk.Label(self, text="Severity (1-10):").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.severity_var = tk.StringVar(value=kwargs.get('severity', ''))
        ttk.Spinbox(
            self,
            from_=1,
            to=10,
            textvariable=self.severity_var
        ).grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Save", 
            command=self.on_save
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Cancel", 
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Center the window
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
    
    def on_save(self):
        """Handle save button click"""
        # Validate required fields
        if not self.date_var.get():
            messagebox.showerror("Error", "Entry date is required")
            return
        
        try:
            datetime.datetime.strptime(self.date_var.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Entry date must be in YYYY-MM-DD format")
            return
        
        if not self.diagnosis_var.get():
            messagebox.showerror("Error", "Diagnosis is required")
            return
        
        # Validate severity
        severity = None
        if self.severity_var.get():
            try:
                severity = int(self.severity_var.get())
                if not (1 <= severity <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Severity must be a number between 1 and 10")
                return
        
        # Prepare result dictionary
        self.result = {
            'entry_date': self.date_var.get(),
            'diagnosis': self.diagnosis_var.get(),
            'treatment': self.treatment_var.get() or None,
            'notes': self.notes_text.get('1.0', 'end-1c') or None,
            'severity': severity
        }
        
        self.destroy()


class AppointmentDialog(tk.Toplevel):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x400")
        self.resizable(False, False)
        
        self.result = None
        
        # Form fields
        ttk.Label(self, text="Appointment Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.date_var = tk.StringVar(value=kwargs.get('appointment_date', datetime.date.today()))
        ttk.Entry(self, textvariable=self.date_var).grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Start Time (HH:MM):").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.start_time_var = tk.StringVar(value=kwargs.get('start_time', '09:00'))
        ttk.Entry(self, textvariable=self.start_time_var).grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="End Time (HH:MM):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.end_time_var = tk.StringVar(value=kwargs.get('end_time', '09:30'))
        ttk.Entry(self, textvariable=self.end_time_var).grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Purpose:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.purpose_var = tk.StringVar(value=kwargs.get('purpose', ''))
        ttk.Entry(self, textvariable=self.purpose_var).grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Status:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.status_var = tk.StringVar(value=kwargs.get('status', 'Scheduled'))
        ttk.Combobox(
            self,
            textvariable=self.status_var,
            values=['Scheduled', 'Completed', 'Cancelled', 'No-show'],
            state='readonly'
        ).grid(row=4, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Notes:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        self.notes_text = tk.Text(self, width=40, height=5)
        self.notes_text.grid(row=5, column=1, padx=10, pady=5, sticky=tk.EW)
        if 'notes' in kwargs and kwargs['notes']:
            self.notes_text.insert('1.0', kwargs['notes'])
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Save", 
            command=self.on_save
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Cancel", 
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Center the window
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
    
    def on_save(self):
        """Handle save button click"""
        # Validate required fields
        if not self.date_var.get():
            messagebox.showerror("Error", "Appointment date is required")
            return
        
        try:
            datetime.datetime.strptime(self.date_var.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Appointment date must be in YYYY-MM-DD format")
            return
        
        if not self.start_time_var.get():
            messagebox.showerror("Error", "Start time is required")
            return
        
        try:
            datetime.datetime.strptime(self.start_time_var.get(), '%H:%M')
        except ValueError:
            messagebox.showerror("Error", "Start time must be in HH:MM format")
            return
        
        if not self.end_time_var.get():
            messagebox.showerror("Error", "End time is required")
            return
        
        try:
            datetime.datetime.strptime(self.end_time_var.get(), '%H:%M')
        except ValueError:
            messagebox.showerror("Error", "End time must be in HH:MM format")
            return
        
        # Prepare result dictionary
        self.result = {
            'appointment_date': self.date_var.get(),
            'start_time': self.start_time_var.get(),
            'end_time': self.end_time_var.get(),
            'purpose': self.purpose_var.get() or None,
            'status': self.status_var.get(),
            'notes': self.notes_text.get('1.0', 'end-1c') or None
        }
        
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MediTrackGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()