import hashlib, sqlite3
from database import *
import json


class Patients(Database):
    def createPatientAccount_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_account (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        self.conn.commit()  # Commit table creation 

    def email_exists(self, email):
        """ Check if the email already exists in the database """
        self.cursor.execute("SELECT email FROM patient_account WHERE email = ?", (email,))
        return self.cursor.fetchone() is not None  # Returns True if email exists

    def createPatientAccount(self, fullname, email, password):
        """ Create a new patient account only if email is unique """
        if self.email_exists(email):
            print(f"Error: The email '{email}' is already in use.")
            return False

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            self.cursor.execute('''
                INSERT INTO patient_account (fullname, email, password)
                VALUES (?, ?, ?)
            ''', (fullname, email, hashed_password))
            self.conn.commit()
            print("Account created successfully")
            return True
        except sqlite3.Error as e:
            print("Error creating account:", e)
            return False
        
    def hash_password(self, password):
        """Hashes the password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def login_patient_account(self, email, password):
        """Checks if the email and password combination exists in the database."""
        hashed_password = self.hash_password(password)

        self.cursor.execute('''
            SELECT COUNT(*) FROM patient_account
            WHERE email = ? AND password = ?
        ''', (email, hashed_password))

        result = self.cursor.fetchone()
        return result[0] > 0  # True if exists, False otherwise

    def search_patient_session(self, email, password):
        """Retrieves patient details if login credentials are valid."""
        hashed_password = self.hash_password(password)

        # Fetch relevant patient account details (excluding password)
        self.cursor.execute('''
            SELECT patient_id, fullname, email, created_at FROM patient_account
            WHERE email = ? AND password = ?
        ''', (email, hashed_password))
        
        result = self.cursor.fetchone()

        # Prepare the response data
        if result:
            response_data = {
                'success': True,
                'account': {
                    'patient_id': result[0],
                    'fullname': result[1],
                    'email': result[2],
                    'created_at': result[3]  # Removed password for security
                }
            }
        else:
            response_data = {
                'success': False,
                'message': 'Incorrect Email or Password'
            }

        return json.dumps(response_data)

if __name__ == "__main__":
    patients = Patients()
    patients.createPatientAccount_table()
    
    # Test creating an account
    patients.createPatientAccount('Juan Dela Cruz', 'admin@gmail.com', 'password1234')
    
    # Try creating the same account again (should show an error)
    patients.createPatientAccount('Juan Dela Cruz', 'admin@gmail.com', 'password5678')
    
    patients.close()  # Close the database connection
