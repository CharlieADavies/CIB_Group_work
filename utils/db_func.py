"""
database functionality common to both flask and tkinter
"""
import mysql
import utils.db_init


connection = mysql.connector.connect(host='you-fail.net',
                                     database='youfailn_cib',
                                     user='youfailn_cib',
                                     password='H4p9Hcf3scCytzr')


def vehicles_insert_query(userID, electricVehicle, registrationVehicle, makeVehicle):
    try:
        creds = utils.db_init.load_credentials("./secrets.json")
        connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO `vehicles`
                          (`username`, `electric_vehicle`, `vehicle_registration`, `vehicle_make`) VALUES (%s,%s,%s,%s,%s)"""
        insert_tuple = (userID, electricVehicle, registrationVehicle, makeVehicle)
        result  = cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()
        print ("Record inserted successfully into vehicles table")
    except mysql.connector.Error as error :
        #connection.rollback()
        print("Failed to insert into vehicles table {}".format(error))

vehicles_insert_query("andrescordovajim@hotmail.com", 0, "CE55 BAD", "Peugeot")