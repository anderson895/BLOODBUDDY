from flask import Flask, redirect, render_template, request, jsonify, session, url_for, json, send_file


app = Flask(__name__)
app.secret_key = "gdwadwad"



@app.route('/')
def landing():
    return render_template('patient.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)