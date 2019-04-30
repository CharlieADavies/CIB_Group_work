CREATE TABLE user
(
    username      VARCHAR(50),
    password      VARCHAR(50),
    first_name    VARCHAR(50),
    last_name     VARCHAR(50),
    phone_no      VARCHAR(50),
    address       VARCHAR(250),
    post_code     VARCHAR(50),
    role          VARCHAR(50),
    employee_no   VARCHAR(50),
    is_blue_badge tinyint(1),
    salt          VARCHAR(45),
    PRIMARY KEY (username)
);

create table booking
(
    booking_ref          VARCHAR(50),
    username             VARCHAR(50),
    booking_time         TIME,
    vehicle_registration VARCHAR(50),
    PRIMARY KEY (booking_ref),
    FOREIGN KEY (username) REFERENCES user (username),
    FOREIGN KEY (vehicle_registration) REFERENCES parking_form (vehicle_registration)
);

create table vehicles
(
    username             VARCHAR(50),
    electric_vehicle     tinyint(1),
    vehicle_registration VARCHAR(50),
    vehicle_make         VARCHAR(50),
    working_timetable    VARCHAR(50),
    is_blue_badge        BOOLEAN,
    PRIMARY KEY (vehicle_registration),
    FOREIGN KEY (username) REFERENCES user (username)
);

drop table parking_form