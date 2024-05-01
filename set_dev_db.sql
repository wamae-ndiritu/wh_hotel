-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS wh_hotel;
CREATE USER IF NOT EXISTS 'wh_hotel_dev'@'localhost' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON `wh_hotel`.* TO 'wh_hotel_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'wh_hotel_dev'@'localhost';
FLUSH PRIVILEGES;

