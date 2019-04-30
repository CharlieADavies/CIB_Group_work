import hashlib
import uuid
import utils.db_init


def hash_password(password, salt):
    # uuid is used to generate a random number
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_user(user_name, password, credential_file):
    """
    This function checks if the user has entered the correct details
    and if so allow them into the booking system.
    :param user_name: username from the user
    :param password: password from the user
    :param credential_file: The json file which contains all of the mysql details.
    :return: returns true or false based on if the details are correct or not.
    """
    correct_details = False
    creds = utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    table = "user"
    sql = "SELECT * FROM " + table
    connect_sql.cursor.execute(sql)
    records = connect_sql.cursor.fetchall()
    user_names = []
    passwords = []
    # salt is temporary until its in the table.
    salt = uuid.uuid4().hex
    hash_password(password, salt)
    for record in records:
        user_names.append(record[0])
        passwords.append(record[1])
    for name in user_names:
        if name == user_name:
            index = user_names.index(name)
            if passwords[index] == password:
                correct_details = True
    return correct_details
