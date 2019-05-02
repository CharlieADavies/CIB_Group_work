"""
database functionality common to both flask and tkinter
"""
import datetime
import random

import mysql.connector

import utils.db_init

POSSIBLE_ROLES = ['user', 'facilities', 'sys_add', 'banned']


def get_user_info(username, file_p=None):
    if file_p is None:
        creds = utils.db_init.load_credentials()
    else:
        creds = utils.db_init.load_credentials(file_p)
    select_query = """
        SELECT username, first_name, last_name, phone_no, managed_by FROM users where username='""" + username + "'"
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(select_query)
        return cursor.fetchall()

    except mysql.connector.Error as e:
        print("Failed to select ", e)
        return False

def insert_vehicle(username, is_electric, vehicle_reg, vehicle_make):
    creds = utils.db_init.load_credentials()

    sql_insert_query = """ 
    INSERT INTO `vehicles`
    (`username`, `electric_vehicle`, `vehicle_registration`, `vehicle_make`) VALUES (%s,%s,%s,%s)
"""
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(sql_insert_query, (username, is_electric, vehicle_reg, vehicle_make))
        print("Row inserted into vehicle table")
        return True

    except mysql.connector.Error as e:
        print("Failed to insert", e)
        return False


def get_pending_users():
    creds = utils.db_init.load_credentials()
    sql_insert_query = """
    SELECT * FROM users
    WHERE role='pending'
    """
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(sql_insert_query, )
        print("Fetching all pending users")
        return cursor.fetchall()

    except mysql.connector.Error as e:
        print("Failed to select", e)
        return False


def set_user_role(username, role):
    # TO let the sys ad approve a user they need to change their role to uer
    assert role in POSSIBLE_ROLES, "role is not a valid role"
    creds = utils.db_init.load_credentials()
    sql_insert_query = """
    UPDATE users
    SET role = %s
    WHERE username = %s
    """
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(sql_insert_query, (username, role))
        print("Print role for " + username + " set to " + role)
        return True

    except mysql.connector.Error as e:
        print("Failed to update", e)
        return False


def validate_booking(username, booking_date: datetime.datetime):
    query = _fetch_booking_info(username)
    booking_date = booking_date.date()
    if not query:
        return False
    for row in query:
        dates = list(row)
        first_date = dates[0]

        if booking_date.day == first_date.day and booking_date.month == first_date.month and booking_date.year == first_date.year:
            return False, "You already have a booking for that date"
        for p_r_date in dates[1:]:
            if p_r_date <= booking_date <= p_r_date + datetime.timedelta(days=7):
                return False, "This collides with your park and ride dates"
        return True


def _fetch_booking_info(username):
    creds = utils.db_init.load_credentials()
    sql_insert_query = """
        SELECT booking_date, first_week,second_week,third_week,fourth_week,fifth_week FROM bookings
        INNER JOIN users u on bookings.username = u.username
        inner join badge_colours b on u.badge = b.badge
        where u.username = '""" + username + "'"
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(sql_insert_query)

        return cursor.fetchall()

    except mysql.connector.Error as e:
        print("Failed to select ", e)
        return False


def get_bookings_for(username, file_p=None):
    if file_p is None:
        creds = utils.db_init.load_credentials()
    else:
        creds = utils.db_init.load_credentials(file_p)
    select_query = """
        SELECT u.username, booking_date,  b.badge, first_week,second_week,third_week,fourth_week,fifth_week, bookings.start_time, bookings.end_time FROM bookings
        INNER JOIN users u on bookings.username = u.username
        inner join badge_colours b on u.badge = b.badge
        where u.username = '""" + username + "'"
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(select_query)
        return cursor.fetchall()

    except mysql.connector.Error as e:
        print("Failed to select ", e)
        return False


def set_manager(username, manager_username):
    creds = utils.db_init.load_credentials()
    sql_insert_query = """
    UPDATE users
    SET managed_by = %s
    WHERE username = %s
    """
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(sql_insert_query, (manager_username, username ))
        print("manager for " + username + " set to " + manager_username)
        return True

    except mysql.connector.Error as e:
        print("Failed to update", e)
        return False


def get_managed_users(username):
    """Gets the users for whom this person manages"""
    creds = utils.db_init.load_credentials()
    select_query = """
        SELECT * FROM users WHERE managed_by = '""" + username + "'"
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(select_query)
        return cursor.fetchall()

    except mysql.connector.Error as e:
        print("Failed to select ", e)
        return False


def insert_booking(username, booking_date, vehicle_reg, start_time=8, end_time=8):
    creds = utils.db_init.load_credentials()
    sql_insert_query = """
    INSERT INTO `bookings`
    (`username`, `booking_date`, `vehicle_registration`,`start_time`,`end_time`) VALUES (%s,%s,%s,%s,%s)
    """
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(sql_insert_query, (username, booking_date, vehicle_reg, start_time, end_time))
        print("Row inserted into booking table")
        return True

    except mysql.connector.Error as e:
        print("Failed to insert", e)
        return False


def give_user_badge(username, badge_colour="RAND"):
    if badge_colour == "RAND":
        colours = ["RED", "LIGHT PINK", "DARK GREEN", "WHITE", "GREY", "DARK_BLUE", "BROWN", "PURPLE", "YELLOW",
                   "ORANGE"]
        random.shuffle(colours)
        badge_colour = colours[0]

    creds = utils.db_init.load_credentials()
    sql_insert_query = """
    UPDATE users
    SET badge = %s
    WHERE username = %s
    """
    try:
        connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor()
        cursor.execute(sql_insert_query, (username, badge_colour))
        print("Print badge colour for " + username + " set to " + badge_colour)
        return True

    except mysql.connector.Error as e:
        print("Failed to update", e)
        return False


if __name__ == "__main__":
    print(set_manager("merrile.fuster@gmail.co.uk", "jacob.smith@gmail.com"))
