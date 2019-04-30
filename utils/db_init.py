"""
gets the object with connection details for the database - requires serets.json
"""
import json

import mysql.connector


def load_credentials(f):
    with open(f, "r+") as f:
        creds = json.load(f)
    return creds


def connect(user, database, password, host):
    return mysql.connector.connect(user=user, database=database, password=password, host=host)


def load_db(file_path="../secrets.json"):
    """
    :return: mysql.connector.connect() whatever that returns
    :param file_path: the file path of the database secrets file
    """
    creds = load_credentials(file_path)
    return connect(user=creds['user'],
                   database=creds['database'],
                   password=creds['password'],
                   host=creds['host']).cursor()



