import utils.db_init
import pandas
import xlsxwriter
import dataframe


def find_rows(which_table):
    creds = utils.db_init.load_credentials()
    connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = connection.cursor()
    sql_rows = "SELECT COUNT(*) FROM " + which_table
    cursor.execute(sql_rows)
    get_as_csv(cursor.fetchone()[0], which_table)


def get_as_csv(rows, which_table):
    creds = utils.db_init.load_credentials()
    connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = connection.cursor()
    sql_query = "SELECT * from " + which_table
    cursor.execute(sql_query)
    print("Table: " + which_table)
    for i in range(0, rows):
        print(cursor.fetchone())
    print("")


find_rows("users")
find_rows("vehicles")
find_rows("bookings")
find_rows("badge_colours")
