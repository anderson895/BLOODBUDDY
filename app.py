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


@app.route('/patient/home_patient')
def home_patient():
    if 'patient_id' not in session:  
        return redirect(url_for('logout')) 
    return render_template('patient/home_patient.html', session=session)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))  # 🔄 Redirect to login page

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
