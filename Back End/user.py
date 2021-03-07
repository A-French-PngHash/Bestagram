import datetime
import os
import random
import re
import werkzeug
import config
import database.mysql_connection
from database import request_utils
from errors import *
import tag
from PIL import Image
import hashlib
import profile
import images
import files


def generate_token() -> str:
    """
    Generate a random x characters long token.
    :return: The token.
    """
    # This are the character used in the token.
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    token = ""
    for i in range(config.TOKEN_LENGTH):
        token += random.choice(letters)
    return token


def email_is_valid(email: str) -> bool:
    """
    Check if an email is valid or not.
    :param email: The email.
    :return:
    """
    email_valid_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    result = re.findall(email_valid_regex, string=email)
    return len(result) == 1


def username_is_valid(username: str) -> bool:
    regex = r"^[a-z0-9_.]{" + str(config.MIN_USERNAME_LENGTH) + "," + str(config.MAX_USERNAME_LENGTH) + "}$"
    # ^[a-z0-9_.]{5,30}$
    return len(re.findall(regex, username)) == 1


def name_is_valid(name: str) -> bool:
    regex = r"^[a-z0-9_.? ]{" + str(config.MIN_NAME_LENGTH) + "," + str(config.MAX_NAME_LENGTH) + "}$"
    return len(re.findall(regex, name)) == 1


def make_server_side_hash(old_hash: str, username: str) -> str:
    """
    Calculate the hash for a given password. This hashing process is described in the global readme.
    :param old_hash:
    :param username:
    :return: The new hash.
    """
    new_hash = hashlib.pbkdf2_hmac("sha256", password=old_hash.encode("utf-8"), salt=username.encode("utf-8"),
                                   iterations=10000, dklen=32).hex()
    return new_hash


