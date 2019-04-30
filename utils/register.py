import hashlib
import uuid

import utils.db_init


def hash_password(password, salt):
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def password_check(password, redo_password):
    check = False
    if password == redo_password:
        check = True
    return check


def insert_into_database(table, credential_file, vals_local):
    creds = utils.db_init.load_credentials(credential_file)
    db = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = db.cursor()
    # uuid is used to generate a random hex number
    salt = uuid.uuid4().hex
    # This encrypts the password
    vals_local[1] = hash_password(vals_local[1], salt)
    sql = "INSERT INTO " + table + \
          "(username, password, first_name, last_name, phone_no," \
          " address, post_code, role, employee_no, blue_badge, salt) VALUES " \
          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (vals_local[0], vals_local[1], vals_local[2], vals_local[3], vals_local[4],
              vals_local[5], vals_local[6], vals_local[7], vals_local[8], salt)
    cursor.execute(sql, values)
    db.commit()


def username_check(username, credential_file):
    check = False
    creds = utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    table = "user"
    sql = "SELECT * FROM " + table
    cursor = connect_sql.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    usernames = []
    for record in records:
        usernames.append(record[0])
    for username_ in usernames:
        if username_ == username:
            check = True
    return check


def check_all():
    master_check_local = False
    # add link to secretes.json file.
    check_username = username_check("temp_username", )
    check_password = password_check("password", "password")
    if check_username is True and check_password is True:
        master_check_local = True
    return master_check_local


if __name__ == '__main__':
    master_check = check_all()
    if master_check is True:
        vals = ["user", "password", "first name", "last name", "phone number", "address", "post code", "role", "employee number", "Blue badge"]
        # add link to secretes.json file.
        insert_into_database("user", "", vals)
