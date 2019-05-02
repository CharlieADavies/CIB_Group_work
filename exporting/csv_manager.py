import utils.db_init
# import pandas
# import xlsxwriter
# import dataframe


def find_rows(which_table, query):
    creds = utils.db_init.load_credentials()
    connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = connection.cursor()
    sql_rows = "SELECT COUNT(*) FROM " + which_table
    cursor.execute(sql_rows)
    get_as_csv(cursor.fetchone()[0], which_table, query)


def get_as_csv(rows, which_table, query):
    creds = utils.db_init.load_credentials()
    connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = connection.cursor()
    sql_query = query
    cursor.execute(sql_query)
    print("Table: " + which_table)
    for i in range(0, rows):
        print(cursor.fetchone())
    print("")


def get_as_csv_count(which_table, query):
    creds = utils.db_init.load_credentials()
    connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = connection.cursor()
    sql_query = query
    cursor.execute(sql_query)
    print("Table count: " + which_table)
    print(cursor.fetchone()[0])
    print("")


def select_all(which_table):
    sql_query = "SELECT * from " + which_table
    find_rows(which_table, sql_query)


def total_parking_all():
    dates = input("To query specific dates enter the range of dates you wish to view separated by a comma in the format"
                  " ' yyyy-mm-dd'")
    result = [x.strip() for x in dates.split(',')]
    if result == "":
        sql_query = "SELECT COUNT(*) FROM bookings"
    else:
        sql_query = "SELECT COUNT(*) FROM bookings WHERE booking_date BETWEEN " + "'" + result[0] + "'" + "AND" + "'" \
                    + result[1] + "'"
    get_as_csv_count("bookings", sql_query)


def total_parking_specific():
    employee = input("Enter username of employee you wish to view")
    dates = input("To query specific dates enter the range of dates you wish to view separated by a comma in the format"
                  " 'yyyy-mm-dd'")
    result_date = [x.strip() for x in dates.split(',')]
    sql_query = "SELECT COUNT(*) FROM bookings WHERE booking_date BETWEEN " + "'" + result_date[0] + "'" + \
                "AND" + "'" + result_date[1] + "'" + "AND username = " + "'" + employee + "'"
    get_as_csv_count("bookings", sql_query)


def total_parking_multiple():
    employee = input("Enter username of employees you wish to view separated by a comma")
    dates = input("To query specific dates enter the range of dates you wish to view separated by a comma in the format"
                  " 'yyyy-mm-dd'")
    result_date = [x.strip() for x in dates.split(',')]
    result_emp = [x.strip() for x in employee.split(',')]
    sql_query = "SELECT COUNT(*) FROM bookings WHERE booking_date BETWEEN " + "'" + result_date[0] + "'" + \
                "AND" + "'" + result_date[1] + "'"
    sql_query += "AND username = " + "'" + result_emp[1] + "'"
    for i in range(len(result_emp)):
        sql_query += "OR username = " + "'" + result_emp[i] + "'"
    get_as_csv_count("bookings", sql_query)


def all_badge_colours():
    sql_query = "SELECT bookings.*, users.badge FROM bookings INNER JOIN users ON bookings.username = users.username" \
                " GROUP BY users.badge"
    find_rows("bookings", sql_query)


def one_badge_colour():
    colour = input("Enter the colour badge you wish to view.")
    sql_query = "SELECT bookings.*, users.badge FROM bookings INNER JOIN users ON bookings.username = users.username" \
                " WHERE badge = " + "'" + colour.upper() + "'" + "GROUP BY users.badge"
    find_rows("users WHERE badge = " + "'" + colour + "'", sql_query)


def multiple_badge_colours():
    colours = input("Enter badge colours you wish to view separated by a comma")
    result_colours = [x.strip() for x in colours.split(',')]
    sql_query = "SELECT bookings.*, users.badge FROM bookings INNER JOIN users ON bookings.username = users.username" \
                " WHERE badge "
    sql_query += "=" + "'" + result_colours[1] + "'"
    for i in range(len(result_colours)):
        sql_query += "OR badge = " + "'" + result_colours[i] + "'"
        find_rows("bookings", sql_query)


select_all("users")
select_all("vehicles")
select_all("bookings")
select_all("badge_colours")

total_parking_all()

total_parking_specific()

total_parking_multiple()

all_badge_colours()

one_badge_colour()

multiple_badge_colours()


