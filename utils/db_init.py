"""
gets the object with connection details for the database - requires serets.json
"""
import json

import mysql.connector


def load_credentials(f="../secrets.json"):

    with open(f, "r+") as f:
        creds = json.load(f)
    return creds


def connect(user, database, password, host):
    return mysql.connector.connect(user=user, database=database, password=password, host=host)

