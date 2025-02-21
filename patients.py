import hashlib, sqlite3
from database import *

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

if __name__ == "__main__":
    patients = Patients()
    patients.createPatientAccount_table()
    
    # Test creating an account
    patients.createPatientAccount('Juan Dela Cruz', 'admin@gmail.com', 'password1234')
    
    # Try creating the same account again (should show an error)
    patients.createPatientAccount('Juan Dela Cruz', 'admin@gmail.com', 'password5678')
    
    patients.close()  # Close the database connection
