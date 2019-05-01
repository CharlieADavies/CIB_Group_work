import hashlib
import uuid
import utils.db_init


def hash_password(password, salt):
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def insert_into_database(table, credential_file, vals_local):
    creds = utils.db_init.load_credentials(credential_file)
    db = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = db.cursor()
    # uuid is used to generate a random hex number
    salt_local = uuid.uuid4().hex
    # This encrypts the password
    vals_local[1] = hash_password(vals_local[1], salt_local)
    sql = "INSERT INTO " + table + \
          "(username, password, first_name, last_name, phone_no," \
          " address, post_code, role, employee_no, badge, is_blue_badge, salt) VALUES " \
          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (vals_local[0], vals_local[1], vals_local[2], vals_local[3], vals_local[4],
              vals_local[5], vals_local[6], vals_local[7], vals_local[8], vals_local[9], vals_local[10], salt_local)
    cursor.execute(sql, values)
    db.commit()


def username_check(username, credential_file):
    check = True
    creds = utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    table = "users"
    sql = "SELECT * FROM " + table
    cursor = connect_sql.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    usernames = []
    for record in records:
        usernames.append(record[0])
    for username_ in usernames:
        if username_ == username:
            check = False
    return check


def email_check(username):
    check = False
    if "@" in username:
        check = True
    return check


def check_all(username_local, path):
    master_check_local = False
    # add link to secretes.json file.
    check_username = username_check(username_local, path)
    check_email = email_check(username_local)
    if check_username is True and check_email is True:
        master_check_local = True
    return master_check_local


if __name__ == '__main__':
    # change these to the entry fields values.
    vals = ["towjdklam@gmail.com", "password", "John", "Smith", "07284192871", "8 Red Road", "BH8 8FT", "Manager",
            "06", None, "0"]
    username = vals[0]
    master_check = check_all(username)
    if master_check is True:
        # add link to secretes.json file.
        insert_into_database("users", "", vals)
    else:
        print("Failed")
