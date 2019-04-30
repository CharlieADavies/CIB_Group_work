import utils.db_init


class AccountDetails:
    def __init__(self, local_username, credential_file):
        self._username = local_username
        self._credential_file = credential_file
        self.user_details = self.get_user_details()

    def get_user_details(self):
        creds = utils.db_init.load_credentials(self._credential_file)
        connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        table = "users"
        sql = "SELECT * FROM " + table + " WHERE username = '" + self._username + "';"
        cursor = connect_sql.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record


if __name__ == '__main__':
    username = "richard.chop@gmail.com"
    # enter secretes.json in empty quotations
    details = AccountDetails(username, "H:\\Applications of programming\\CIB\\secrets.json")
    for detail in details
