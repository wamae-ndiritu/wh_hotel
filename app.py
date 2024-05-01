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


from datetime import datetime, timedelta

@app.route('/book_room/<int:room_id>', methods=['POST'])
@login_required
def book_hotel_room(room_id):
    """
    Book Hotel Room
    """
    if request.method == 'POST':
        # Retrieve the logged-in user
        user = session['user_id']

        # Retrieve the selected room
        room = Room.query.get_or_404(room_id)
        hotel = Hotel.query.get_or_404(room.hotel_id)
        # Retrieve form data
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']

        # Convert date strings to datetime objects
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()

        # Calculate the number of nights
        num_nights = (check_out_date - check_in_date).days

        # Determine the rate based on peak or off-peak season
        if check_in_date.month in [4, 5, 6, 7, 8, 11, 12]:
            rate = hotel.peak_season_rate
        else:
            rate = hotel.off_peak_rate

        # Calculate the booking amount
        amount = num_nights * rate

        # Calculate the check-in date
        today = datetime.now().date()
        days_until_check_in = (check_in_date - today).days

        # Apply advanced booking discount
        if 80 <= days_until_check_in <= 90:
            discount = 0.3  # 30% discount
        elif 60 <= days_until_check_in <= 79:
            discount = 0.2  # 20% discount
        elif 45 <= days_until_check_in <= 59:
            discount = 0.1  # 10% discount
        else:
            discount = 0  # No discount

        # Apply discount to the booking amount
        discounted_amount = amount - (amount * discount)

        # Create a new booking instance
        new_booking = Booking(
            user_id=user,
            room_id=room.id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            amount=discounted_amount
        )

        # Add the new booking to the database
        db.session.add(new_booking)
        db.session.commit()

        # Redirect to a success page or display a success message
        flash('Booking successful!', 'success')
        return redirect(url_for('index'))

    # Handle GET requests by rendering a form
    return redirect(url_for('index'))


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

        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'error')
            return redirect(url_for('register'))

        # Create a new user instance with hashed password
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

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
            return redirect(url_for('index'))
        else:
            # If credentials are incorrect, render the login page with an error message
            return render_template('login.html', error='Invalid username or password')

    # If request method is GET, render the login page
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Clear the User session
    """
    session.pop('user_id', None)

    # Redirect to the home page
    return redirect(url_for('index'))

# Get Profile Information
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    """
    Profile Inifo
    """
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

# Update Password
@app.route('/update_password', methods=['POST'])
@login_required
def update_password():
    """
    Update current user password
    """
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)  # Assuming you have a User model
    # Get the new password from the form
    new_password = request.form.get('new_password')
    print(new_password)
    # Update the user's password
    user.set_password(new_password)
    # Commit the changes to the database
    db.session.commit()
    flash('Password updated successfully!', 'success')
    # Redirect back to the profile page
    return redirect(url_for('profile'))

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
def go_to_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    rooms = Room.query.filter_by(hotel_id=hotel_id).all()
    current_date = datetime.now().date()
    return render_template('room_booking.html', hotel=hotel, rooms=rooms, current_date=current_date)


@app.route('/bookings', methods=['GET'])
@login_required
def list_bookings():
    bookings = Booking.query.all()
    bookings_info = []

    for booking in bookings:
        # Query the User table to get the user information
        user = User.query.get_or_404(booking.user_id)
        room = Room.query.get_or_404(booking.room_id)
        hotel = Hotel.query.get_or_404(room.hotel_id)
        num_days = (booking.check_out_date - booking.check_in_date).days
        
        # Create a dictionary containing booking details and user information
        booking_details = {
            "booking_id": booking.id,
            "user_id": booking.user_id,
            "email": user.email,
            "room": room.type,
            "city": hotel.city,
            "check_in_date": booking.check_in_date,
            "check_out_date": booking.check_out_date,
            "amount": booking.amount,
            "days": num_days
        }

        # Append the dictionary to the list
        bookings_info.append(booking_details)

    return render_template('admin_bookings.html', bookings=bookings_info)


@app.route('/user/bookings', methods=['GET'])
@login_required
def list_user_bookings():
    """
    List current user bookings
    """
    user_id = session['user_id']
    user_bookings = Booking.query.filter_by(user_id=user_id).all()
    user_bookings_with_hotel_info = []

    for booking in user_bookings:
        # Calculate the number of days for the booking
        num_days = (booking.check_out_date - booking.check_in_date).days

        # Query the Room table to get the room information
        room = Room.query.get_or_404(booking.room_id)

        if room:
            # Query the Hotel table to get the hotel information
            hotel = Hotel.query.get_or_404(room.hotel_id)

            # Create a dictionary containing booking details and hotel information
            booking_info = {
                "booking_id": booking.id,
                "room": room.type,
                "hotel_city": hotel.city if hotel else None,  # Get hotel city if hotel exists
                # Add more hotel information as needed
                "check_in_date": booking.check_in_date,
                "check_out_date": booking.check_out_date,
                "num_days": num_days,
                "amount": booking.amount
            }

            # Append the dictionary to the list
            user_bookings_with_hotel_info.append(booking_info)

    return render_template('user_bookings.html', bookings=user_bookings_with_hotel_info)

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
