""" Contain configuration variables. """
databaseUserName = "root"
password = "password"
host = "localhost"
databaseName = "Bestagram"

TOKEN_EXPIRATION = 3600
"""
The number of seconds after which a token is not valid anymore and need to be renewed.
"""
TOKEN_LENGTH = 30
"""
The number of characters used in the token. If you change this value be sure to change the VARCHAR token field in the 
database to the new value you put for the token.
"""
MAX_USERNAME_LENGTH = 30
MIN_USERNAME_LENGTH = 5
