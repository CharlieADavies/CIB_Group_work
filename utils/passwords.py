import hashlib
import utils.db_init.py


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def check_user(user_name, password, credential_file):
    correct_details = False
    utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect()
    table = "login_table"
    sql = "SELECT * FROM " + table
    connect_sql.cursor.execute(sql)
    records = connect_sql.cursor.fetchall()
    user_names = []
    passwords = []
    for record in records:
        user_names.append(record[1])
        passwords.append(record[2])
    for name in user_names:
        if name == user_name:
            index = user_names.index(name)
            if passwords[index] == password:
                correct_details = True
    return correct_details


if __name__ == '__main__':
    check = check_user("Finn", "password")
    print(check)
