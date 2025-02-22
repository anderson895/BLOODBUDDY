from flask import Flask, redirect, render_template, request, jsonify, session, url_for, json
from patients import Patients  

app = Flask(__name__)
app.secret_key = "gdwadwad"  # 🔐 Change this for better security

@app.route('/')
def landing():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/patient/donation_success')
def donation_success():
    return render_template('/patient/donation_success.html')


@app.route('/patient/about_patient')
def about_patient():
    return render_template('/patient/about_patient.html')
    

    
@app.route('/patient/donate_patient')
def donate_patient():
    return render_template('/patient/donate_patient.html')



@app.route('/patient/home_patient')
def home_patient():
    if 'patient_id' not in session:  
        return redirect(url_for('logout')) 
    return render_template('patient/home_patient.html', session=session)



@app.route('/get-blood-list', methods=['GET'])
def get_blood_list():
    patient_id = session.get('patient_id')
    if not patient_id:
        return jsonify({"error": "Patient ID is missing"}), 400

    data = Patients().fetchDonorDonation(patient_id)
    return jsonify(data)  # Return JSON response



@app.route('/remove-blood-donation', methods=['POST'])
def remove_blood_donation():
    data = request.get_json()
    donation_id = data.get('donation_id')
    if not donation_id:
        return jsonify({"error": "Missing donation ID"}), 400
    success = Patients().deleteDonation(donation_id)
    if success:
        return jsonify({"message": "Donation removed successfully"}), 200
    else:
        return jsonify({"error": "Failed to remove donation"}), 500
    


@app.route('/mark-blood-donation-done', methods=['POST'])
def mark_blood_donation_done():
    data = request.get_json()
    donation_id = data.get('donation_id')
    if not donation_id:
        return jsonify({"error": "Missing donation ID"}), 400
    success = Patients().markDonationAsDone(donation_id)
    if success:
        return jsonify({"message": "Donation marked as done."}), 200
    else:
        return jsonify({"error": "Failed to update status."}), 500


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))  # 🔄 Redirect to login page










@app.route('/post_patient_donate', methods=['POST'])
def post_patient_donate():
    data = request.get_json()
    donor_id = data.get('donor_id')
    donor_name = data.get('donor_name')
    donor_age = data.get('donor_age')
    donor_city = data.get('donor_city')
    donor_contact = data.get('donor_contact')
    donor_email = data.get('donor_email')
    donor_bloodtype = data.get('donor_bloodtype')

    print(f"📩 Received Data: {data}")  # Debugging input data

    patients = Patients()

    

    success = patients.insert_donation(donor_id,donor_name, donor_age, donor_city,donor_contact,donor_email,donor_bloodtype)
    
    if success:
        print("✅ Donation Succesfully Recorded!")
        return jsonify({'status': 'success', 'message': 'Donation Succesfully Recorded!'})
    else:
        print("❌ Failed to register user in Supabase. Check logs for errors.")
        return jsonify({'status': 'error', 'message': 'Failed to register user!'})





# /get-donors

@app.route('/get-donors', methods=['GET'])
def fetch_donors():
    data = Patients().fetchAllDonation()
    return jsonify(data)



@app.route('/createPatientAccount', methods=['POST'])
def createPatientAccount():
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON data received'}), 400

    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')

    print(f"📩 Received Data: {data}")  # Debugging input data

    patients = Patients()

    # 🔍 Check Database Connection
    try:
        conn = patients.conn  # Corrected to use `patients.conn` instead of `patients.connection`
        if conn is None:
            print("❌ Database connection failed!")
            return jsonify({'status': 'error', 'message': 'Database connection failed!'})
    except Exception as e:
        print(f"❌ Error checking database connection: {e}")
        return jsonify({'status': 'error', 'message': 'Error connecting to database!'})

    if patients.email_exists(email):
        print(f"❌ Email '{email}' already exists.")
        return jsonify({'status': 'error', 'message': 'Email already exists!'})

    success = patients.create_patient_account(fullname, email, password)
    
    if success:
        print("✅ User registered successfully!")
        return jsonify({'status': 'success', 'message': 'User registered successfully!'})
    else:
        print("❌ Failed to register user in Supabase. Check logs for errors.")
        return jsonify({'status': 'error', 'message': 'Failed to register user!'})





@app.route("/post_login_patient", methods=['POST'])
def post_login_patient():
    """Handles patient login and session management"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    patient = Patients()  # Initialize Patients class

    # Check login
    if patient.login_patient_account(email, password):
        session_data = patient.search_patient_session(email, password)
        session_info = json.loads(session_data)

        # Store user session
        if session_info['success']:
            session['patient_id'] = session_info['account']['patient_id']
            session['email'] = session_info['account']['email']
            session.permanent = True  # Keep session active

            return jsonify({'status': 'success', 'message': 'Login successful!'})  
        else:
            return jsonify({'status': 'error', 'message': session_info['message']})

    return jsonify({'status': 'error', 'message': 'Incorrect Email or Password'})  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
