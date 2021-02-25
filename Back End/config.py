""" Contain configuration variables. """

TOKEN_EXPIRATION = 3600
"""
The number of seconds after which a token is not valid anymore and need to be renewed.
"""
TOKEN_LENGTH = 50
"""
The number of characters used in the token. If you change this value be sure to change the VARCHAR token field in the 
database to the new value you put for the token.
"""

MAX_USERNAME_LENGTH = 30
"""
Max length for usernames allowed. If you change this value make sure to change the VARCHAR value of the token field in
the database as the username is added at the beginning of the token."""
MIN_USERNAME_LENGTH = 5

MAX_NAME_LENGTH = 50
MIN_NAME_LENGTH = 1


IMAGE_DIMENSION = 1080
"""
Dimension to resize the images to when an upload is made.
"""
PROFILE_PICTURE_DIMENSION = 150
