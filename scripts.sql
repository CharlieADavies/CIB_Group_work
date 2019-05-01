CREATE TABLE users
(
    username      VARCHAR(50),
    password      VARCHAR(250),
    first_name    VARCHAR(50),
    last_name     VARCHAR(50),
    phone_no      VARCHAR(50),
    address       VARCHAR(250),
    post_code     VARCHAR(50),
    role          VARCHAR(50),
    employee_no   VARCHAR(50),
    badge         VARCHAR(50),
    is_blue_badge tinyint(1),
    salt          VARCHAR(45),
    PRIMARY KEY (username),
    FOREIGN KEY (badge) REFERENCES badge_colours (badge)
);

create table vehicles
(
    username             VARCHAR(50),
    electric_vehicle     tinyint(1),
    vehicle_registration VARCHAR(50),
    vehicle_make         VARCHAR(50),
    PRIMARY KEY (vehicle_registration),
    FOREIGN KEY (username) REFERENCES users (username)
);

create table bookings
(
    booking_ref          integer auto_increment,
    username             VARCHAR(50),
    booking_date         DATE,
    vehicle_registration VARCHAR(50),
    start_time           INTEGER default 8,
    end_time             INTEGER default 20,
    PRIMARY KEY (booking_ref),
    FOREIGN KEY (username) REFERENCES users (username),
    FOREIGN KEY (vehicle_registration) REFERENCES vehicles (vehicle_registration)
);

CREATE TABLE badge_colours
(
    badge       VARCHAR(50),
    first_week  DATE,
    second_week DATE,
    third_week  DATE,
    fourth_week DATE,
    fifth_week  DATE,
    PRIMARY KEY (badge)
);

INSERT INTO users(username, password, first_name, last_name, phone_no, address, post_code, role, employee_no, badge,
                  is_blue_badge, salt)
VALUES ("jacob.smith@gmail.com",
        "02bf31f440b5941e698cc2e7e682627b211932ca9d10c62a07623a8d4f2e107a:97e89558ccbc4bb3a55162ddf9e05879", "Jacob",
        "Smith", "3953604440", "67 Hollow Ridge Trail", "SP3 4UN", "Manager", "01", "RED", 0,
        "97e89558ccbc4bb3a55162ddf9e05879"),
       ("ardra.denford@yahoo.co.uk",
        "cf0af64566290ba259091de0f73b22ca642693fefc693ade4e9313111c79d4df:eb2b0ffe968d4b2fb10ef4245b5b729a", "Ardra",
        "Denford", "1491335319", "1062 Northwestern Place", "NN6 0QQ", "Facilities", "02", "DARK GREEN", 0,
        "eb2b0ffe968d4b2fb10ef4245b5b729a"),
       ("merrile.fuster@gmail.co.uk",
        "6fe18e21f04455bba324aa597c7426889e9e9a2d8669e5e65e234b71d7e44394:b60054c895404f808d7736e18258e4ad", "Merrile",
        "Fuster", "9601526599", "1889 School Alley", "LL17 0AW", "Employee", "03", "GREY", 0,
        "b60054c895404f808d7736e18258e4ad"),
       ("richard.chop@gmail.com",
        "00eeefa6423aca2237e080e18c0307cd8c6675b75ee25cd3b6bce8262a7e9dd8:2f6a903a10224792ae6a09687d370748", "Richard",
        "Chopping", "7586192639", "3876 Hallows Alley", "TS18 5LN", "System Administrator", "04", "PURPLE", 1,
        "2f6a903a10224792ae6a09687d370748"),
       ("al.n.murford@yahoo.co.uk",
        "b0e037b4ce763ba90a1958aff4ef3032eb1d5256f94480c8d7812b3448b2e09f:86a3497334934a5dbace72443b6741e5", "Alvina",
        "Murford", "8475882191", "5198 Scofield Court", "LE6 0JA", "Facilities", "05", "ORANGE", 0,
        "86a3497334934a5dbace72443b6741e5");



INSERT INTO vehicles(username, electric_vehicle, vehicle_registration, vehicle_make)
VALUES ("jacob.smith@gmail.com", 1, "TIG 8184", "Ford"),
       ("ardra.denford@yahoo.co.uk", 0, "CSZ 2178", "Mercedes"),
       ("merrile.fuster@gmail.co.uk", 0, "JGZ 5677", "Hyundi"),
       ("merrile.fuster@gmail.co.uk", 1, "BJ57 TWM", "BMW"),
       ("richard.chop@gmail.com", 0, "WHZ 1558", "Vauxhall"),
       ("al.n.murford@yahoo.co.uk", 0, "DRS 318D", "Ford");

INSERT INTO bookings (username, booking_date, vehicle_registration)
VALUES ("jacob.smith@gmail.com", "2018-06-25", "TIG 8184"),
       ("ardra.denford@yahoo.co.uk", "2018-09-09", "CSZ 2178"),
       ("merrile.fuster@gmail.co.uk", "2018-10-18", "JGZ 5677"),
       ("richard.chop@gmail.com", "2018-09-20", "WHZ 1558"),
       ("al.n.murford@yahoo.co.uk", "2018-12-05", "DRS 318D");

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


select *
from bookings