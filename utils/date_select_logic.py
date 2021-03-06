import datetime

import utils.db_init


def convert_to_string(date):
    time_return = datetime.datetime.strptime(
        str(date), "%Y-%m-%d")
    time_return = "{:%Y-%m-%d}".format(time_return)
    return time_return


def check_date(date, credential_file):
    check = True
    creds = utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    table = "bookings"
    sql = "SELECT * FROM " + table
    cursor = connect_sql.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    dates = []
    for record in records:
        check_record = convert_to_string(record[2])
        dates.append(record[2])
        count = 0
        if date == check_record:
            count = count + 1
            if count > 1000:
                check = False
                break
            else:
                check = True
            print(check)
        else:
            check = True
    return check


def insert_into_database(credential_file, date, username):
    creds = utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    table = "users"
    sql = "SELECT * FROM " + table
    cursor = connect_sql.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    for record in records:
        if record[0] == username:

            reg = ""
            sql = "SELECT * FROM " + "vehicles"
            cursor = connect_sql.cursor()
            cursor.execute(sql)
            reg_records = cursor.fetchall()
            for reg_record in reg_records:
                if reg_record[0] == username:
                    reg = reg_record[2]

            sql = "SELECT * FROM " + "bookings"
            cursor = connect_sql.cursor()
            cursor.execute(sql)
            reg_records = cursor.fetchall()
            id = []
            for reg_record in reg_records:
                id.append(reg_record[0])
            new_id = max(id) + 1
            values = (new_id, username, date, reg)
            sql = "INSERT INTO " + "bookings" + \
                  "(booking_ref, username, booking_date, vehicle_registration) VALUES " \
                  "(%s, %s, %s, %s)"
            cursor.execute(sql, values)
            connect_sql.commit()


def check_if_booked(user, credential_file):
    creds = utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    reg = ""
    sql = "SELECT * FROM " + "bookings"
    cursor = connect_sql.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    dates_booked = []
    for record in records:
        if record[1] == user:
            date = convert_to_string(record[2])
            dates_booked.append(date)
    return dates_booked


def get_date_time(user, credential_file):
    creds = utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    reg = ""
    sql = "SELECT * FROM " + "bookings"
    cursor = connect_sql.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    dates_booked = []
    time_booked = []
    end_times = []
    for record in records:
        if record[1] == user:
            date = convert_to_string(record[2])
            dates_booked.append(date)
            time_booked.append(record[4])
            end_times.append(record[5])
    master_list = []
    master_list.append(dates_booked)
    master_list.append(time_booked)
    master_list.append(end_times)
    return master_list
