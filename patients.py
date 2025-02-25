import hashlib
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from database import Database

class Patients(Database):
    def __init__(self):
        """Initializes the Patients class and ensures the database connection is established."""
        super().__init__()  # Calls the parent class's constructor, which connects to the DB

    def create_patient_account_table(self):
        """Creates the patient_account table in PostgreSQL."""
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS patient_account (
                patient_id SERIAL PRIMARY KEY,
                fullname TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        print("✅ Table `patient_account` is ready.")

    def email_exists(self, email):
        """Checks if the email already exists in the database."""
        result = self.fetch_one("SELECT email FROM patient_account WHERE email = %s", (email,))
        return result is not None  # Returns True if email exists
    

    def insert_donation(self,donor_id,donor_name, donor_age, donor_city,donor_contact,donor_email,donor_bloodtype):
        donor_status='Pending'
        try:
            self.execute_query('''
                INSERT INTO patient_donation (donor_id, donor_name, donor_age,donor_city,donor_contact,donor_email,donor_bloodtype,donor_status)
                VALUES (%s,%s, %s, %s,%s, %s, %s,%s)
            ''', (donor_id,donor_name, donor_age, donor_city,donor_contact,donor_email,donor_bloodtype,donor_status))
            print("✅ Donation Succesfully Recorded")
            return True
        except psycopg2.Error as e:
            print("❌ Error creating account:", e)
            return False



    def create_patient_account(self, fullname, email, password):
        """Creates a new patient account only if email is unique."""
        if self.email_exists(email):
            print(f"❌ Error: The email '{email}' is already in use.")
            return False

        hashed_password = self.hash_password(password)

        try:
            self.execute_query('''
                INSERT INTO patient_account (fullname, email, password)
                VALUES (%s, %s, %s)
            ''', (fullname, email, hashed_password))
            print("✅ Account created successfully")
            return True
        except psycopg2.Error as e:
            print("❌ Error creating account:", e)
            return False
        

    def fetchAllDonation(self, patient_id):
        """Fetches all donation records from patient_donation for a given patient ID."""
        query = "SELECT * FROM patient_donation WHERE donor_status = %s AND donor_id != %s"
        params = ("Pending", patient_id)
        rows = self.fetch_all(query, params)
        return rows if rows else []

    

    def fetchDonorDonation(self, donor_id):
        """Fetches all donation records from patient_donation for a specific donor."""
        query = "SELECT * FROM patient_donation WHERE donor_id = %s" 
        rows = self.fetch_all(query, (donor_id,))
        return rows if rows else []  # Return an empty list if no records exist
    
    
    def deleteDonation(self, donation_id):
        """Deletes a donation record from patient_donation using donation_id."""
        query = "DELETE FROM patient_donation WHERE id = %s"
        success = self.execute_query(query, (donation_id,))
        return success  # Returns True if deletion was successful, False otherwise

    def markDonationAsDone(self, donation_id):
        """Marks a donation as done in the database."""
        query = "UPDATE patient_donation SET donor_status = 'Done' WHERE id = %s"
        success = self.execute_query(query, (donation_id,))
        return success  # Returns True if successful


        

    def hash_password(self, password):
        """Hashes the password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def login_patient_account(self, email, password):
        """Checks if the email and password combination exists in the database."""
        hashed_password = self.hash_password(password)

        result = self.fetch_one('''
            SELECT COUNT(*) FROM patient_account
            WHERE email = %s AND password = %s
        ''', (email, hashed_password))

        return result['count'] > 0 if result else False

    def search_patient_session(self, email, password):
        """Retrieves patient details if login credentials are valid."""
        hashed_password = self.hash_password(password)

        result = self.fetch_one('''
            SELECT patient_id, fullname, email, created_at FROM patient_account
            WHERE email = %s AND password = %s
        ''', (email, hashed_password))

        # Prepare the response data
        if result:
            response_data = {
                'success': True,
                'account': result
            }
        else:
            response_data = {
                'success': False,
                'message': 'Incorrect Email or Password'
            }

        return json.dumps(response_data, default=str)

    def close(self):
        """Close the database connection properly when done."""
        super().close()  # Calls the parent class's close method
