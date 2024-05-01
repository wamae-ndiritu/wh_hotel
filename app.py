"""
App Views
"""
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from config.db import db

app = Flask(__name__)

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://wh_hotel_dev:12345678@localhost/wh_hotel_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.secret_key = 'vfnbgibkvsdfvdlkv'

db.init_app(app)

from models.index import User, Hotel, Room, Booking, Price, Currency, ExchangeRate, Constraint


def login_required(func):
    """
    Login required decorator
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # User is not logged in, redirect to login page
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function

@app.route('/book_room/<int:room_id>', methods=['POST'])
@login_required
def book_hotel_room(room_id):
    # Booking logic here
    pass

@app.route('/')
def index():
    """
    Homepage
    """
    # Fetch all hotels from the database
    hotels = Hotel.query.all()

    # Pass the list of hotels to the template
    return render_template('index.html', hotels=hotels)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Create a new user instance
        new_user = User(username=username, email=email, password=password)

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login user - Session authentication
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database and if the password is correct
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # If credentials are correct, set session variable and redirect to home page
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            # If credentials are incorrect, render the login page with an error message
            return render_template('login.html', error='Invalid username or password')

    # If request method is GET, render the login page
    return render_template('login.html')

@app.route('/admin/dashboard')
def dashboard():
    """
    Admin Dashboard
    """
    # Fetch data for dashboard widgets (example data)
    num_hotels = 10
    num_room_types = 5
    total_bookings = 100
    total_revenue = 5000

    # Render the dashboard.html template and pass the data
    return render_template('admin_dashboard.html', num_hotels=num_hotels, num_room_types=num_room_types, total_bookings=total_bookings, total_revenue=total_revenue)


@app.route('/admin/add_hotel', methods=['GET', 'POST'])
def add_hotel():
    """
    Create Hotel
    """
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        capacity = request.form['capacity']
        peak_season_rate = request.form['peak_season_rate']
        off_peak_rate = request.form['off_peak_rate']
        image_path = None

        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
            else:
                image_path = None
        else:
            image_path = None
        
        # Create a new hotel
        hotel = Hotel(city=city, capacity=capacity, peak_season_rate=peak_season_rate, off_peak_rate=off_peak_rate, city_image_url=image_path)
        db.session.add(hotel)
        db.session.commit()
        return 'Hotel added successfully!'
    else:
        return render_template('add_hotel.html')


@app.route('/admin/hotels_listing')
def admin_hotels():
    """
    Admin list all hotels
    """
    hotels = Hotel.query.all()
    return render_template('admin_listing.html', hotels=hotels)

# View a single hotel
@app.route('/admin/hotel/<int:hotel_id>')
def view_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    rooms = Room.query.filter_by(hotel_id=hotel_id).all()
    return render_template('view_hotel.html', hotel=hotel, rooms=rooms)

# Edit a hotel
@app.route('/admin/hotel/<int:hotel_id>/edit', methods=['GET', 'POST'])
def edit_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if request.method == 'POST':
        # Update hotel details
        hotel.city = request.form['city']
        hotel.city_image_url = request.form['city_image_url']
        hotel.capacity = request.form['capacity']
        hotel.peak_season_rate = request.form['peak_season_rate']
        hotel.off_peak_rate = request.form['off_peak_rate']
        db.session.commit()
        flash('Hotel updated successfully!', 'success')
        return redirect(url_for('admin_hotels'))
    return render_template('edit_hotel.html', hotel=hotel)

# Delete a hotel
@app.route('/admin/hotel/<int:hotel_id>/delete')
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deleted successfully!', 'success')
    return redirect(url_for('admin_hotels'))


@app.route('/admin/add_room/<int:hotel_id>', methods=['GET', 'POST'])
def add_room(hotel_id):
    """
    Create Hotel Room
    """
    if request.method == 'POST':
        type = request.form['type']

        hotel = Hotel.query.get(hotel_id)
        
        room = Room(type=type, hotel_id=hotel_id)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('view_hotel', hotel_id=hotel_id))


@app.route('/hotels', methods=['GET'])
def list_hotels():
    """
    Fetch all hotels from the database
    """
    hotels = Hotel.query.all()
    return render_template('list_hotels.html', hotels=hotels)

@app.route('/hotel/<int:hotel_id>/booking', methods=['GET', 'POST'])
def book_room(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    rooms = Room.query.filter_by(hotel_id=hotel_id).all()
    current_date = datetime.now().date()

    if request.method == 'POST':
        # Logic to book the room goes here
        # For example, you might add the booked room to a database table

        flash('Room booked successfully!', 'success')
        return redirect(url_for('index'))
    else:
        return render_template('room_booking.html', hotel=hotel, rooms=rooms, current_date=current_date)


@app.route('/rooms')
def rooms():
    # Your rooms logic here
    return render_template('rooms.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    # Your payment logic here
    return render_template('payment.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
