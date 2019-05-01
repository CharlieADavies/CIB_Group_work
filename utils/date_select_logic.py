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

if __name__ == '__main__':
    check = check_date( "2019-06-25", "H:\Applications of programming\CIB\secrets.json")
    print(check)
