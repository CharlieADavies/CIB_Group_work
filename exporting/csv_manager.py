import utils.db_init


def get_as_csv(rows, which_table):
    creds = utils.db_init.load_credentials()
    connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = connection.cursor()
    sql_query = "SELECT * from " + which_table
    cursor.execute(sql_query)
    for i in range(0, rows):
        print(cursor.fetchone())


def find_rows(which_table):
    creds = utils.db_init.load_credentials()
    connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = connection.cursor()
    sql_rows = "SELECT COUNT(*) FROM " + which_table
    cursor.execute(sql_rows)
    return cursor.fetchone()[0]


print("Table: Users")
find_rows("users")
get_as_csv(find_rows("users"), "users")
print("")

print("Table: Vehicles")
find_rows("vehicles")
get_as_csv(find_rows("vehicles"), "vehicles")
print("")

print("Table: Bookings")
find_rows("bookings")
get_as_csv(find_rows("bookings"), "bookings")
print("")

print("Table: Badge Colours")
find_rows("badge_colours")
get_as_csv(find_rows("badge_colours"), "badge_colours")
