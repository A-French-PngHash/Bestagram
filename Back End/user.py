from errors import *
import datetime
import config
import random
import mysql.connector


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

    def __init__(self, username: str, hash: str, cursor: mysql.connector.connection_cext.CMySQLCursor):
        """
        Initialize the user object. This is the login, if a user need to be registered, the static function create must
        be called.

        :param username: Username of the user.
        :param hash: Hash of the user.
        :param cursor: Cursor connecting to the database.

        :raise InvalidCredentials: When the username and hash don't both correspond to the data of a user.
        """
        self.username = username

        # This query fetch all the user data of this user in the table UserTable
        user_query = f"""
        SELECT *
        FROM UserTable
        WHERE UserTable.username = "{username}";
        """
        cursor.execute(user_query)
        result = cursor.fetchall()
        print(user_query)
        # Checking if given credentials are correct.
        if len(result) == 0 or result[0]["hash"] != hash:
            raise InvalidCredentials(username=username, hash=hash)

        result = result[0]

        self.cursor = cursor
        self.hash = hash
        self.id = result["id"]
        self._token = result["token"]
        self._token_registration_date = result["token_registration_date"]
        self._description = result["description"]
        self._profile_image_path = result["profile_image_path"]

    @property
    def token(self):
        if self._token_registration_date:
            # Checking if token is expired.
            if (datetime.datetime.today() - self._token_registration_date).total_seconds() < config.TOKEN_EXPIRATION:
                # Token is not expired, fetching it from the database.
                token_query = f"""
                SELECT token
                FROM UserTable
                WHERE UserTable.id = {self.id};
                """
                self.cursor.execute(token_query)
                result = self.cursor.fetchall()[0]
                return result["token"]

        # Token is expired or has never been created.
        # generating new token.
        new_token = generate_token()
        self.token = new_token
        return new_token

    @token.setter
    def token(self, value: str):
        # Update the token value in the database AND the registration date
        self._set_value(values={
            "token": value,
            "token_registration_date": datetime.datetime.today().replace(microsecond=0)
        })

    def _set_value(self, values: dict):
        """
        Set value(s) for this user in the UserTable table.
        :param values: This is a dictionary. Each key is a field and the value is the new value to put in the database.
        :return:
        """
        query = f"""
        UPDATE UserTable
        SET 
        """

        for (key, value) in values.items():
            # Adding each field specified.
            query += f"""{key} = "{value}","""
        # Last element is an unwanted comma.
        query = query[:-1]
        query += f"""
        WHERE UserTable.id = {self.id};
        """
        self.cursor.execute(query)

    @staticmethod
    def create(username: str, hash: str, email: str, cursor: mysql.connector.connection_cext.CMySQLCursor):
        """
        Add a user in the database and return the User object associated. Also check if the username is not already
        taken.
        :param cursor: Cursor connecting to the database.
        :param username: The username of the user to create.
        :param hash: The hash the user use to login.
        :raise UsernameTaken:
        :return: User object created.
        """

        # Checking if the username is already taken or not.
        check_if_username_taken_query = f"""
        SELECT * FROM UserTable
        WHERE UserTable.username = "{username}";
        """
        cursor.execute(check_if_username_taken_query)
        if len(cursor.fetchall()) != 0:
            # Username is taken.
            raise UsernameTaken(username=username)

        add_user_query = f"""
        INSERT INTO UserTable (username, hash, email) VALUES
        ("{username}", "{hash}", "{email}");
        """
        cursor.execute(add_user_query)
        return User(username, hash, cursor)
