"""
Database Models
"""
from config.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    city_image_url = db.Column(db.String(255))
    capacity = db.Column(db.Integer, nullable=False)
    standard_room_capacity = db.Column(db.Integer, default=0.3*capacity)
    double_room_capacity = db.Column(db.Integer, default=0.5*capacity)
    family_room_capacity = db.Column(db.Integer, default=0.2*capacity)
    peak_season_rate = db.Column(db.Float, nullable=False)
    off_peak_rate = db.Column(db.Float, nullable=False)
    rooms = db.relationship('Room', backref='hotel', lazy=True)

    def __repr__(self):
        return '<Hotel %r>' % self.name


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    bookings = db.relationship('Booking', backref='room', lazy=True)

    def __repr__(self):
        return '<Room %r>' % self.type


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<Booking %r>' % self.id


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Price %r>' % self.id


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(3), nullable=False)
    exchange_rates = db.relationship('ExchangeRate', backref='currency', lazy=True)

    def __repr__(self):
        return '<Currency %r>' % self.code


class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    rate = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<ExchangeRate %r>' % self.id


class Constraint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Constraint %r>' % self.name
