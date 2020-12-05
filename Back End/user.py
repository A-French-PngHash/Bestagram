from database.database_request import *
from errors import *
from datetime import datetime
import config
import random


def generate_token() -> str:
    """
    Generate a random 30 characters long token.
    :return: The token.
    """
    # This are the character used in the token.
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    token = ""
    for i in range(30):
        token += random.choice(letters)
    return token


class User:
    """
    Is a user of Bestagram.
    """

    def __init__(self, username, hash):
        """
        Initialize the user object. Login verification is here.
        :param username:
        :param hash:
        """
        self.username = username

        # This query fetch all the user data of this user in the table UserTable
        user_query = f"""
        SELECT *
        FROM UserTable
        WHERE UserTable.username = "{username}";
        """
        result = request(user_query)[0]
        # Checking if given credentials are correct.
        if result["hash"] != hash:
            raise InvalidCredentials()

        self.id = result["id"]
        self._token = result["token"]
        self._token_registration_date = result["token_registration_date"]
        self._description = result["description"]
        self._profile_image_path = result["profile_image_path"]

    @property
    def token(self):
        if self._token_registration_date:
            # Checking if token is expired.
            if (datetime.today() - self._token_registration_date).total_seconds() > config.TOKEN_EXPIRATION:
                # Token is expired.
                # Updating the token.
                newToken = generate_token()
                self.token = newToken
                return newToken
            else:
                # Token is not expired, fetching it from the database.
                token_query = f"""
                SELECT Token
                FROM UserTable
                WHERE UserTable.id = {self.id};
                """
                result = request(token_query)[0]
                return result["token"]
        return

    @token.setter
    def token(self, value: str):
        self._set_value("token", value)

    def _set_value(self, field_name: str, value):
        """
        Set a value for self in the UserTable table.
        :param field_name: The field to change the values.
        :param value: The new value to put in the field.
        :return:
        """
        query = f"""
        UPDATE UserTable
        SET {field_name} = "{value}"
        WHERE UserTable.id = "{self.id}"
        """
        request(query, fetch=False)
