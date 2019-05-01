import utils.db_init

def users_with_bookings_in_range(range=1):
    """
    Gets all users with a booking in the next 3 days
    :return: column headers, column names
    """

    creds = utils.db_init.load_credentials(f="../secrets.json")
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = connect_sql.cursor()
    cursor.execute("""select users.username, booking_date, phone_no, bookings.vehicle_registration
from users
         inner join vehicles on users.username = vehicles.username
         inner join bookings on users.username = bookings.username
where CURDATE() >= (bookings.booking_date - interval """+str(range)+""" day) AND curdate() < bookings.booking_date""")
    return cursor.column_names, cursor.fetchall()


def assign_parking_spaces(cols):
    assert len(cols) <= 1000, "More users than parking spaces"
    for index, col in enumerate(cols):
        send_alert(col)


def send_alert(text):
    """Placeholder function for the function that will be used to text or email users"""
    print(text)


if __name__ == "__main__":
    assign_parking_spaces(users_with_bookings_in_range()[1])
