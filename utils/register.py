import hashlib
import uuid

import utils.db_init


def hash_password(password, salt):
    # uuid is used to generate a random number
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def password_check(password, redo_password):
    check = False
    if password == redo_password:
        check = True
    return check


def insert_into_database(table, credential_file, vals):
    creds = utils.db_init.load_credentials(credential_file)
    db = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    cursor = db.cursor()
    salt = uuid.uuid4().hex
    sql = "INSERT INTO " + table + \
          "(username, password, first_name, last_name, phone_no," \
          " address, post_code, role, employee_no, blue_badge, salt) VALUES " \
          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8], salt)
    cursor.execute(sql, values)
    db.commit()


def email_check(email, credential_file):
    check = False
    creds = utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    table = "user"
    sql = "SELECT * FROM " + table
    connect_sql.cursor.execute(sql)
    records = connect_sql.cursor.fetchall()
    emails = []
    for record in records:
        emails.append(record[0])
    for email_ in emails:
        if email_ == email:
            check = True
    return check


def check_all():
    master_check_local = False
    # add link to secretes.json file.
    check_email = email_check("email@gmail.com", )
    check_password = password_check("password", "password")
    if check_email is True and check_password is True:
        master_check_local = True
    return master_check_local


if __name__ == '__main__':
    master_check = check_all()
    if master_check is True:
        vals = ["user", "password", "first name", "last name", "phone number", "address", "post code", "role", "employee number", "Blue badge"]
        # add link to secretes.json file.
        insert_into_database("user", "", vals)
