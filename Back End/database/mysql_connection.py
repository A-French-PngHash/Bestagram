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
cnx.cursor()


def make_cursor() -> mysql.connector.connection_cext.CMySQLCursor:
    """
    Returns a mysql cursor. Put the desire parameter automatically so no need to add them in the programm,
    just call the method.
    :return:
    """
    return cnx.cursor(dictionary=True)
