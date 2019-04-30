CREATE TABLE users 
(
    username VARCHAR(50),
    password VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone_no VARCHAR(50),
    address VARCHAR(250),
    post_code VARCHAR(50),
    role VARCHAR(50),
    employee_no VARCHAR(50),
    is_blue_badge tinyint(1),
    salt VARCHAR(45),
    PRIMARY KEY (username)
);

create table vehicles
(
    username             VARCHAR(50),
    electric_vehicle     tinyint(1),
    vehicle_registration VARCHAR(50),
    vehicle_make         VARCHAR(50),
    is_blue_badge        tinyint(1),
    PRIMARY KEY (vehicle_registration),
    FOREIGN KEY (username) REFERENCES users (username)
);

create table bookings (
    booking_ref VARCHAR(50),
    username VARCHAR(50),
    booking_date DATE,
    vehicle_registration VARCHAR(50),
    PRIMARY KEY (booking_ref),
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (vehicle_registration) REFERENCES vehicles(vehicle_registration)
);

INSERT INTO users(username, password, first_name, last_name, phone_no, address, post_code, role, employee_no, is_blue_badge, salt)
    VALUES ("jacob.smith@gmail.com", "Hyf754Lk", "Jacob", "Smith", "3953604440", "67 Hollow Ridge Trail", "SP3 4UN", "Manager", "01", 0, "78976865422"),
           ("ardra.denford@yahoo.co.uk", "VYq0X718mm", "Ardra", "Denford", "1491335319", "1062 Northwestern Place", "NN6 0QQ", "Facilities", "02", 0, "3456490798"),
           ("merrile.fuster@gmail.co.uk", "yyHs3AJUvfh", "Merrile", "Fuster", "9601526599", "1889 School Alley", "LL17 0AW", "Employee", "03", 0, "67576879075"),
           ("richard.chop@gmail.com", "yLaDhkyS", "Richard", "Chopping", "7586192639", "3876 Hallows Alley", "TS18 5LN", "System Administrator", "04", 1, "786574365475"),
           ("al.n.murford@yahoo.co.uk", "eK5V5deg9Y", "Alvina", "Murford", "8475882191", "5198 Scofield Court", "LE6 0JA", "Facilities", "05", 0, "9887654657689")

INSERT INTO vehicles(username, electric_vehicle, vehicle_registration, vehicle_make, is_blue_badge)
    VALUES ("jacob.smith@gmail.com", 1, "TIG 8184", "Ford", 0),
           ("ardra.denford@yahoo.co.uk", 0, "CSZ 2178", "Mercedes", 0),
           ("merrile.fuster@gmail.co.uk", 0, "JGZ 5677", "Hyundi", 0),
           ("merrile.fuster@gmail.co.uk", 1, "BJ57 TWM", "BMW", 0),
           ("richard.chop@gmail.com", 0, "WHZ 1558", "Vauxhall", 1),
           ("al.n.murford@yahoo.co.uk", 0, "DRS 318D", "Ford", 0)

INSERT INTO bookings(booking_ref, username, booking_date, vehicle_registration)
    VALUES ("BK0027", "jacob.smith@gmail.com", "2018-11-22", "TIG 8184"),
           ("BK0005", "ardra.denford@yahoo.co.uk", "2018-08-09", "CSZ 2178"),
           ("BK0128", "merrile.fuster@gmail.co.uk", "2018-05-23", "JGZ 5677"),
           ("BK0059", "richard.chop@gmail.com", "2018-02-23", "WHZ 1558"),
           ("BK1756", "al.n.murford@yahoo.co.uk", "2018-07-23", "DRS 318D")

DROP TABLE users
DROP TABLE vehicles
DROP TABLE bookings