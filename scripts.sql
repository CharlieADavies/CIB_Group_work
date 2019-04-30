CREATE TABLE users (
    username VARCHAR(50),
    password VARCHAR(250),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone_no VARCHAR(50),
    address VARCHAR(250),
    post_code VARCHAR(50),
    role VARCHAR(50),
    employee_no VARCHAR(50),
    badge VARCHAR(50),
    is_blue_badge tinyint(1),
    salt VARCHAR(45),
    PRIMARY KEY (username),
    FOREIGN KEY (badge) REFERENCES badge_colours(badge)
);

create table vehicles (
    username             VARCHAR(50),
    electric_vehicle     tinyint(1),
    vehicle_registration VARCHAR(50),
    vehicle_make         VARCHAR(50),
    PRIMARY KEY (vehicle_registration),
    FOREIGN KEY (username) REFERENCES users(username)
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

CREATE TABLE badge_colours (
    badge VARCHAR(50),
    first_week DATE,
    second_week DATE,
    third_week DATE,
    fourth_week DATE,
    fifth_week DATE,
    PRIMARY KEY (badge)
);

INSERT INTO users(username, password, first_name, last_name, phone_no, address, post_code, role, employee_no, badge,is_blue_badge, salt)
    VALUES ("jacob.smith@gmail.com", "Hyf754Lk", "Jacob", "Smith", "3953604440", "67 Hollow Ridge Trail", "SP3 4UN", "Manager", "01", "RED",0, "78976865422"),
           ("ardra.denford@yahoo.co.uk", "VYq0X718mm", "Ardra", "Denford", "1491335319", "1062 Northwestern Place", "NN6 0QQ", "Facilities", "02", "DARK GREEN",0, "3456490798"),
           ("merrile.fuster@gmail.co.uk", "yyHs3AJUvfh", "Merrile", "Fuster", "9601526599", "1889 School Alley", "LL17 0AW", "Employee", "03", "GREY",0, "67576879075"),
           ("richard.chop@gmail.com", "yLaDhkyS", "Richard", "Chopping", "7586192639", "3876 Hallows Alley", "TS18 5LN", "System Administrator", "04", "PURPLE", 1, "786574365475"),
           ("al.n.murford@yahoo.co.uk", "eK5V5deg9Y", "Alvina", "Murford", "8475882191", "5198 Scofield Court", "LE6 0JA", "Facilities", "05", "ORANGE",0, "9887654657689");



INSERT INTO vehicles(username, electric_vehicle, vehicle_registration, vehicle_make)
    VALUES ("jacob.smith@gmail.com", 1, "TIG 8184", "Ford"),
           ("ardra.denford@yahoo.co.uk", 0, "CSZ 2178", "Mercedes"),
           ("merrile.fuster@gmail.co.uk", 0, "JGZ 5677", "Hyundi"),
           ("merrile.fuster@gmail.co.uk", 1, "BJ57 TWM", "BMW"),
           ("richard.chop@gmail.com", 0, "WHZ 1558", "Vauxhall"),
           ("al.n.murford@yahoo.co.uk", 0, "DRS 318D", "Ford");

INSERT INTO bookings (booking_ref, username, booking_date, vehicle_registration)
    VALUES ("BK0027", "jacob.smith@gmail.com", "2018-06-25", "TIG 8184"),
           ("BK0005", "ardra.denford@yahoo.co.uk", "2018-09-09", "CSZ 2178"),
           ("BK0128", "merrile.fuster@gmail.co.uk", "2018-10-18", "JGZ 5677"),
           ("BK0059", "richard.chop@gmail.com", "2018-09-20", "WHZ 1558"),
           ("BK1756", "al.n.murford@yahoo.co.uk", "2018-12-05", "DRS 318D");

INSERT INTO badge_colours(badge, first_week, second_week, third_week, fourth_week, fifth_week)
    VALUES ("RED", "2018-06-25", "2018-07-30", "2018-09-03", "2018-10-08", "2018-11-12"),
           ("LIGHT PINK", "2018-06-25", "2018-07-30", "2018-09-03", "2018-10-08", "2018-11-12"),
           ("DARK GREEN", "2018-07-02", "2018-08-06", "2018-09-10", "2018-10-15", "2018-11-19"),
           ("WHITE", "2018-07-02", "2018-08-06", "2018-09-10", "2018-10-15", "2018-11-19"),
           ("GREY", "2018-07-09", "2018-08-13", "2018-09-17", "2018-10-22", "2018-11-26"),
           ("DARK BLUE", "2018-07-09", "2018-08-13", "2018-09-17", "2018-10-22", "2018-11-26"),
           ("BROWN", "2018-07-16", "2018-08-20", "2018-09-24", "2018-10-29", "2018-12-03"),
           ("PURPLE", "2018-07-16", "2018-08-20", "2018-09-24", "2018-10-29", "2018-12-03"),
           ("YELLOW", "2018-07-23", "2018-08-27", "2018-10-01", "2018-11-05", "2018-12-10"),
           ("ORANGE", "2018-07-23", "2018-08-27", "2018-10-01", "2018-11-05", "2018-12-10");

DROP TABLE users;
DROP TABLE vehicles;
DROP TABLE bookings;
DROP TABLE badge_colours;