from flask import Flask, redirect, render_template, request, jsonify, session, url_for, json, send_file


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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)