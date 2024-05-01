# World Hotels Web Application

## Overview

This is a web application for managing hotels, bookings, and user profiles. It allows users to browse hotels, book rooms, and manage their bookings. Admin users have additional privileges to add and manage hotels.

## Features

- User authentication: Users can sign up, log in, and log out.
- Hotel management: Admin users can add, view, update, and delete hotels.
- Booking management: Users can book rooms in hotels, view their bookings, and cancel bookings.
- Profile management: Users can update their profile information and change their password.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Jinja2
- HTML/CSS (Tailwind CSS)
- MySQL

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/world-hotels.git

2. Navigate to projects directory
```bash
cd wh_hotel

3. Create virtual Environment
On Windows
```
python -m venv venv
```
On Linux/MacOS
```
python3 -m venv venv
```

4. Activate virtual environment
On Windows
```
venv\Scripts\activate
```
On Linux/MacOS
```
Source venv/bin/activate
```

5. Install dependencies using
```
pip install -r requirements.txt
```

6. Set up your database:
> Note the Flask application has been configured to connect to a MYSQL Database and changing to other DBMS may require some slight change in the configuration.
> Create a MySQL database for the application. - [MYSQL DUMP](./wh_hotel_dump.sql) provides the initial database setup. It includes the SQL Queries for creating all the necessary database tables and inserting the data that was used in the testing.
- The following are the main activities done;
	- Create a user called `wh_hotel_dev` with password `12345678`: This user will be used by the application to connect to the database
	- Create a new database called `wh_hotel_db`: This is the database used by the applcation
	- Create tables inside `wh_hotel_db`
	- Insert relevant data including users, hotels and bookings

> To set up your database, import the `wh_hotel_dump.sql` to your database and execute it. This will perfom all the operations above and you'll be good to go.

7. Run the application
```
python -m app
```
> Always ensure you are running the app from the root directory of the project `wh_hotel`
