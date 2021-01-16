import config
import mysql.connector

"""
This variable is the connection to the database. It is not defined here as its content depends on the context.
If what is running is the production version (main.py) then it is defined in main.py.
If what is running is tests then it is defined in tests/tests.py pointing to the test database.
This enable testing without altering the production database.
"""
cnx : mysql.connector.MySQLConnection = None
