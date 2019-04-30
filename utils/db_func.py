"""
database functionality common to both flask and tkinter
"""

"""
import these
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
"""

def vehicles_insert_query(userID, electricVehicle, registrationVehicle, makeVehicle, blueBadge):
    try:
        connection = mysql.connector.connect(host='you-fail.net',
                             database='youfailn_cib',
                             user='youfailn_cb',
                             password='H4p9Hcf3scCytzr')
        cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO `vehicles`
                          (`username`, `electric_vehicle`, `vehicle_registration`, `vehicle_make`,`is_blue_badge`) VALUES (%s,%s,%s,%s,%s)"""
        insert_tuple = (userID, electricVehicle, registrationVehicle, makeVehicle, blueBadge)
        result  = cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()
        print ("Record inserted successfully into vehicles table")
    except mysql.connector.Error as error :
        connection.rollback()
        print("Failed to insert into vehicles table {}".format(error))

vehicles_insert_query("andrescordovajim@hotmail.com", 0, "CE55 BAD", "Peugeot",0)