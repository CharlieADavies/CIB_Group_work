import utils.db_init

def get_as_csv():
    creds = utils.db_init.load_credentials()
    connection = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = connection.cursor()
    sql_query = "SELECT * from users"
    cursor.execute(sql_query)
    print(cursor.fetchall())


get_as_csv()
