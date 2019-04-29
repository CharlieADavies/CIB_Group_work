create table user
(
    username      varchar(50) primary key,
    e_address     varchar(50),
    password      varchar(50),
    role          varchar(50) default "EMPLOYEE",
    phone_no      varchar(50),
    first_name    varchar(50),
    last_name     varchar(50),
    employee_no   varchar(50),
    address       varchar(250),
    is_blue_badge TINYINT(1)  default 0
);

