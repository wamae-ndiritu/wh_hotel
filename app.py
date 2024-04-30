# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/')
def index():
    # Your homepage logic here
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Your login logic here
    return render_template('login.html')

@app.route('/rooms')
def rooms():
    # Your rooms logic here
    return render_template('rooms.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    # Your payment logic here
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
