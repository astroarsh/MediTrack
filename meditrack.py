import csv
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import uuid
from datetime import datetime

class CSVManager:
    @staticmethod
    def create_csv_files():
        files = {
            "patients.csv": ["Patient ID", "Name", "DOB", "Gender", "Contact", "Address", "Blood Type", "Allergies"],
            "appointments.csv": ["Appointment ID", "Patient ID", "Patient Name", "Doctor ID", "Doctor Name", "Date", "Time", "Reason", "Status"],
            "doctors.csv": ["Doctor ID", "Name", "Specialization", "Contact No.", "License Number"],
            "billing.csv": ["Invoice ID", "Patient ID", "Patient Name", "Amount", "Payment Method", "Status", "Date"],
            "prescriptions.csv": ["Prescription ID", "Patient ID", "Patient Name", "Doctor ID", "Doctor Name", 
                                 "Medication", "Dosage", "Instructions", "Issue Date", "Expiry Date"],
            "medical_records.csv": ["Record ID", "Patient ID", "Patient Name", "Doctor ID", "Doctor Name", 
                                   "Visit Date", "Diagnosis", "Treatment", "Notes", "Follow Up"],
            "admin.csv": ["Username", "Password"],
            "doctor_login.csv": ["Doctor ID", "Password"],
            "patient_login.csv": ["Patient ID", "Password"]
        }

        for filename, headers in files.items():
            if not os.path.exists(filename):
                with open(filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    if filename == "admin.csv":
                        writer.writerow(["admin1", "admin"])  # Default admin credentials
                    elif filename == "patient_login.csv":
                        writer.writerow(["1001", "patient1"])  # Default patient credentials

class BackgroundManager:
    @staticmethod
    def set_background(window, background_image=None):
        if background_image:
            bg_photo = ImageTk.PhotoImage(background_image)
            bg_canvas = tk.Canvas(window, width=800, height=600)
            bg_canvas.pack(fill="both", expand=True)
            bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")
            bg_canvas.image = bg_photo
            return bg_canvas
        return None

class SearchSortManager:
    @staticmethod
    def bubble_sort(data, sort_key, ascending=True):
        """Bubble sort implementation for sorting data"""     #arshdeep's code
        n = len(data)            
        for i in range(n):
            for j in range(0, n-i-1):
                # Handle numeric values differently from strings
                try:
                    val1 = float(data[j][sort_key])
                    val2 = float(data[j+1][sort_key])
                except (ValueError, KeyError):
                    val1 = str(data[j][sort_key]).lower()
                    val2 = str(data[j+1][sort_key]).lower()
                
                if ascending:
                    if val1 > val2:
                        data[j], data[j+1] = data[j+1], data[j]
                else:
                    if val1 < val2:
                        data[j], data[j+1] = data[j+1], data[j]
        return data

    @staticmethod
    def linear_search(data, search_key, search_value):
        """Linear search implementation to find matching records"""
        results = []             #arshdeep's code
        for record in data:
            if str(search_value).lower() in str(record.get(search_key, '')).lower():
                results.append(record)
        return results

class LoginManager:
    @staticmethod
    def verify_login(username, password, file_name):
        try:
            with open(file_name, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if username == row[0].strip() and password == row[1].strip():
                        return True
            return False
        except Exception as e:
            messagebox.showerror("Login Error", f"Error: {e}")
            return False

class PatientManager:
    @staticmethod
    def register_patient(name, dob, gender, contact, address, blood_type, allergies):
        try:
            patient_id = str(uuid.uuid4())[:8]
            patient_data = [patient_id, name, dob, gender, contact, address, blood_type, allergies]
            
            with open("patients.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(patient_data)
            
            with open("patient_login.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([patient_id, patient_id])  # Using patient ID as initial password
            
            messagebox.showinfo("Success", f"Patient registered successfully!\nPatient ID: {patient_id}")
            return True
        except Exception as e:
            messagebox.showerror("Registration Error", f"Error: {e}")
            return False

    @staticmethod
    def view_all_patients():
        try:
            patients = []
            with open("patients.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    patients.append(row)
            return patients
        except Exception as e:
            messagebox.showerror("View Error", f"Error: {e}")
            return []

    @staticmethod
    def delete_patient(patient_id):
        try:
            # Delete from patients.csv
            updated_patients = []
            with open("patients.csv", mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                updated_patients.append(headers)
                for row in reader:
                    if row[0] != patient_id:
                        updated_patients.append(row)
            
            with open("patients.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_patients)
            
            # Delete from patient_login.csv
            updated_logins = []
            with open("patient_login.csv", mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                updated_logins.append(headers)
                for row in reader:
                    if row[0] != patient_id:
                        updated_logins.append(row)
            
            with open("patient_login.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_logins)
            
            messagebox.showinfo("Success", f"Patient {patient_id} deleted successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Delete Error", f"Error: {e}")
            return False

    @staticmethod
    def get_patient_details(patient_id):
        try:
            with open("patients.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Patient ID'] == patient_id:
                        return row
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch patient details: {e}")
            return None

class DoctorManager:
    @staticmethod
    def add_doctor(name, specialization, contact, license_no):
        try:
            doctor_id = str(uuid.uuid4())[:8]
            doctor_data = [doctor_id, name, specialization, contact, license_no]
            
            with open("doctors.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(doctor_data)
            
            with open("doctor_login.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([doctor_id, doctor_id])  # Using doctor ID as initial password
            
            messagebox.showinfo("Success", f"Doctor added successfully!\nDoctor ID: {doctor_id}")
            return True
        except Exception as e:
            messagebox.showerror("Doctor Registration Error", f"Error: {e}")
            return False

    @staticmethod
    def view_all_doctors():
        try:
            doctors = []
            with open("doctors.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    doctors.append(row)
            return doctors
        except Exception as e:
            messagebox.showerror("View Error", f"Error: {e}")
            return []

    @staticmethod
    def delete_doctor(doctor_id):
        try:
            # Delete from doctors.csv
            updated_doctors = []
            with open("doctors.csv", mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                updated_doctors.append(headers)
                for row in reader:
                    if row[0] != doctor_id:
                        updated_doctors.append(row)
            
            with open("doctors.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_doctors)
            
            # Delete from doctor_login.csv
            updated_logins = []
            with open("doctor_login.csv", mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                updated_logins.append(headers)
                for row in reader:
                    if row[0] != doctor_id:
                        updated_logins.append(row)
            
            with open("doctor_login.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_logins)
            
            messagebox.showinfo("Success", f"Doctor {doctor_id} deleted successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Delete Error", f"Error: {e}")
            return False

    @staticmethod
    def get_doctor_details(doctor_id):
        try:
            with open("doctors.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Doctor ID'] == doctor_id:
                        return row
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch doctor details: {e}")
            return None

class AppointmentManager:      #arshdeep's code
    @staticmethod
    def make_appointment(patient_id, patient_name, doctor_id, doctor_name, date, time, reason):
        try:
            appointment_id = str(uuid.uuid4())[:8]
            appointment_data = [appointment_id, patient_id, patient_name, doctor_id, doctor_name, 
                               date, time, reason, "Scheduled"]
            
            with open("appointments.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(appointment_data)
            
            messagebox.showinfo("Success", f"Appointment booked successfully!\nAppointment ID: {appointment_id}")
            return True
        except Exception as e:
            messagebox.showerror("Booking Error", f"Error: {e}")
            return False

    @staticmethod
    def view_appointments(patient_id=None, doctor_id=None):
        try:
            appointments = []
            with open("appointments.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if patient_id and row['Patient ID'] == patient_id:
                        appointments.append(row)
                    elif doctor_id and row['Doctor ID'] == doctor_id:
                        appointments.append(row)
                    elif not patient_id and not doctor_id:
                        appointments.append(row)
            return appointments
        except Exception as e:
            messagebox.showerror("View Error", f"Error: {e}")
            return []

    @staticmethod
    def delete_appointment(appointment_id):
        try:
            updated_rows = []
            with open("appointments.csv", mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                updated_rows.append(headers)
                for row in reader:
                    if row[0] != appointment_id:
                        updated_rows.append(row)
            
            with open("appointments.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            
            messagebox.showinfo("Success", f"Appointment {appointment_id} deleted successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Delete Error", f"Error: {e}")
            return False

    @staticmethod
    def update_appointment_status(appointment_id, new_status):
        try:
            updated_rows = []
            with open("appointments.csv", mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                updated_rows.append(headers)
                for row in reader:
                    if row[0] == appointment_id:
                        row[8] = new_status  # Update status
                    updated_rows.append(row)
            
            with open("appointments.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            
            return True
        except Exception as e:
            messagebox.showerror("Update Error", f"Error: {e}")
            return False

class PrescriptionManager:
    @staticmethod
    def create_prescription(patient_id, patient_name, doctor_id, doctor_name, 
                           medication, dosage, instructions, issue_date, expiry_date):
        try:
            prescription_id = str(uuid.uuid4())[:8]
            prescription_data = [prescription_id, patient_id, patient_name, doctor_id, doctor_name,
                               medication, dosage, instructions, issue_date, expiry_date]
            
            with open("prescriptions.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(prescription_data)
            
            messagebox.showinfo("Success", f"Prescription created successfully!\nPrescription ID: {prescription_id}")
            return True
        except Exception as e:
            messagebox.showerror("Prescription Error", f"Error: {e}")
            return False

    @staticmethod
    def view_prescriptions(patient_id=None, doctor_id=None):
        try:
            prescriptions = []
            with open("prescriptions.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if patient_id and row['Patient ID'] == patient_id:
                        prescriptions.append(row)
                    elif doctor_id and row['Doctor ID'] == doctor_id:
                        prescriptions.append(row)
                    elif not patient_id and not doctor_id:
                        prescriptions.append(row)
            return prescriptions
        except Exception as e:
            messagebox.showerror("View Error", f"Error: {e}")
            return []

    @staticmethod
    def delete_prescription(prescription_id):
        try:
            updated_rows = []
            with open("prescriptions.csv", mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                updated_rows.append(headers)
                for row in reader:
                    if row[0] != prescription_id:
                        updated_rows.append(row)
            
            with open("prescriptions.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            
            messagebox.showinfo("Success", f"Prescription {prescription_id} deleted successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Delete Error", f"Error: {e}")
            return False

class MedicalRecordManager:
    @staticmethod
    def create_record(patient_id, patient_name, doctor_id, doctor_name, 
                     visit_date, diagnosis, treatment, notes, follow_up):
        try:
            record_id = str(uuid.uuid4())[:8]
            record_data = [record_id, patient_id, patient_name, doctor_id, doctor_name,
                          visit_date, diagnosis, treatment, notes, follow_up]
            
            with open("medical_records.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(record_data)
            
            messagebox.showinfo("Success", f"Medical record created successfully!\nRecord ID: {record_id}")
            return True
        except Exception as e:
            messagebox.showerror("Record Error", f"Error: {e}")
            return False

    @staticmethod
    def view_records(patient_id=None, doctor_id=None):
        try:
            records = []
            with open("medical_records.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if patient_id and row['Patient ID'] == patient_id:
                        records.append(row)
                    elif doctor_id and row['Doctor ID'] == doctor_id:
                        records.append(row)
                    elif not patient_id and not doctor_id:
                        records.append(row)
            return records
        except Exception as e:
            messagebox.showerror("View Error", f"Error: {e}")
            return []

    @staticmethod
    def delete_record(record_id):
        try:
            updated_rows = []
            with open("medical_records.csv", mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                updated_rows.append(headers)
                for row in reader:
                    if row[0] != record_id:
                        updated_rows.append(row)
            
            with open("medical_records.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            
            messagebox.showinfo("Success", f"Medical record {record_id} deleted successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Delete Error", f"Error: {e}")
            return False

class PaymentManager:
    @staticmethod
    def process_payment(patient_id, patient_name, amount, method):
        try:
            invoice_id = str(uuid.uuid4())[:8]
            payment_date = datetime.now().strftime("%Y-%m-%d")
            payment_data = [invoice_id, patient_id, patient_name, amount, method, "Paid", payment_date]
            
            with open("billing.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(payment_data)
            
            messagebox.showinfo("Payment", f"Payment processed successfully!\nInvoice ID: {invoice_id}")
            return True
        except Exception as e:
            messagebox.showerror("Payment Error", f"Error: {e}")
            return False

    @staticmethod
    def view_payments(patient_id=None):
        try:
            payments = []
            with open("billing.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if patient_id and row['Patient ID'] == patient_id:
                        payments.append(row)
                    elif not patient_id:
                        payments.append(row)
            return payments
        except Exception as e:
            messagebox.showerror("View Error", f"Error: {e}")
            return []

class MediTrackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MediTrack Healthcare System")
        self.root.geometry("800x600")
        self.current_user_id = None
        self.current_user_type = None
        self.current_patient_name = None

        # Load background image
        try:
            self.background_image = Image.open("meditrack1.jpg")
            self.background_image = self.background_image.resize((800, 600), Image.LANCZOS)
        except FileNotFoundError:
            messagebox.showerror("Error", "Background image 'meditrack1.jpg' not found!")
            self.background_image = None

        CSVManager.create_csv_files()
        self.create_home_screen()

    def create_home_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        bg_canvas = BackgroundManager.set_background(self.root, self.background_image)

        button_frame = tk.Frame(self.root, bg='white', bd=10, relief=tk.RAISED)
        if bg_canvas:
            bg_canvas.create_window(400, 300, window=button_frame)
        else:
            button_frame.pack(expand=True, fill='both')

        tk.Label(button_frame, text="MediTrack Healthcare System",
                 font=("Arial", 24, "bold"),
                 fg="navy",
                 bg='white').pack(pady=20)

        buttons = [
            ("Admin Login", lambda: self.login_screen("Admin Login", "admin.csv", "admin")),
            ("Doctor Login", lambda: self.login_screen("Doctor Login", "doctor_login.csv", "doctor")),
            ("Patient Login", lambda: self.login_screen("Patient Login", "patient_login.csv", "patient"))
        ]

        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                width=20,
                height=2,
                font=("Arial", 14),
                bg="navy",
                fg="white",
                activebackground="darkblue",
                activeforeground="white"
            )
            btn.pack(pady=10)

    def login_screen(self, title, file_name, user_type):
        login_window = tk.Toplevel(self.root)
        login_window.title(title)
        login_window.geometry("500x400")

        bg_canvas = BackgroundManager.set_background(login_window, self.background_image)

        login_frame = tk.Frame(login_window, bg='white', bd=10, relief=tk.RAISED)
        if bg_canvas:
            bg_canvas.create_window(250, 200, window=login_frame)
        else:
            login_frame.pack(expand=True, fill='both')

        tk.Label(login_frame, text=title, font=("Arial", 20, "bold"),
                 fg="navy", bg='white').pack(pady=20)

        username_label = tk.Label(login_frame, text="Username:",
                                  font=("Arial", 12),
                                  fg="navy",
                                  bg='white')
        username_label.pack()
        username_entry = tk.Entry(login_frame, font=("Arial", 12), width=30)
        username_entry.pack(pady=5)

        password_label = tk.Label(login_frame, text="Password:",
                                  font=("Arial", 12),
                                  fg="navy",
                                  bg='white')
        password_label.pack()
        password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12), width=30)
        password_entry.pack(pady=5)

        def verify():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if LoginManager.verify_login(username, password, file_name):
                messagebox.showinfo("Login Success", f"Welcome {title.split()[0]}!")
                self.current_user_id = username
                self.current_user_type = user_type
                
                # Get patient name if patient
                if user_type == "patient":
                    patient_details = PatientManager.get_patient_details(username)
                    if patient_details:
                        self.current_patient_name = patient_details['Name']
                
                login_window.destroy()
                
                if user_type == "admin":
                    self.admin_section()
                elif user_type == "doctor":
                    self.doctor_dashboard()
                elif user_type == "patient":
                    self.patient_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials!")

        login_btn = tk.Button(login_frame, text="Login",
                              command=verify,
                              font=("Arial", 14),
                              bg="navy",
                              fg="white",
                              activebackground="darkblue",
                              activeforeground="white",
                              width=20)
        login_btn.pack(pady=20)

    def admin_section(self):
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Panel")
        admin_window.geometry("1000x700")

        bg_canvas = BackgroundManager.set_background(admin_window, self.background_image)

        admin_frame = tk.Frame(admin_window, bg='white', bd=10, relief=tk.RAISED)
        if bg_canvas:
            bg_canvas.create_window(500, 350, window=admin_frame)
        else:
            admin_frame.pack(expand=True, fill='both')

        tk.Label(admin_frame, text="Admin Panel",
                 font=("Arial", 24, "bold"),
                 fg="navy",
                 bg='white').pack(pady=20)

        # Create a frame for the button grid
        button_grid_frame = tk.Frame(admin_frame, bg='white')
        button_grid_frame.pack(pady=20)

        # First row of buttons
        row1_frame = tk.Frame(button_grid_frame, bg='white')
        row1_frame.pack(pady=5)

        btn1 = tk.Button(
            row1_frame,
            text="Register New Patient",
            command=self.register_patient,
            font=("Arial", 12),
            bg="navy",
            fg="white",
            width=20,
            height=2,
            activebackground="darkblue",
            activeforeground="white"
        )
        btn1.pack(side=tk.LEFT, padx=5)

        btn2 = tk.Button(
            row1_frame,
            text="Patient Management",
            command=self.patient_management_menu,
            font=("Arial", 12),
            bg="navy",
            fg="white",
            width=20,
            height=2,
            activebackground="darkblue",
            activeforeground="white"
        )
        btn2.pack(side=tk.LEFT, padx=5)

        btn3 = tk.Button(
            row1_frame,
            text="Doctor Management",
            command=self.doctor_management_menu,
            font=("Arial", 12),
            bg="navy",
            fg="white",
            width=20,
            height=2,
            activebackground="darkblue",
            activeforeground="white"
        )
        btn3.pack(side=tk.LEFT, padx=5)

        # Second row of buttons
        row2_frame = tk.Frame(button_grid_frame, bg='white')
        row2_frame.pack(pady=5)

        btn4 = tk.Button(
            row2_frame,
            text="Appointment Management",
            command=self.appointment_management_menu,
            font=("Arial", 12),
            bg="navy",
            fg="white",
            width=20,
            height=2,
            activebackground="darkblue",
            activeforeground="white"
        )
        btn4.pack(side=tk.LEFT, padx=5)

        btn5 = tk.Button(
            row2_frame,
            text="Prescription Management",
            command=self.prescription_management_menu,
            font=("Arial", 12),
            bg="navy",
            fg="white",
            width=20,
            height=2,
            activebackground="darkblue",
            activeforeground="white"
        )
        btn5.pack(side=tk.LEFT, padx=5)

        btn6 = tk.Button(
            row2_frame,
            text="Medical Records",
            command=self.medical_records_menu,
            font=("Arial", 12),
            bg="navy",
            fg="white",
            width=20,
            height=2,
            activebackground="darkblue",
            activeforeground="white"
        )
        btn6.pack(side=tk.LEFT, padx=5)

        # Third row of buttons
        row3_frame = tk.Frame(button_grid_frame, bg='white')
        row3_frame.pack(pady=5)

        btn7 = tk.Button(
            row3_frame,
            text="Billing & Payments",
            command=self.billing_payments_menu,
            font=("Arial", 12),
            bg="navy",
            fg="white",
            width=20,
            height=2,
            activebackground="darkblue",
            activeforeground="white"
        )
        btn7.pack(side=tk.LEFT, padx=5)

        # Logout and Close buttons
        btn_frame = tk.Frame(admin_frame, bg='white')
        btn_frame.pack(pady=20)

        logout_btn = tk.Button(
            btn_frame,
            text="Logout",
            command=admin_window.destroy,
            width=15,
            height=2,
            font=("Arial", 12),
            bg="red",
            fg="white",
            activebackground="darkred",
            activeforeground="white"
        )
        logout_btn.pack(side=tk.LEFT, padx=10)

        close_btn = tk.Button(
            btn_frame,
            text="Close",
            command=admin_window.destroy,
            width=15,
            height=2,
            font=("Arial", 12),
            bg="gray",
            fg="white",
            activebackground="darkgray",
            activeforeground="white"
        )
        close_btn.pack(side=tk.LEFT)

    def patient_management_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Patient Management")
        menu_window.geometry("400x300")

        tk.Label(menu_window, text="Patient Management", font=("Arial", 16)).pack(pady=10)

        buttons = [
            ("View All Patients", self.view_all_patients),
            ("Search Patients", self.search_patients),
            ("Delete Patient", self.delete_patient),
            ("Back", menu_window.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                menu_window,
                text=text,
                command=command,
                width=20,
                height=2,
                font=("Arial", 12),
                bg="navy",
                fg="white"
            )
            btn.pack(pady=5)

    def doctor_management_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Doctor Management")
        menu_window.geometry("400x300")

        tk.Label(menu_window, text="Doctor Management", font=("Arial", 16)).pack(pady=10)

        buttons = [
            ("Add New Doctor", self.add_new_doctor),
            ("View All Doctors", self.view_all_doctors),
            ("Search Doctors", self.search_doctors),
            ("Delete Doctor", self.delete_doctor),
            ("Back", menu_window.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                menu_window,
                text=text,
                command=command,
                width=20,
                height=2,
                font=("Arial", 12),
                bg="navy",
                fg="white"
            )
            btn.pack(pady=5)

    def appointment_management_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Appointment Management")
        menu_window.geometry("400x300")

        tk.Label(menu_window, text="Appointment Management", font=("Arial", 16)).pack(pady=10)

        buttons = [
            ("View All Appointments", self.view_all_appointments),
            ("Search Appointments", self.search_appointments),
            ("Delete Appointment", self.delete_appointment),
            ("Update Status", self.update_appointment_status),
            ("Back", menu_window.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                menu_window,
                text=text,
                command=command,
                width=20,
                height=2,
                font=("Arial", 12),
                bg="navy",
                fg="white"
            )
            btn.pack(pady=5)

    def prescription_management_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Prescription Management")
        menu_window.geometry("400x300")

        tk.Label(menu_window, text="Prescription Management", font=("Arial", 16)).pack(pady=10)

        buttons = [
            ("View All Prescriptions", self.view_all_prescriptions),
            ("Search Prescriptions", self.search_prescriptions),
            ("Delete Prescription", self.delete_prescription),
            ("Back", menu_window.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                menu_window,
                text=text,
                command=command,
                width=20,
                height=2,
                font=("Arial", 12),
                bg="navy",
                fg="white"
            )
            btn.pack(pady=5)

    def medical_records_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Medical Records Management")
        menu_window.geometry("400x300")

        tk.Label(menu_window, text="Medical Records", font=("Arial", 16)).pack(pady=10)

        buttons = [
            ("View All Records", self.view_all_medical_records),
            ("Search Records", self.search_medical_records),
            ("Delete Record", self.delete_medical_record),
            ("Back", menu_window.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                menu_window,
                text=text,
                command=command,
                width=20,
                height=2,
                font=("Arial", 12),
                bg="navy",
                fg="white"
            )
            btn.pack(pady=5)

    def billing_payments_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Billing & Payments")
        menu_window.geometry("400x300")

        tk.Label(menu_window, text="Billing & Payments", font=("Arial", 16)).pack(pady=10)

        buttons = [
            ("View All Payments", self.view_all_payments),
            ("Search Payments", self.search_payments),
            ("Process Payment", self.process_payment),
            ("Back", menu_window.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                menu_window,
                text=text,
                command=command,
                width=20,
                height=2,
                font=("Arial", 12),
                bg="navy",
                fg="white"
            )
            btn.pack(pady=5)

    def register_patient(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Register New Patient")
        reg_window.geometry("600x600")

        tk.Label(reg_window, text="Patient Registration", font=("Arial", 20)).pack(pady=10)

        fields = [
            ("Name:", "name"),
            ("Date of Birth:", "dob"),
            ("Gender:", "gender"),
            ("Contact:", "contact"),
            ("Address:", "address"),
            ("Blood Type:", "blood_type"),
            ("Allergies:", "allergies")
        ]

        entries = {}
        for label_text, field_name in fields:
            tk.Label(reg_window, text=label_text).pack()
            
            if field_name == "dob":
                entry = DateEntry(reg_window, width=12, background='darkblue', foreground='white')
            elif field_name == "gender":
                entry = ttk.Combobox(reg_window, values=["Male", "Female", "Other"], state="readonly")
            elif field_name == "blood_type":
                entry = ttk.Combobox(reg_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], state="readonly")
            else:
                entry = tk.Entry(reg_window, width=40)
            
            entry.pack(pady=5)
            entries[field_name] = entry

        def submit_registration():
            values = {k: v.get() if hasattr(v, 'get') else v.get_date() for k, v in entries.items()}
            
            if all(values.values()):
                PatientManager.register_patient(
                    values['name'], 
                    values['dob'], 
                    values['gender'], 
                    values['contact'], 
                    values['address'],
                    values['blood_type'],
                    values['allergies']
                )
                reg_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill all fields")

        tk.Button(reg_window, text="Register", command=submit_registration).pack(pady=10)

    def view_all_patients(self):
        patients = PatientManager.view_all_patients()
        if patients:
            patients_window = tk.Toplevel(self.root)
            patients_window.title("All Patients")
            patients_window.geometry("1000x600")

            tree = ttk.Treeview(patients_window, columns=("ID", "Name", "DOB", "Gender", "Contact", "Address", "Blood Type", "Allergies"), show="headings")
            
            headings = ["Patient ID", "Name", "Date of Birth", "Gender", "Contact", "Address", "Blood Type", "Allergies"]
            for i, heading in enumerate(headings):
                tree.heading(tree['columns'][i], text=heading)
                tree.column(tree['columns'][i], width=120, anchor='center')

            for patient in patients:
                tree.insert("", tk.END, values=(
                    patient['Patient ID'],
                    patient['Name'],
                    patient['DOB'],
                    patient['Gender'],
                    patient['Contact'],
                    patient['Address'],
                    patient['Blood Type'],
                    patient['Allergies']
                ))

            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(patients_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            messagebox.showinfo("Patients", "No patients found.")

    def search_patients(self):
        patients = PatientManager.view_all_patients()
        if patients:
            search_window = tk.Toplevel(self.root)
            search_window.title("Search Patients")
            search_window.geometry("500x300")

            tk.Label(search_window, text="Search Patients", font=("Arial", 16)).pack(pady=10)

            tk.Label(search_window, text="Search Field:").pack()
            search_field = ttk.Combobox(search_window, 
                                      values=["Patient ID", "Name", "Gender", "Blood Type"],
                                      state="readonly")
            search_field.pack(pady=5)
            search_field.set("Name")

            tk.Label(search_window, text="Search Term:").pack()
            search_entry = tk.Entry(search_window, width=40)
            search_entry.pack(pady=5)

            def perform_search():
                field = search_field.get()
                term = search_entry.get().strip()
                
                if term:
                    results = SearchSortManager.linear_search(patients, field, term)
                    if results:
                        result_window = tk.Toplevel(search_window)
                        result_window.title("Search Results")
                        result_window.geometry("1000x400")

                        tree = ttk.Treeview(result_window, columns=("ID", "Name", "DOB", "Gender", "Contact"), show="headings")
                        
                        headings = ["Patient ID", "Name", "Date of Birth", "Gender", "Contact"]
                        for i, heading in enumerate(headings):
                            tree.heading(tree['columns'][i], text=heading)
                            tree.column(tree['columns'][i], width=120, anchor='center')

                        for patient in results:
                            tree.insert("", tk.END, values=(
                                patient['Patient ID'],
                                patient['Name'],
                                patient['DOB'],
                                patient['Gender'],
                                patient['Contact']
                            ))

                        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                        scrollbar = ttk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree.yview)
                        tree.configure(yscroll=scrollbar.set)
                        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    else:
                        messagebox.showinfo("No Results", "No patients found matching your search criteria.")
                else:
                    messagebox.showwarning("Empty Search", "Please enter a search term.")

            tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)
        else:
            messagebox.showinfo("Patients", "No patients to search.")

    def delete_patient(self):
        patients = PatientManager.view_all_patients()
        if patients:
            delete_window = tk.Toplevel(self.root)
            delete_window.title("Delete Patient")
            delete_window.geometry("400x300")

            tk.Label(delete_window, text="Select Patient to Delete:").pack(pady=10)
            
            patient_ids = [f"{patient['Patient ID']} - {patient['Name']}" for patient in patients]
            patient_combobox = ttk.Combobox(delete_window, values=patient_ids, state="readonly")
            patient_combobox.pack(pady=10)

            def confirm_delete():
                selected = patient_combobox.get()
                if selected:
                    patient_id = selected.split(" - ")[0]
                    if PatientManager.delete_patient(patient_id):
                        delete_window.destroy()

            tk.Button(delete_window, text="Delete", command=confirm_delete).pack(pady=10)
        else:
            messagebox.showinfo("Patients", "No patients to delete.")

    def add_new_doctor(self):
        doctor_window = tk.Toplevel(self.root)
        doctor_window.title("Add New Doctor")
        doctor_window.geometry("500x500")

        tk.Label(doctor_window, text="Doctor Registration", font=("Arial", 20)).pack(pady=10)

        tk.Label(doctor_window, text="Name:").pack()
        name_entry = tk.Entry(doctor_window, width=40)
        name_entry.pack(pady=5)

        tk.Label(doctor_window, text="Specialization:").pack()
        specialization_entry = tk.Entry(doctor_window, width=40)
        specialization_entry.pack(pady=5)

        tk.Label(doctor_window, text="Contact No.:").pack()
        contact_entry = tk.Entry(doctor_window, width=40)
        contact_entry.pack(pady=5)

        tk.Label(doctor_window, text="License Number:").pack()
        license_entry = tk.Entry(doctor_window, width=40)
        license_entry.pack(pady=5)

        def submit_doctor():
            name = name_entry.get()
            specialization = specialization_entry.get()
            contact = contact_entry.get()
            license_no = license_entry.get()

            if name and specialization and contact and license_no:
                DoctorManager.add_doctor(name, specialization, contact, license_no)
                doctor_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill all fields")

        tk.Button(doctor_window, text="Register Doctor", command=submit_doctor).pack(pady=10)

    def view_all_doctors(self):
        doctors = DoctorManager.view_all_doctors()
        if doctors:
            doctors_window = tk.Toplevel(self.root)
            doctors_window.title("All Doctors")
            doctors_window.geometry("1000x600")

            tree = ttk.Treeview(doctors_window, columns=("ID", "Name", "Specialization", "Contact", "License"), show="headings")
            
            headings = ["Doctor ID", "Name", "Specialization", "Contact", "License Number"]
            for i, heading in enumerate(headings):
                tree.heading(tree['columns'][i], text=heading)
                tree.column(tree['columns'][i], width=180, anchor='center')

            for doctor in doctors:
                tree.insert("", tk.END, values=(
                    doctor['Doctor ID'],
                    doctor['Name'],
                    doctor['Specialization'],
                    doctor['Contact No.'],
                    doctor['License Number']
                ))

            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(doctors_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            messagebox.showinfo("Doctors", "No doctors found.")

    def search_doctors(self):
        doctors = DoctorManager.view_all_doctors()
        if doctors:
            search_window = tk.Toplevel(self.root)
            search_window.title("Search Doctors")
            search_window.geometry("500x300")

            tk.Label(search_window, text="Search Doctors", font=("Arial", 16)).pack(pady=10)

            tk.Label(search_window, text="Search Field:").pack()
            search_field = ttk.Combobox(search_window, 
                                      values=["Doctor ID", "Name", "Specialization"],
                                      state="readonly")
            search_field.pack(pady=5)
            search_field.set("Name")

            tk.Label(search_window, text="Search Term:").pack()
            search_entry = tk.Entry(search_window, width=40)
            search_entry.pack(pady=5)

            def perform_search():
                field = search_field.get()
                term = search_entry.get().strip()
                
                if term:
                    results = SearchSortManager.linear_search(doctors, field, term)
                    if results:
                        result_window = tk.Toplevel(search_window)
                        result_window.title("Search Results")
                        result_window.geometry("800x400")

                        tree = ttk.Treeview(result_window, columns=("ID", "Name", "Specialization", "Contact"), show="headings")
                        
                        headings = ["Doctor ID", "Name", "Specialization", "Contact"]
                        for i, heading in enumerate(headings):
                            tree.heading(tree['columns'][i], text=heading)
                            tree.column(tree['columns'][i], width=120, anchor='center')

                        for doctor in results:
                            tree.insert("", tk.END, values=(
                                doctor['Doctor ID'],
                                doctor['Name'],
                                doctor['Specialization'],
                                doctor['Contact No.']
                            ))

                        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                        scrollbar = ttk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree.yview)
                        tree.configure(yscroll=scrollbar.set)
                        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    else:
                        messagebox.showinfo("No Results", "No doctors found matching your search criteria.")
                else:
                    messagebox.showwarning("Empty Search", "Please enter a search term.")

            tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)
        else:
            messagebox.showinfo("Doctors", "No doctors to search.")

    def delete_doctor(self):
        doctors = DoctorManager.view_all_doctors()
        if doctors:
            delete_window = tk.Toplevel(self.root)
            delete_window.title("Delete Doctor")
            delete_window.geometry("400x300")

            tk.Label(delete_window, text="Select Doctor to Delete:").pack(pady=10)
            
            doctor_ids = [f"{doctor['Doctor ID']} - {doctor['Name']}" for doctor in doctors]
            doctor_combobox = ttk.Combobox(delete_window, values=doctor_ids, state="readonly")
            doctor_combobox.pack(pady=10)

            def confirm_delete():
                selected = doctor_combobox.get()
                if selected:
                    doctor_id = selected.split(" - ")[0]
                    if DoctorManager.delete_doctor(doctor_id):
                        delete_window.destroy()

            tk.Button(delete_window, text="Delete", command=confirm_delete).pack(pady=10)
        else:
            messagebox.showinfo("Doctors", "No doctors to delete.")

    def view_all_appointments(self):
        appointments = AppointmentManager.view_appointments()
        if appointments:
            appointments_window = tk.Toplevel(self.root)
            appointments_window.title("All Appointments")
            appointments_window.geometry("1200x600")

            tree = ttk.Treeview(appointments_window, 
                              columns=("ID", "Patient ID", "Patient", "Doctor ID", "Doctor", "Date", "Time", "Reason", "Status"), 
                              show="headings")
            
            headings = ["Appointment ID", "Patient ID", "Patient Name", "Doctor ID", "Doctor Name", "Date", "Time", "Reason", "Status"]
            for i, heading in enumerate(headings):
                tree.heading(tree['columns'][i], text=heading)
                tree.column(tree['columns'][i], width=120, anchor='center')

            for appt in appointments:
                tree.insert("", tk.END, values=(
                    appt['Appointment ID'],
                    appt['Patient ID'],
                    appt['Patient Name'],
                    appt['Doctor ID'],
                    appt['Doctor Name'],
                    appt['Date'],
                    appt['Time'],
                    appt['Reason'],
                    appt['Status']
                ))

            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(appointments_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            messagebox.showinfo("Appointments", "No appointments found.")

    def search_appointments(self):
        appointments = AppointmentManager.view_appointments()
        if appointments:
            search_window = tk.Toplevel(self.root)
            search_window.title("Search Appointments")
            search_window.geometry("500x300")

            tk.Label(search_window, text="Search Appointments", font=("Arial", 16)).pack(pady=10)

            tk.Label(search_window, text="Search Field:").pack()
            search_field = ttk.Combobox(search_window, 
                                      values=["Appointment ID", "Patient Name", "Doctor Name", "Status"],
                                      state="readonly")
            search_field.pack(pady=5)
            search_field.set("Patient Name")

            tk.Label(search_window, text="Search Term:").pack()
            search_entry = tk.Entry(search_window, width=40)
            search_entry.pack(pady=5)

            def perform_search():
                field = search_field.get()
                term = search_entry.get().strip()
                
                if term:
                    results = SearchSortManager.linear_search(appointments, field, term)
                    if results:
                        result_window = tk.Toplevel(search_window)
                        result_window.title("Search Results")
                        result_window.geometry("1000x400")

                        tree = ttk.Treeview(result_window, 
                                          columns=("ID", "Patient", "Doctor", "Date", "Status"), 
                                          show="headings")
                        
                        headings = ["Appointment ID", "Patient Name", "Doctor Name", "Date", "Status"]
                        for i, heading in enumerate(headings):
                            tree.heading(tree['columns'][i], text=heading)
                            tree.column(tree['columns'][i], width=120, anchor='center')

                        for appt in results:
                            tree.insert("", tk.END, values=(
                                appt['Appointment ID'],
                                appt['Patient Name'],
                                appt['Doctor Name'],
                                appt['Date'],
                                appt['Status']
                            ))

                        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                        scrollbar = ttk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree.yview)
                        tree.configure(yscroll=scrollbar.set)
                        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    else:
                        messagebox.showinfo("No Results", "No appointments found matching your search criteria.")
                else:
                    messagebox.showwarning("Empty Search", "Please enter a search term.")

            tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)
        else:
            messagebox.showinfo("Appointments", "No appointments to search.")

    def delete_appointment(self):
        appointments = AppointmentManager.view_appointments()
        if appointments:
            delete_window = tk.Toplevel(self.root)
            delete_window.title("Delete Appointment")
            delete_window.geometry("400x300")

            tk.Label(delete_window, text="Select Appointment to Delete:").pack(pady=10)
            
            appointment_ids = [f"{appt['Appointment ID']} - {appt['Patient Name']} ({appt['Date']})" for appt in appointments]
            appointment_combobox = ttk.Combobox(delete_window, values=appointment_ids, state="readonly")
            appointment_combobox.pack(pady=10)

            def confirm_delete():
                selected = appointment_combobox.get()
                if selected:
                    appointment_id = selected.split(" - ")[0]
                    if AppointmentManager.delete_appointment(appointment_id):
                        delete_window.destroy()

            tk.Button(delete_window, text="Delete", command=confirm_delete).pack(pady=10)
        else:
            messagebox.showinfo("Appointments", "No appointments to delete.")

    def update_appointment_status(self):
        appointments = AppointmentManager.view_appointments()
        if appointments:
            update_window = tk.Toplevel(self.root)
            update_window.title("Update Appointment Status")
            update_window.geometry("500x300")

            tk.Label(update_window, text="Update Appointment Status", font=("Arial", 16)).pack(pady=10)

            tk.Label(update_window, text="Select Appointment:").pack()
            appointment_ids = [f"{appt['Appointment ID']} - {appt['Patient Name']} ({appt['Date']})" for appt in appointments]
            appointment_combobox = ttk.Combobox(update_window, values=appointment_ids, state="readonly")
            appointment_combobox.pack(pady=10)

            tk.Label(update_window, text="New Status:").pack()
            status_combobox = ttk.Combobox(update_window, 
                                         values=["Scheduled", "Completed", "Cancelled", "No Show"],
                                         state="readonly")
            status_combobox.pack(pady=10)

            def confirm_update():
                selected = appointment_combobox.get()
                new_status = status_combobox.get()
                
                if selected and new_status:
                    appointment_id = selected.split(" - ")[0]
                    if AppointmentManager.update_appointment_status(appointment_id, new_status):
                        messagebox.showinfo("Success", "Appointment status updated successfully!")
                        update_window.destroy()

            tk.Button(update_window, text="Update", command=confirm_update).pack(pady=10)
        else:
            messagebox.showinfo("Appointments", "No appointments to update.")

    def view_all_prescriptions(self):
        prescriptions = PrescriptionManager.view_prescriptions()
        if prescriptions:
            prescriptions_window = tk.Toplevel(self.root)
            prescriptions_window.title("All Prescriptions")
            prescriptions_window.geometry("1200x600")

            tree = ttk.Treeview(prescriptions_window, 
                              columns=("ID", "Patient ID", "Patient", "Doctor ID", "Doctor", 
                                      "Medication", "Dosage", "Issue Date", "Expiry Date"), 
                              show="headings")
            
            headings = ["Prescription ID", "Patient ID", "Patient Name", "Doctor ID", "Doctor Name",
                       "Medication", "Dosage", "Issue Date", "Expiry Date"]
            for i, heading in enumerate(headings):
                tree.heading(tree['columns'][i], text=heading)
                tree.column(tree['columns'][i], width=120, anchor='center')

            for pres in prescriptions:
                tree.insert("", tk.END, values=(
                    pres['Prescription ID'],
                    pres['Patient ID'],
                    pres['Patient Name'],
                    pres['Doctor ID'],
                    pres['Doctor Name'],
                    pres['Medication'],
                    pres['Dosage'],
                    pres['Issue Date'],
                    pres['Expiry Date']
                ))

            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(prescriptions_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            messagebox.showinfo("Prescriptions", "No prescriptions found.")

    def search_prescriptions(self):
        prescriptions = PrescriptionManager.view_prescriptions()
        if prescriptions:
            search_window = tk.Toplevel(self.root)
            search_window.title("Search Prescriptions")
            search_window.geometry("500x300")

            tk.Label(search_window, text="Search Prescriptions", font=("Arial", 16)).pack(pady=10)

            tk.Label(search_window, text="Search Field:").pack()
            search_field = ttk.Combobox(search_window, 
                                      values=["Prescription ID", "Patient Name", "Doctor Name", "Medication"],
                                      state="readonly")
            search_field.pack(pady=5)
            search_field.set("Patient Name")

            tk.Label(search_window, text="Search Term:").pack()
            search_entry = tk.Entry(search_window, width=40)
            search_entry.pack(pady=5)

            def perform_search():
                field = search_field.get()
                term = search_entry.get().strip()
                
                if term:
                    results = SearchSortManager.linear_search(prescriptions, field, term)
                    if results:
                        result_window = tk.Toplevel(search_window)
                        result_window.title("Search Results")
                        result_window.geometry("1000x400")

                        tree = ttk.Treeview(result_window, 
                                          columns=("ID", "Patient", "Doctor", "Medication", "Issue Date"), 
                                          show="headings")
                        
                        headings = ["Prescription ID", "Patient Name", "Doctor Name", "Medication", "Issue Date"]
                        for i, heading in enumerate(headings):
                            tree.heading(tree['columns'][i], text=heading)
                            tree.column(tree['columns'][i], width=120, anchor='center')

                        for pres in results:
                            tree.insert("", tk.END, values=(
                                pres['Prescription ID'],
                                pres['Patient Name'],
                                pres['Doctor Name'],
                                pres['Medication'],
                                pres['Issue Date']
                            ))

                        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                        scrollbar = ttk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree.yview)
                        tree.configure(yscroll=scrollbar.set)
                        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    else:
                        messagebox.showinfo("No Results", "No prescriptions found matching your search criteria.")
                else:
                    messagebox.showwarning("Empty Search", "Please enter a search term.")

            tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)
        else:
            messagebox.showinfo("Prescriptions", "No prescriptions to search.")

    def delete_prescription(self):
        prescriptions = PrescriptionManager.view_prescriptions()
        if prescriptions:
            delete_window = tk.Toplevel(self.root)
            delete_window.title("Delete Prescription")
            delete_window.geometry("400x300")

            tk.Label(delete_window, text="Select Prescription to Delete:").pack(pady=10)
            
            prescription_ids = [f"{pres['Prescription ID']} - {pres['Patient Name']} ({pres['Issue Date']})" for pres in prescriptions]
            prescription_combobox = ttk.Combobox(delete_window, values=prescription_ids, state="readonly")
            prescription_combobox.pack(pady=10)

            def confirm_delete():
                selected = prescription_combobox.get()
                if selected:
                    prescription_id = selected.split(" - ")[0]
                    if PrescriptionManager.delete_prescription(prescription_id):
                        delete_window.destroy()

            tk.Button(delete_window, text="Delete", command=confirm_delete).pack(pady=10)
        else:
            messagebox.showinfo("Prescriptions", "No prescriptions to delete.")

    def view_all_medical_records(self):
        records = MedicalRecordManager.view_records()
        if records:
            records_window = tk.Toplevel(self.root)
            records_window.title("All Medical Records")
            records_window.geometry("1200x600")

            tree = ttk.Treeview(records_window, 
                              columns=("ID", "Patient ID", "Patient", "Doctor ID", "Doctor", 
                                      "Visit Date", "Diagnosis", "Follow Up"), 
                              show="headings")
            
            headings = ["Record ID", "Patient ID", "Patient Name", "Doctor ID", "Doctor Name",
                       "Visit Date", "Diagnosis", "Follow Up"]
            for i, heading in enumerate(headings):
                tree.heading(tree['columns'][i], text=heading)
                tree.column(tree['columns'][i], width=120, anchor='center')

            for record in records:
                tree.insert("", tk.END, values=(
                    record['Record ID'],
                    record['Patient ID'],
                    record['Patient Name'],
                    record['Doctor ID'],
                    record['Doctor Name'],
                    record['Visit Date'],
                    record['Diagnosis'],
                    record['Follow Up']
                ))

            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(records_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            def view_details():
                selected_item = tree.selection()
                if selected_item:
                    record_id = tree.item(selected_item[0])['values'][0]
                    for record in records:
                        if record['Record ID'] == record_id:
                            details_window = tk.Toplevel(records_window)
                            details_window.title("Record Details")
                            details_window.geometry("600x400")

                            text_area = scrolledtext.ScrolledText(details_window, wrap=tk.WORD)
                            text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                            details = f"""Medical Record Details:
                            
Record ID: {record['Record ID']}
Patient: {record['Patient Name']} (ID: {record['Patient ID']})
Doctor: {record['Doctor Name']} (ID: {record['Doctor ID']})
Visit Date: {record['Visit Date']}

Diagnosis: {record['Diagnosis']}

Treatment:
{record['Treatment']}

Notes:
{record['Notes']}

Follow Up Required: {record['Follow Up']}
"""
                            text_area.insert(tk.END, details)
                            text_area.config(state=tk.DISABLED)

            details_btn = tk.Button(records_window, text="View Details", command=view_details)
            details_btn.pack(pady=10)
        else:
            messagebox.showinfo("Medical Records", "No medical records found.")

    def search_medical_records(self):
        records = MedicalRecordManager.view_records()
        if records:
            search_window = tk.Toplevel(self.root)
            search_window.title("Search Medical Records")
            search_window.geometry("500x300")

            tk.Label(search_window, text="Search Medical Records", font=("Arial", 16)).pack(pady=10)

            tk.Label(search_window, text="Search Field:").pack()
            search_field = ttk.Combobox(search_window, 
                                      values=["Record ID", "Patient Name", "Doctor Name", "Diagnosis"],
                                      state="readonly")
            search_field.pack(pady=5)
            search_field.set("Patient Name")

            tk.Label(search_window, text="Search Term:").pack()
            search_entry = tk.Entry(search_window, width=40)
            search_entry.pack(pady=5)

            def perform_search():
                field = search_field.get()
                term = search_entry.get().strip()
                
                if term:
                    results = SearchSortManager.linear_search(records, field, term)
                    if results:
                        result_window = tk.Toplevel(search_window)
                        result_window.title("Search Results")
                        result_window.geometry("1000x400")

                        tree = ttk.Treeview(result_window, 
                                          columns=("ID", "Patient", "Doctor", "Visit Date", "Diagnosis"), 
                                          show="headings")
                        
                        headings = ["Record ID", "Patient Name", "Doctor Name", "Visit Date", "Diagnosis"]
                        for i, heading in enumerate(headings):
                            tree.heading(tree['columns'][i], text=heading)
                            tree.column(tree['columns'][i], width=120, anchor='center')

                        for record in results:
                            tree.insert("", tk.END, values=(
                                record['Record ID'],
                                record['Patient Name'],
                                record['Doctor Name'],
                                record['Visit Date'],
                                record['Diagnosis']
                            ))

                        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                        scrollbar = ttk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree.yview)
                        tree.configure(yscroll=scrollbar.set)
                        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                        def view_details():
                            selected_item = tree.selection()
                            if selected_item:
                                record_id = tree.item(selected_item[0])['values'][0]
                                for record in results:
                                    if record['Record ID'] == record_id:
                                        details_window = tk.Toplevel(result_window)
                                        details_window.title("Record Details")
                                        details_window.geometry("600x400")

                                        text_area = scrolledtext.ScrolledText(details_window, wrap=tk.WORD)
                                        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                                        details = f"""Medical Record Details:
                                        
Record ID: {record['Record ID']}
Patient: {record['Patient Name']} (ID: {record['Patient ID']})
Doctor: {record['Doctor Name']} (ID: {record['Doctor ID']})
Visit Date: {record['Visit Date']}

Diagnosis: {record['Diagnosis']}

Treatment:
{record['Treatment']}

Notes:
{record['Notes']}

Follow Up Required: {record['Follow Up']}
"""
                                        text_area.insert(tk.END, details)
                                        text_area.config(state=tk.DISABLED)

                        details_btn = tk.Button(result_window, text="View Details", command=view_details)
                        details_btn.pack(pady=10)
                    else:
                        messagebox.showinfo("No Results", "No records found matching your search criteria.")
                else:
                    messagebox.showwarning("Empty Search", "Please enter a search term.")

            tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)
        else:
            messagebox.showinfo("Medical Records", "No medical records to search.")

    def delete_medical_record(self):
        records = MedicalRecordManager.view_records()
        if records:
            delete_window = tk.Toplevel(self.root)
            delete_window.title("Delete Medical Record")
            delete_window.geometry("400x300")

            tk.Label(delete_window, text="Select Record to Delete:").pack(pady=10)
            
            record_ids = [f"{record['Record ID']} - {record['Patient Name']} ({record['Visit Date']})" for record in records]
            record_combobox = ttk.Combobox(delete_window, values=record_ids, state="readonly")
            record_combobox.pack(pady=10)

            def confirm_delete():
                selected = record_combobox.get()
                if selected:
                    record_id = selected.split(" - ")[0]
                    if MedicalRecordManager.delete_record(record_id):
                        delete_window.destroy()

            tk.Button(delete_window, text="Delete", command=confirm_delete).pack(pady=10)
        else:
            messagebox.showinfo("Medical Records", "No medical records to delete.")

    def view_all_payments(self):
        payments = PaymentManager.view_payments()
        if payments:
            payments_window = tk.Toplevel(self.root)
            payments_window.title("All Payments")
            payments_window.geometry("1000x600")

            tree = ttk.Treeview(payments_window, 
                              columns=("Invoice", "Patient ID", "Patient", "Amount", "Method", "Status", "Date"), 
                              show="headings")
            
            headings = ["Invoice ID", "Patient ID", "Patient Name", "Amount", "Payment Method", "Status", "Date"]
            for i, heading in enumerate(headings):
                tree.heading(tree['columns'][i], text=heading)
                tree.column(tree['columns'][i], width=120, anchor='center')

            for payment in payments:
                tree.insert("", tk.END, values=(
                    payment['Invoice ID'],
                    payment['Patient ID'],
                    payment['Patient Name'],
                    payment['Amount'],
                    payment['Payment Method'],
                    payment['Status'],
                    payment['Date']
                ))

            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(payments_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            messagebox.showinfo("Payments", "No payment records found.")

    def search_payments(self):
        payments = PaymentManager.view_payments()
        if payments:
            search_window = tk.Toplevel(self.root)
            search_window.title("Search Payments")
            search_window.geometry("500x300")

            tk.Label(search_window, text="Search Payments", font=("Arial", 16)).pack(pady=10)

            tk.Label(search_window, text="Search Field:").pack()
            search_field = ttk.Combobox(search_window, 
                                      values=["Invoice ID", "Patient Name", "Status"],
                                      state="readonly")
            search_field.pack(pady=5)
            search_field.set("Patient Name")

            tk.Label(search_window, text="Search Term:").pack()
            search_entry = tk.Entry(search_window, width=40)
            search_entry.pack(pady=5)

            def perform_search():
                field = search_field.get()
                term = search_entry.get().strip()
                
                if term:
                    results = SearchSortManager.linear_search(payments, field, term)
                    if results:
                        result_window = tk.Toplevel(search_window)
                        result_window.title("Search Results")
                        result_window.geometry("800x400")

                        tree = ttk.Treeview(result_window, 
                                          columns=("Invoice", "Patient", "Amount", "Date", "Status"), 
                                          show="headings")
                        
                        headings = ["Invoice ID", "Patient Name", "Amount", "Date", "Status"]
                        for i, heading in enumerate(headings):
                            tree.heading(tree['columns'][i], text=heading)
                            tree.column(tree['columns'][i], width=120, anchor='center')

                        for payment in results:
                            tree.insert("", tk.END, values=(
                                payment['Invoice ID'],
                                payment['Patient Name'],
                                payment['Amount'],
                                payment['Date'],
                                payment['Status']
                            ))

                        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                        scrollbar = ttk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree.yview)
                        tree.configure(yscroll=scrollbar.set)
                        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    else:
                        messagebox.showinfo("No Results", "No payments found matching your search criteria.")
                else:
                    messagebox.showwarning("Empty Search", "Please enter a search term.")

            tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)
        else:
            messagebox.showinfo("Payments", "No payment records to search.")

    def process_payment(self):
        patients = PatientManager.view_all_patients()
        if patients:
            payment_window = tk.Toplevel(self.root)
            payment_window.title("Process Payment")
            payment_window.geometry("500x400")

            tk.Label(payment_window, text="Process Payment", font=("Arial", 16)).pack(pady=10)

            tk.Label(payment_window, text="Select Patient:").pack()
            patient_names = [f"{patient['Patient ID']} - {patient['Name']}" for patient in patients]
            patient_combobox = ttk.Combobox(payment_window, values=patient_names, state="readonly")
            patient_combobox.pack(pady=10)

            tk.Label(payment_window, text="Amount:").pack()
            amount_entry = tk.Entry(payment_window)
            amount_entry.pack(pady=10)

            tk.Label(payment_window, text="Payment Method:").pack()
            method_combobox = ttk.Combobox(payment_window, 
                                          values=["Cash", "Credit Card", "Debit Card", "Bank Transfer"],
                                          state="readonly")
            method_combobox.pack(pady=10)

            def submit_payment():
                patient_info = patient_combobox.get()
                amount = amount_entry.get()
                method = method_combobox.get()

                if patient_info and amount and method:
                    patient_id = patient_info.split(" - ")[0]
                    patient_name = patient_info.split(" - ")[1]
                    
                    try:
                        amount = float(amount)
                        if PaymentManager.process_payment(patient_id, patient_name, amount, method):
                            payment_window.destroy()
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid amount")
                else:
                    messagebox.showerror("Error", "Please fill all fields")

            tk.Button(payment_window, text="Process Payment", command=submit_payment).pack(pady=10)
        else:
            messagebox.showinfo("Patients", "No patients available to process payment")

    def doctor_dashboard(self):
        doctor_window = tk.Toplevel(self.root)
        doctor_window.title("Doctor Dashboard")
        doctor_window.geometry("600x600")

        bg_canvas = BackgroundManager.set_background(doctor_window, self.background_image)

        doctor_frame = tk.Frame(doctor_window, bg='white', bd=10, relief=tk.RAISED)
        if bg_canvas:
            bg_canvas.create_window(300, 300, window=doctor_frame)
        else:
            doctor_frame.pack(expand=True, fill='both')

        tk.Label(doctor_frame, text="Doctor Dashboard",
                 font=("Arial", 20, "bold"),
                 fg="navy",
                 bg='white').pack(pady=20)

        def view_appointments():
            appointments = AppointmentManager.view_appointments(doctor_id=self.current_user_id)
            if appointments:
                appointments_window = tk.Toplevel(doctor_window)
                appointments_window.title("My Appointments")
                appointments_window.geometry("1000x600")

                tree = ttk.Treeview(appointments_window, 
                                  columns=("ID", "Patient", "Date", "Time", "Reason", "Status"), 
                                  show="headings")
                
                headings = ["Appointment ID", "Patient Name", "Date", "Time", "Reason", "Status"]
                for i, heading in enumerate(headings):
                    tree.heading(tree['columns'][i], text=heading)
                    tree.column(tree['columns'][i], width=120, anchor='center')

                for appt in appointments:
                    tree.insert("", tk.END, values=(
                        appt['Appointment ID'],
                        appt['Patient Name'],
                        appt['Date'],
                        appt['Time'],
                        appt['Reason'],
                        appt['Status']
                    ))

                tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                scrollbar = ttk.Scrollbar(appointments_window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                def update_status():
                    selected_item = tree.selection()
                    if selected_item:
                        appt_id = tree.item(selected_item[0])['values'][0]
                        status_window = tk.Toplevel(appointments_window)
                        status_window.title("Update Status")
                        status_window.geometry("300x200")

                        tk.Label(status_window, text="Select New Status:").pack(pady=10)
                        status_var = tk.StringVar()
                        status_combobox = ttk.Combobox(status_window, 
                                                      values=["Scheduled", "Completed", "Cancelled", "No Show"],
                                                      textvariable=status_var,
                                                      state="readonly")
                        status_combobox.pack(pady=10)

                        def confirm_update():
                            new_status = status_var.get()
                            if new_status:
                                if AppointmentManager.update_appointment_status(appt_id, new_status):
                                    messagebox.showinfo("Success", "Appointment status updated!")
                                    status_window.destroy()
                                    appointments_window.destroy()
                                    view_appointments()  # Refresh view

                        tk.Button(status_window, text="Update", command=confirm_update).pack(pady=10)

                update_btn = tk.Button(appointments_window, text="Update Status", command=update_status)
                update_btn.pack(pady=10)
            else:
                messagebox.showinfo("Appointments", "No appointments found.")

        def create_prescription():
            patients = PatientManager.view_all_patients()
            if patients:
                prescription_window = tk.Toplevel(doctor_window)
                prescription_window.title("Create Prescription")
                prescription_window.geometry("600x600")

                tk.Label(prescription_window, text="Create New Prescription", font=("Arial", 20)).pack(pady=10)

                # Patient Selection
                tk.Label(prescription_window, text="Select Patient:").pack()
                patient_names = [f"{patient['Patient ID']} - {patient['Name']}" for patient in patients]
                patient_var = tk.StringVar()
                patient_combobox = ttk.Combobox(prescription_window, values=patient_names, state="readonly", textvariable=patient_var)
                patient_combobox.pack(pady=10)

                # Medication Details
                tk.Label(prescription_window, text="Medication:").pack()
                medication_entry = tk.Entry(prescription_window, width=40)
                medication_entry.pack(pady=5)

                tk.Label(prescription_window, text="Dosage:").pack()
                dosage_entry = tk.Entry(prescription_window, width=40)
                dosage_entry.pack(pady=5)

                tk.Label(prescription_window, text="Instructions:").pack()
                instructions_entry = tk.Text(prescription_window, width=40, height=5)
                instructions_entry.pack(pady=5)

                # Dates
                tk.Label(prescription_window, text="Issue Date:").pack()
                issue_date = DateEntry(prescription_window, width=12, background='darkblue', foreground='white')
                issue_date.pack(pady=5)

                tk.Label(prescription_window, text="Expiry Date:").pack()
                expiry_date = DateEntry(prescription_window, width=12, background='darkblue', foreground='white')
                expiry_date.pack(pady=5)

                def submit_prescription():
                    patient_id = patient_var.get().split(" - ")[0] if patient_var.get() else ""
                    medication = medication_entry.get()
                    dosage = dosage_entry.get()
                    instructions = instructions_entry.get("1.0", tk.END).strip()
                    issue = issue_date.get_date()
                    expiry = expiry_date.get_date()

                    if patient_id and medication and dosage and instructions and issue and expiry:
                        doctor_details = DoctorManager.get_doctor_details(self.current_user_id)
                        if doctor_details:
                            patient_details = PatientManager.get_patient_details(patient_id)
                            if patient_details:
                                PrescriptionManager.create_prescription(
                                    patient_id,
                                    patient_details['Name'],
                                    self.current_user_id,
                                    doctor_details['Name'],
                                    medication,
                                    dosage,
                                    instructions,
                                    issue,
                                    expiry
                                )
                                prescription_window.destroy()
                    else:
                        messagebox.showerror("Error", "Please fill all fields")

                tk.Button(prescription_window, text="Create Prescription", command=submit_prescription).pack(pady=10)
            else:
                messagebox.showinfo("Patients", "No patients available to create prescription")

        def view_prescriptions():
            prescriptions = PrescriptionManager.view_prescriptions(doctor_id=self.current_user_id)
            if prescriptions:
                prescriptions_window = tk.Toplevel(doctor_window)
                prescriptions_window.title("My Prescriptions")
                prescriptions_window.geometry("1000x600")

                tree = ttk.Treeview(prescriptions_window, 
                                  columns=("ID", "Patient", "Medication", "Dosage", "Issue Date", "Expiry Date"), 
                                  show="headings")
                
                headings = ["Prescription ID", "Patient Name", "Medication", "Dosage", "Issue Date", "Expiry Date"]
                for i, heading in enumerate(headings):
                    tree.heading(tree['columns'][i], text=heading)
                    tree.column(tree['columns'][i], width=120, anchor='center')

                for pres in prescriptions:
                    tree.insert("", tk.END, values=(
                        pres['Prescription ID'],
                        pres['Patient Name'],
                        pres['Medication'],
                        pres['Dosage'],
                        pres['Issue Date'],
                        pres['Expiry Date']
                    ))

                tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                scrollbar = ttk.Scrollbar(prescriptions_window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                def view_instructions():
                    selected_item = tree.selection()
                    if selected_item:
                        pres_id = tree.item(selected_item[0])['values'][0]
                        for pres in prescriptions:
                            if pres['Prescription ID'] == pres_id:
                                instructions_window = tk.Toplevel(prescriptions_window)
                                instructions_window.title("Prescription Instructions")
                                instructions_window.geometry("500x300")

                                text_area = scrolledtext.ScrolledText(instructions_window, wrap=tk.WORD)
                                text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                                details = f"""Prescription Instructions:
                                
Medication: {pres['Medication']}
Dosage: {pres['Dosage']}

Instructions:
{pres['Instructions']}

Issued by: {pres['Doctor Name']}
Issue Date: {pres['Issue Date']}
Expiry Date: {pres['Expiry Date']}
"""
                                text_area.insert(tk.END, details)
                                text_area.config(state=tk.DISABLED)

                instructions_btn = tk.Button(prescriptions_window, text="View Instructions", command=view_instructions)
                instructions_btn.pack(pady=10)
            else:
                messagebox.showinfo("Prescriptions", "No prescriptions found")

        def create_medical_record():
            patients = PatientManager.view_all_patients()
            if patients:
                record_window = tk.Toplevel(doctor_window)
                record_window.title("Create Medical Record")
                record_window.geometry("600x600")

                tk.Label(record_window, text="Create Medical Record", font=("Arial", 20)).pack(pady=10)

                # Patient Selection
                tk.Label(record_window, text="Select Patient:").pack()
                patient_names = [f"{patient['Patient ID']} - {patient['Name']}" for patient in patients]
                patient_var = tk.StringVar()
                patient_combobox = ttk.Combobox(record_window, values=patient_names, state="readonly", textvariable=patient_var)
                patient_combobox.pack(pady=10)

                # Visit Details
                tk.Label(record_window, text="Visit Date:").pack()
                visit_date = DateEntry(record_window, width=12, background='darkblue', foreground='white')
                visit_date.pack(pady=5)

                tk.Label(record_window, text="Diagnosis:").pack()
                diagnosis_entry = tk.Entry(record_window, width=40)
                diagnosis_entry.pack(pady=5)

                tk.Label(record_window, text="Treatment:").pack()
                treatment_entry = tk.Text(record_window, width=40, height=5)
                treatment_entry.pack(pady=5)

                tk.Label(record_window, text="Notes:").pack()
                notes_entry = tk.Text(record_window, width=40, height=5)
                notes_entry.pack(pady=5)

                tk.Label(record_window, text="Follow Up Required:").pack()
                follow_var = tk.StringVar(value="No")
                follow_combobox = ttk.Combobox(record_window, values=["Yes", "No"], state="readonly", textvariable=follow_var)
                follow_combobox.pack(pady=5)

                def submit_record():
                    patient_id = patient_var.get().split(" - ")[0] if patient_var.get() else ""
                    diagnosis = diagnosis_entry.get()
                    treatment = treatment_entry.get("1.0", tk.END).strip()
                    notes = notes_entry.get("1.0", tk.END).strip()
                    follow_up = follow_var.get()
                    visit = visit_date.get_date()

                    if patient_id and diagnosis and treatment and notes and follow_up and visit:
                        doctor_details = DoctorManager.get_doctor_details(self.current_user_id)
                        if doctor_details:
                            patient_details = PatientManager.get_patient_details(patient_id)
                            if patient_details:
                                MedicalRecordManager.create_record(
                                    patient_id,
                                    patient_details['Name'],
                                    self.current_user_id,
                                    doctor_details['Name'],
                                    visit,
                                    diagnosis,
                                    treatment,
                                    notes,
                                    follow_up
                                )
                                record_window.destroy()
                    else:
                        messagebox.showerror("Error", "Please fill all fields")

                tk.Button(record_window, text="Create Record", command=submit_record).pack(pady=10)
            else:
                messagebox.showinfo("Patients", "No patients available to create record")

        def view_medical_records():
            records = MedicalRecordManager.view_records(doctor_id=self.current_user_id)
            if records:
                records_window = tk.Toplevel(doctor_window)
                records_window.title("Medical Records")
                records_window.geometry("1000x600")

                tree = ttk.Treeview(records_window, 
                                  columns=("ID", "Patient", "Visit Date", "Diagnosis", "Follow Up"), 
                                  show="headings")
                
                headings = ["Record ID", "Patient Name", "Visit Date", "Diagnosis", "Follow Up"]
                for i, heading in enumerate(headings):
                    tree.heading(tree['columns'][i], text=heading)
                    tree.column(tree['columns'][i], width=120, anchor='center')

                for record in records:
                    tree.insert("", tk.END, values=(
                        record['Record ID'],
                        record['Patient Name'],
                        record['Visit Date'],
                        record['Diagnosis'],
                        record['Follow Up']
                    ))

                tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                scrollbar = ttk.Scrollbar(records_window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                def view_details():
                    selected_item = tree.selection()
                    if selected_item:
                        record_id = tree.item(selected_item[0])['values'][0]
                        for record in records:
                            if record['Record ID'] == record_id:
                                details_window = tk.Toplevel(records_window)
                                details_window.title("Record Details")
                                details_window.geometry("600x400")

                                text_area = scrolledtext.ScrolledText(details_window, wrap=tk.WORD)
                                text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                                details = f"""Medical Record Details:
                                
Record ID: {record['Record ID']}
Patient: {record['Patient Name']} (ID: {record['Patient ID']})
Doctor: {record['Doctor Name']} (ID: {record['Doctor ID']})
Visit Date: {record['Visit Date']}

Diagnosis: {record['Diagnosis']}

Treatment:
{record['Treatment']}

Notes:
{record['Notes']}

Follow Up Required: {record['Follow Up']}
"""
                                text_area.insert(tk.END, details)
                                text_area.config(state=tk.DISABLED)

                details_btn = tk.Button(records_window, text="View Details", command=view_details)
                details_btn.pack(pady=10)
            else:
                messagebox.showinfo("Medical Records", "No medical records found")

        buttons = [
            ("View Appointments", view_appointments),
            ("Create Prescription", create_prescription),
            ("View Prescriptions", view_prescriptions),
            ("Create Medical Record", create_medical_record),
            ("View Medical Records", view_medical_records),
            ("Logout", doctor_window.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                doctor_frame,
                text=text,
                command=command,
                font=("Arial", 14),
                bg="navy",
                fg="white",
                width=25,
                activebackground="darkblue",
                activeforeground="white"
            )
            btn.pack(pady=10)

    def patient_dashboard(self):
        patient_window = tk.Toplevel(self.root)
        patient_window.title("Patient Dashboard")
        patient_window.geometry("600x600")

        bg_canvas = BackgroundManager.set_background(patient_window, self.background_image)

        patient_frame = tk.Frame(patient_window, bg='white', bd=10, relief=tk.RAISED)
        if bg_canvas:
            bg_canvas.create_window(300, 300, window=patient_frame)
        else:
            patient_frame.pack(expand=True, fill='both')

        tk.Label(patient_frame, text="Patient Dashboard",
                 font=("Arial", 20, "bold"),
                 fg="navy",
                 bg='white').pack(pady=20)

        def make_appointment():
            doctors = DoctorManager.view_all_doctors()
            if doctors:
                appointment_window = tk.Toplevel(patient_window)
                appointment_window.title("Make Appointment")
                appointment_window.geometry("500x500")

                tk.Label(appointment_window, text="Book Appointment", font=("Arial", 20)).pack(pady=10)

                tk.Label(appointment_window, text="Select Doctor:").pack()
                doctor_names = [f"{doctor['Name']} - {doctor['Specialization']}" for doctor in doctors]
                doctor_combobox = ttk.Combobox(appointment_window, values=doctor_names, state="readonly")
                doctor_combobox.pack(pady=10)

                tk.Label(appointment_window, text="Select Date:").pack()
                date_picker = DateEntry(appointment_window, width=12, background='darkblue', foreground='white')
                date_picker.pack(pady=10)

                tk.Label(appointment_window, text="Time (HH:MM):").pack()
                time_entry = tk.Entry(appointment_window)
                time_entry.pack(pady=10)

                tk.Label(appointment_window, text="Reason for Appointment:").pack()
                reason_entry = tk.Entry(appointment_window, width=50)
                reason_entry.pack(pady=10)

                def submit_appointment():
                    doctor_info = doctor_combobox.get()
                    date = date_picker.get_date()
                    time = time_entry.get()
                    reason = reason_entry.get()

                    if doctor_info and date and time and reason:
                        doctor_id = None
                        for doctor in doctors:
                            if f"{doctor['Name']} - {doctor['Specialization']}" == doctor_info:
                                doctor_id = doctor['Doctor ID']
                                break
                        
                        if doctor_id:
                            AppointmentManager.make_appointment(
                                self.current_user_id,
                                self.current_patient_name,
                                doctor_id,
                                doctor_info.split(" - ")[0],
                                date,
                                time,
                                reason
                            )
                            appointment_window.destroy()
                    else:
                        messagebox.showerror("Error", "Please fill all fields")

                tk.Button(appointment_window, text="Book Appointment", command=submit_appointment).pack(pady=10)
            else:
                messagebox.showinfo("Doctors", "No doctors available to book appointment")

        def view_appointments():
            appointments = AppointmentManager.view_appointments(patient_id=self.current_user_id)
            if appointments:
                appointments_window = tk.Toplevel(patient_window)
                appointments_window.title("My Appointments")
                appointments_window.geometry("800x400")

                tree = ttk.Treeview(appointments_window, 
                                  columns=("ID", "Doctor", "Date", "Time", "Reason", "Status"), 
                                  show="headings")
                
                headings = ["Appointment ID", "Doctor Name", "Date", "Time", "Reason", "Status"]
                for i, heading in enumerate(headings):
                    tree.heading(tree['columns'][i], text=heading)
                    tree.column(tree['columns'][i], width=120, anchor='center')

                for appt in appointments:
                    tree.insert("", tk.END, values=(
                        appt['Appointment ID'],
                        appt['Doctor Name'],
                        appt['Date'],
                        appt['Time'],
                        appt['Reason'],
                        appt['Status']
                    ))

                tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                scrollbar = ttk.Scrollbar(appointments_window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                def cancel_appointment():
                    selected_item = tree.selection()
                    if selected_item:
                        appt_id = tree.item(selected_item[0])['values'][0]
                        if AppointmentManager.delete_appointment(appt_id):
                            appointments_window.destroy()
                            view_appointments()  # Refresh view

                cancel_btn = tk.Button(appointments_window, text="Cancel Appointment", command=cancel_appointment)
                cancel_btn.pack(pady=10)
            else:
                messagebox.showinfo("Appointments", "No appointments found")

        def view_prescriptions():
            prescriptions = PrescriptionManager.view_prescriptions(patient_id=self.current_user_id)
            if prescriptions:
                prescriptions_window = tk.Toplevel(patient_window)
                prescriptions_window.title("My Prescriptions")
                prescriptions_window.geometry("800x400")

                tree = ttk.Treeview(prescriptions_window, 
                                  columns=("ID", "Doctor", "Medication", "Dosage", "Issue Date", "Expiry Date"), 
                                  show="headings")
                
                headings = ["Prescription ID", "Doctor Name", "Medication", "Dosage", "Issue Date", "Expiry Date"]
                for i, heading in enumerate(headings):
                    tree.heading(tree['columns'][i], text=heading)
                    tree.column(tree['columns'][i], width=120, anchor='center')

                for pres in prescriptions:
                    tree.insert("", tk.END, values=(
                        pres['Prescription ID'],
                        pres['Doctor Name'],
                        pres['Medication'],
                        pres['Dosage'],
                        pres['Issue Date'],
                        pres['Expiry Date']
                    ))

                tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                scrollbar = ttk.Scrollbar(prescriptions_window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                def view_instructions():
                    selected_item = tree.selection()
                    if selected_item:
                        pres_id = tree.item(selected_item[0])['values'][0]
                        for pres in prescriptions:
                            if pres['Prescription ID'] == pres_id:
                                instructions_window = tk.Toplevel(prescriptions_window)
                                instructions_window.title("Prescription Instructions")
                                instructions_window.geometry("500x300")

                                text_area = scrolledtext.ScrolledText(instructions_window, wrap=tk.WORD)
                                text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                                details = f"""Prescription Instructions:
                                
Medication: {pres['Medication']}
Dosage: {pres['Dosage']}

Instructions:
{pres['Instructions']}

Issued by: {pres['Doctor Name']}
Issue Date: {pres['Issue Date']}
Expiry Date: {pres['Expiry Date']}
"""
                                text_area.insert(tk.END, details)
                                text_area.config(state=tk.DISABLED)

                instructions_btn = tk.Button(prescriptions_window, text="View Instructions", command=view_instructions)
                instructions_btn.pack(pady=10)
            else:
                messagebox.showinfo("Prescriptions", "No prescriptions found")

        def view_medical_records():
            records = MedicalRecordManager.view_records(patient_id=self.current_user_id)
            if records:
                records_window = tk.Toplevel(patient_window)
                records_window.title("Medical Records")
                records_window.geometry("800x400")

                tree = ttk.Treeview(records_window, 
                                  columns=("ID", "Doctor", "Visit Date", "Diagnosis", "Follow Up"), 
                                  show="headings")
                
                headings = ["Record ID", "Doctor Name", "Visit Date", "Diagnosis", "Follow Up"]
                for i, heading in enumerate(headings):
                    tree.heading(tree['columns'][i], text=heading)
                    tree.column(tree['columns'][i], width=120, anchor='center')

                for record in records:
                    tree.insert("", tk.END, values=(
                        record['Record ID'],
                        record['Doctor Name'],
                        record['Visit Date'],
                        record['Diagnosis'],
                        record['Follow Up']
                    ))

                tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                scrollbar = ttk.Scrollbar(records_window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                def view_details():
                    selected_item = tree.selection()
                    if selected_item:
                        record_id = tree.item(selected_item[0])['values'][0]
                        for record in records:
                            if record['Record ID'] == record_id:
                                details_window = tk.Toplevel(records_window)
                                details_window.title("Record Details")
                                details_window.geometry("600x400")

                                text_area = scrolledtext.ScrolledText(details_window, wrap=tk.WORD)
                                text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                                details = f"""Medical Record Details:
                                
Record ID: {record['Record ID']}
Doctor: {record['Doctor Name']}
Visit Date: {record['Visit Date']}

Diagnosis: {record['Diagnosis']}

Treatment:
{record['Treatment']}

Notes:
{record['Notes']}

Follow Up Required: {record['Follow Up']}
"""
                                text_area.insert(tk.END, details)
                                text_area.config(state=tk.DISABLED)

                details_btn = tk.Button(records_window, text="View Details", command=view_details)
                details_btn.pack(pady=10)
            else:
                messagebox.showinfo("Medical Records", "No medical records found")

        def make_payment():
            payment_window = tk.Toplevel(patient_window)
            payment_window.title("Make Payment")
            payment_window.geometry("400x300")

            tk.Label(payment_window, text="Make Payment", font=("Arial", 20)).pack(pady=10)
            tk.Label(payment_window, text="Amount:").pack()
            amount_entry = tk.Entry(payment_window)
            amount_entry.pack(pady=5)

            tk.Label(payment_window, text="Payment Method:").pack()
            methods = ["Credit Card", "Debit Card", "Bank Transfer", "PayPal"]
            method_combobox = ttk.Combobox(payment_window, values=methods, state="readonly")
            method_combobox.pack(pady=5)

            def submit_payment():
                amount = amount_entry.get()
                method = method_combobox.get()

                if amount and method:
                    PaymentManager.process_payment(
                        self.current_user_id,
                        self.current_patient_name,
                        amount,
                        method
                    )
                    payment_window.destroy()
                else:
                    messagebox.showerror("Error", "Please fill all fields")

            tk.Button(payment_window, text="Pay", command=submit_payment).pack(pady=10)

        def view_bills():
            payments = PaymentManager.view_payments(patient_id=self.current_user_id)
            if payments:
                bills_window = tk.Toplevel(patient_window)
                bills_window.title("My Bills")
                bills_window.geometry("600x400")

                tree = ttk.Treeview(bills_window, 
                                  columns=("Invoice", "Amount", "Method", "Status", "Date"), 
                                  show="headings")
                
                headings = ["Invoice ID", "Amount", "Payment Method", "Status", "Date"]
                for i, heading in enumerate(headings):
                    tree.heading(tree['columns'][i], text=heading)
                    tree.column(tree['columns'][i], width=120, anchor='center')

                for payment in payments:
                    tree.insert("", tk.END, values=(
                        payment['Invoice ID'],
                        payment['Amount'],
                        payment['Payment Method'],
                        payment['Status'],
                        payment['Date']
                    ))

                tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                scrollbar = ttk.Scrollbar(bills_window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                messagebox.showinfo("Bills", "No payment records found")

        buttons = [
            ("Make Appointment", make_appointment),
            ("View Appointments", view_appointments),
            ("View Prescriptions", view_prescriptions),
            ("View Medical Records", view_medical_records),
            ("Make Payment", make_payment),
            ("View My Bills", view_bills),
            ("Logout", patient_window.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                patient_frame,
                text=text,
                command=command,
                font=("Arial", 14),
                bg="navy",
                fg="white",
                width=25,
                activebackground="darkblue",
                activeforeground="white"
            )
            btn.pack(pady=10)

    def logout(self):
        self.current_user_id = None
        self.current_user_type = None
        self.current_patient_name = None
        self.create_home_screen()

    def on_close(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MediTrackGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
    