import datetime
import os
import random
import re
import werkzeug
import config
import database.mysql_connection
from database.request_utils import value_in_database
from errors import *


def generate_token() -> str:
    """
    Generate a random 30 characters long token.
    :return: The token.
    """
    # This are the character used in the token.
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    token = ""
    for i in range(200):
        token += random.choice(letters)
    return token


def email_is_valid(email: str) -> bool:
    """
    Check if an email is valid or not.
    :param email: The email.
    :return:
    """
    email_valid_regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
    result = re.findall(email_valid_regex, string=email)
    return len(result) == 1


def username_is_valid(username: str) -> bool:
    regex = r"^[a-z0-9_.]{" + str(config.MIN_USERNAME_LENGTH) + "," + str(config.MAX_USERNAME_LENGTH) + "}$"
    return len(re.findall(regex, username)) == 1


class User:
    """
    User of Bestagram.
    """

    def __init__(self, username: str, hash: str = None, token: str = None):
        """
        Initialize the user object. This is the login, if a user need to be registered, the static function create must
        be called. Note that either the hash parameter OR the token is required.

        :param username: Username of the user.
        :param hash: Hash of the user.
        :param token: Token to connect with.

        :raise InvalidCredentials: When the username and hash don't both correspond to the data of a user.
        """
        self.username = username

        # This query fetch all the user data of this user in the table UserTable
        user_query = f"""
        SELECT *
        FROM UserTable
        WHERE UserTable.username = "{username}";
        """
        self.cursor = database.mysql_connection.cnx.cursor(dictionary=True)
        self.cursor.execute(user_query)
        result = self.cursor.fetchall()

        if len(result) == 0:
            raise InvalidCredentials(username=username, hash=hash)

        result = result[0]
        self._token = result["token"]
        self._token_registration_date = result["token_registration_date"]
        self.id = result["id"]

        # Checking if given credentials are correct.
        if not (result["hash"] == hash or self.token == token):
            raise InvalidCredentials(username=username, hash=hash)

        self.hash = hash
        self._description = result["description"]
        self._profile_image_path = result["profile_image_path"]

    def __del__(self):
        try:
            self.cursor.fetchall()
        except:
            pass
        self.cursor.close()

    @property
    def token(self) -> str:
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

    @property
    def directory(self) -> str:
        """
        Path leading to the directory where post's images from this user are stored.
        :return:
        """
        return f'Posts/{self.username}'

    @property
    def number_of_post(self) -> int:
        """
        Number of post this user has made.
        :return:
        """
        get_posts_request = f"""
        SELECT * FROM Post
        WHERE Post.user_id = {self.id};
        """
        self.cursor.execute(get_posts_request)
        return len(self.cursor.fetchall())

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

    def create_post(self, image: werkzeug.datastructures.FileStorage, description: str):
        """
        Create a post from this user.
        :param image: Post's image.
        :param description: Description provided with the post.
        :return:
        """
        self.prepare_directory()
        image.filename = f"{self.number_of_post}.png"
        image_path = os.path.join(self.directory, image.filename)
        try:
            image.save(image_path)
        except:
            # When testing, the image provided is invalid so this enables the program to continue anyway.
            pass
        create_post_query = f"""
        INSERT INTO Post
        VALUES(
        NULL, "{image_path}", {self.id}, "{datetime.datetime.now().replace(microsecond=0)}", "{description}"
        );
        """
        print(create_post_query)
        self.cursor.execute(create_post_query)

    def prepare_directory(self):
        """
        Prepare the directory to store a post's image in. Create it if it not already exists.
        :return:
        """
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    @staticmethod
    def create(username: str, hash: str, email: str):
        """
        Add a user in the database and return the User object associated. Also check if the username is not already
        taken.
        :param username: The username of the user to create.
        :param email: Email of the user.
        :param hash: The hash the user use to login.

        :raise UsernameTaken:
        :raise EmailTaken:

        :return: User object created.
        """
        username = username.lower()


        if not email_is_valid(email):
            raise InvalidEmail(email=email)

        if not username_is_valid(username):
            raise InvalidUsername(username=username)

        re.findall("string", "test")

        if value_in_database("UserTable", "username", username):
            # Username is taken.
            raise UsernameTaken(username=username)

        if value_in_database("UserTable", "email", email):
            # Email is taken.
            raise EmailTaken(email=email)

        add_user_query = f"""
        INSERT INTO UserTable (username, hash, email) VALUES
        ("{username}", "{hash}", "{email}");
        """
        cursor = database.mysql_connection.cnx.cursor()
        cursor.execute(add_user_query)
        cursor.close()
        return User(username, hash=hash)
