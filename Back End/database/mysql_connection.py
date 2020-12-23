import config
import mysql.connector

"""
Establish the connection to the database.
"""
cnx = mysql.connector.connect(
    user=config.databaseUserName,
    password=config.password,
    host=config.host,
    database=config.databaseName,
    use_pure=True)
cnx.autocommit = True
cursor = cnx.cursor(dictionary=True)

def make_cursor():
    return cnx.cursor(dictionary=True)