class User:
    """
    User of Bestagram.
    """

    def __init__(self, username: str = None, hash: str = None, token: str = None, refresh_token: str = None):
        """
        Initialize the user object. This is the login, if a user need to be registered, the static function create must
        be called. There is two different way of login the user : using username and hash or using the token only.
        WARNING : refresh token should only be used to get the new token and never to do other actions.

        :param username: Username of the user.
        :param hash: Hash of the user.
        :param token: Token to connect with.

        :raise InvalidCredentials: When the username and hash don't both correspond to the data of a user.
        """
        if hash:
            hash = make_server_side_hash(old_hash=hash, username=username)

        if username:
            # This query fetch all the user data of this user in the table UserTable.
            user_query = f"""
            SELECT *
            FROM UserTable
            WHERE UserTable.username = "{username}" AND UserTable.hash = "{hash}";
            """
        elif refresh_token:
            user_query = f"""
            SELECT * 
            FROM UserTable
            WHERE UserTable.refresh_token = "{refresh_token}";
            """
        else:
            user_query = f"""
            SELECT * 
            FROM UserTable
            WHERE UserTable.token = "{token}";
            """

        self.cursor = database.mysql_connection.cnx.cursor(dictionary=True)
        self.cursor.execute(user_query)
        result = self.cursor.fetchall()

        if len(result) == 0:
            if token:
                # Token authentication
                raise InvalidCredentials(token=token)
            else:
                raise InvalidCredentials(username=username, hash=hash)

        result = result[0]
        self._token = result["token"]
        self._token_registration_date: datetime.datetime = result["token_registration_date"]
        self.id = result["id"]

        if token and self.token != token:
            """
            This may happen if the user was logged in with an expired token. The token was not yet regenerated so it was
            successful in retrieving the data. However by calling the calculated property token, it is regenerated 
            leading the if statement to enter as they are now different.
            """
            raise InvalidCredentials(token=token)

        self.username = result["username"]
        self.name = result["name"]

        self.hash = hash
        self._caption = result["caption"]
        self._profile = None

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
        self._token_registration_date = (
                    datetime.datetime.today() + datetime.timedelta(seconds=config.TOKEN_EXPIRATION)).replace(
            microsecond=0)
        update_token_registration_query = f"""
        UPDATE UserTable
        SET token_registration_date = "{self._token_registration_date}"
        WHERE id = "{self.id}";
        """
        self.cursor.execute(update_token_registration_query)
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
    def refresh_token(self):
        get_refresh_token_query = f"""SELECT refresh_token FROM UserTable WHERE UserTable.id = {self.id}"""
        self.cursor.execute(get_refresh_token_query)
        result = self.cursor.fetchall()
        return result[0]["refresh_token"]

    @property
    def token_expiration_date(self):
        return (self._token_registration_date + datetime.timedelta(seconds=config.TOKEN_EXPIRATION))

    @property
    def directory(self) -> str:
        """
        Path leading to the image directory where post's images from this user are stored.
        :return:
        """
        return f'Medias/image/{self.id}'

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

    @property
    def profile(self) -> profile.Profile:
        if self._profile:
            return self._profile
        self._profile = profile.Profile(self)
        return self._profile

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

    def follow(self, id: int):
        """
        Follow another user.
        :param id: Id of the user to follow.
        """
        # TODO: - This function currently doesn't check if the account is private or not.

        follow_query = f"""
        INSERT INTO Follow
        VALUES({self.id}, {id});
        """
        # This query check if this user is already following the other user.
        check_if_already_follow_query = f"""
        SELECT * FROM Follow
        WHERE user_id = {self.id} && user_id_followed = {id};
        """
        self.cursor.execute(check_if_already_follow_query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            # This user already follow the other user.
            raise UserAlreadyFollowed
        try:
            self.cursor.execute(follow_query)
        except Exception as e:
            raise UserNotExisting
        return True

    @staticmethod
    def create(username: str, name: str, hash: str, email: str):
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
        name = name.lower()
        print(hash)
        # TODO: update requirements for parameters in documentation.
        if not email_is_valid(email):
            raise InvalidEmail(email=email)

        if not username_is_valid(username):
            raise InvalidUsername(username=username)

        if not name_is_valid(name):
            raise InvalidName(name=name)

        if request_utils.value_in_database("UserTable", "username", username):
            # Username is taken.
            raise UsernameTaken(username=username)

        if request_utils.value_in_database("UserTable", "email", email):
            # Email is taken.
            raise EmailTaken(email=email)

        # Account can be created, server-side hashing can now take place following the protocol described in the global
        # readme.
        new_hash = make_server_side_hash(old_hash=hash, username=username)
        refresh_token = generate_token()

        add_user_query = f"""
        INSERT INTO UserTable (username, name, hash, email, refresh_token) VALUES
        ("{username}", "{name}", "{new_hash}", "{email}", "{refresh_token}");
        """
        cursor = database.mysql_connection.cnx.cursor()
        cursor.execute(add_user_query)
        cursor.close()
        return User(username, hash=hash)

    def search_for(self, search: str, offset: int, row_count: int) -> dict:
        """
        This function execute a search for user on the database using the search string. It is not a static method as
        the search result depends on the user searching.

        :param search: Search string.
        :param offset: Offset to begin at. Begins at 0.
        :param row_count: Number of results to have. Must be less
        :return: Returns a dictionary of dictionary containing the id of the user (+ its name and username) whose username match the
        search. First dctionary keys are the rank in the search (the lowest, the more matching), begins from the offset.
        """

        search_str = "%" + "%".join(search) + "%"
        """
        If the string is abc it transforms it to %a%b%c% which allow us to match suggestions for string like : 
        
         - ABraCadabra
         - ABC
         - hellow A B hellow C
         
        It allows for matches even if the charaters doesn't touch each other as long as they appear in the same order
        """
        if offset < 0:
            offset = 0
        if row_count > 100:
            row_count = 100
        search_str = self.cursor._connection.converter.escape(search_str)
        # This query select user matching the search query which the current user follow.
        followed_search_query = f"""
        SELECT name, username, id, (SELECT COUNT(*) FROM Follow WHERE user_id_followed = id) AS followers FROM UserTable 
        JOIN Follow ON Follow.user_id_followed = UserTable.id
        WHERE UserTable.name LIKE "{search_str}" AND Follow.user_id = {self.id}
        ORDER BY followers DESC, name ASC
        LIMIT {offset}, {row_count};
        """
        self.cursor.execute(followed_search_query)
        results = self.cursor.fetchall()
        if len(results) < row_count:
            # Not enough results in the first query targeting followed user. Executing search on not followed user.
            not_followed_search_query = f"""
            SELECT name, username, id, (SELECT COUNT(*) FROM Follow WHERE user_id_followed = id) AS followers FROM UserTable
            WHERE UserTable.name LIKE "{search_str}" AND id NOT IN (SELECT user_id_followed FROM Follow WHERE user_id = {self.id}) AND id != {self.id}
            ORDER BY followers DESC, name ASC
            LIMIT {offset}, {row_count - len(results)};
            """
            self.cursor.execute(not_followed_search_query)
            results += self.cursor.fetchall()
        usernames = [i["id"] for i in results]
        dictionary = {index + int(offset): {"id": element["id"], "username": element["username"], "name": element["name"]} for (index, element)
                      in enumerate(results)}
        return dictionary
