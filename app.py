from flask import Flask, redirect, render_template, request, jsonify, session, url_for, json, send_file
from patients import Patients  

app = Flask(__name__)
app.secret_key = "gdwadwad"



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




@app.route('/createPatientAccount', methods=['POST'])
def createPatientAccount():
    data = request.get_json()
    fullname = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    patients = Patients()
    
    # Check if email already exists
    if patients.email_exists(email):
        return jsonify({'status': 'error', 'message': 'Email already exists!'})

    # Create account
    success = patients.createPatientAccount(fullname, email, password)
    
    if success:
        return jsonify({'status':'success','message': 'User registered successfully!'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to register user!'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)