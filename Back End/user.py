import datetime
import os
import random
import re
import werkzeug
import config
import database.mysql_connection
from database.request_utils import value_in_database
from errors import *
from tag import *
from PIL import Image


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


class User:
    """
    User of Bestagram.
    """

    def __init__(self, username: str = None, hash: str = None, token: str = None):
        """
        Initialize the user object. This is the login, if a user need to be registered, the static function create must
        be called. There is two different way of login the user : using username and hash or using the token only.

        :param username: Username of the user.
        :param hash: Hash of the user.
        :param token: Token to connect with.

        :raise InvalidCredentials: When the username and hash don't both correspond to the data of a user.
        """

        if username:
            # This query fetch all the user data of this user in the table UserTable.
            user_query = f"""
            SELECT *
            FROM UserTable
            WHERE UserTable.username = "{username}" AND UserTable.hash = "{hash}";
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
        self.username = result["username"]
        self.name = result["name"]
        self._token = result["token"]
        self._token_registration_date = result["token_registration_date"]
        self.id = result["id"]

        self.hash = hash
        self._caption = result["caption"]
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
        new_token = self.username + generate_token()
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
    def temp_directory(self) -> str:
        """
        Path leading to the temp directory. Image are first stored there, resized, compressed and then stored in
        the correct file.
        :return:
        """
        # $ can't be in a username so we know that this is a unique directory and won't override any existing directory.
        return f'Posts/$temp'

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

    def resize_image(self, image: Image, length: int) -> Image:
        """
        Resize an image to a square. Can make an image bigger to make it fit or smaller if it doesn't fit. It also crops
        part of the image.

        :param self:
        :param image: Image to resize.
        :param length: Width and height of the output image.
        :return: Return the resized image.
        """

        """
        Resizing strategy : 
         1) We resize the smallest side to the desired dimension (e.g. 1080)
         2) We crop the other side so as to make it fit with the same length as the smallest side (e.g. 1080)
        """
        if image.size[0] < image.size[1]:
            # The image is in portrait mode. Height is bigger than width.

            # This makes the width fit the LENGTH in pixels while conserving the ration.
            resized_image = image.resize((length, int(image.size[1] * (length / image.size[0]))))

            # Amount of pixel to lose in total on the height of the image.
            required_loss = (resized_image.size[1] - length)

            # Crop the height of the image so as to keep the center part.
            resized_image = resized_image.crop(
                box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))

            # We now have a 1080x1080 pixels image.
            return resized_image
        else:
            # This image is in landscape mode or already squared. The width is bigger than the heihgt.

            # This makes the height fit the LENGTH in pixels while conserving the ration.
            resized_image = image.resize((int(image.size[0] * (length / image.size[1])), length))

            # Amount of pixel to lose in total on the width of the image.
            required_loss = resized_image.size[0] - length

            # Crop the width of the image so as to keep 1080 pixels of the center part.
            resized_image = resized_image.crop(
                box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))

            # We now have a 1080x1080 pixels image.
            return resized_image

    def create_post(self, image: werkzeug.datastructures.FileStorage, caption: str, tags: [Tag]):
        """
        Create a post from this user.
        :param image: Post's image.
        :param caption: Caption provided with the post.
        :param tags: List of this post's tags.
        :return:
        """
        self.prepare_directory(self.directory)
        self.prepare_directory(self.temp_directory)

        image.filename = f"{self.number_of_post}.png"
        temp_image_path = os.path.join(self.temp_directory, image.filename)

        # Dir where the image will be stored after its resizing
        final_image_path = os.path.join(self.directory, image.filename)

        # Saving the image in the temp directory.
        image.save(temp_image_path)
        image.close()

        # NOTE: The image is stored in a temporary directory to be able to open it in the PIL.Image format which can be
        # used for resizing.

        resized_image = Image.open(temp_image_path)
        resized_image = self.resize_image(resized_image, config.DEFAULT_IMAGE_DIMENSION)

        # Saving to final directory.
        resized_image.save(final_image_path)
        # Removing the temporary image created.
        os.remove(temp_image_path)

        create_post_query = f"""
        START TRANSACTION;
            INSERT INTO Post
            VALUES(
            NULL, "{final_image_path}", {self.id}, "{datetime.datetime.now().replace(microsecond=0)}", "{caption}"
            );
            
            SELECT LAST_INSERT_ID();
        COMMIT;
        """
        iterable = self.cursor.execute(create_post_query, multi=True)
        # 4 request are made a the same time. The third is the select one.
        index = 0
        result: list = []

        for i in iterable:
            if index == 2:
                result = i.fetchall()
            index += 1

        post_id = result[0]["LAST_INSERT_ID()"]
        for i in tags:
            i.save(post_id)

    def prepare_directory(self, dir: str):
        """
        Prepare the directory to store a post's image in. Create it if it not already exists.
        :return:
        """
        if not os.path.exists(dir):
            os.makedirs(dir)

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

        if not email_is_valid(email):
            raise InvalidEmail(email=email)

        if not username_is_valid(username):
            raise InvalidUsername(username=username)

        if not name_is_valid(name):
            raise InvalidName(name=name)

        if value_in_database("UserTable", "username", username):
            # Username is taken.
            raise UsernameTaken(username=username)

        if value_in_database("UserTable", "email", email):
            # Email is taken.
            raise EmailTaken(email=email)

        add_user_query = f"""
        INSERT INTO UserTable (username, name, hash, email) VALUES
        ("{username}", "{name}", "{hash}", "{email}");
        """
        cursor = database.mysql_connection.cnx.cursor()
        cursor.execute(add_user_query)
        cursor.close()
        return User(username, hash=hash)

    def search_for(self, search: str, offset: int, row_count: int) -> list:
        """
        This function execute a search for user on the database using the search string. It is not a static method as
        the search result depends on the user searching.

        :param search: Search string.
        :param offset: Offset to begin at. Begins at 0.
        :param row_count: Number of results to have. Must be less
        :return: Returns the list of username matching the search.
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
            # Not enough results in the first query targetting followed user. Executing search on not followed user.
            not_followed_search_query = f"""
            SELECT name, username, id, (SELECT COUNT(*) FROM Follow WHERE user_id_followed = id) AS followers FROM UserTable
            WHERE UserTable.name LIKE "{search_str}" AND id NOT IN (SELECT user_id_followed FROM Follow WHERE user_id = {self.id}) AND id != {self.id}
            ORDER BY followers DESC, name ASC
            LIMIT {offset}, {row_count - len(results)};
            """
            self.cursor.execute(not_followed_search_query)
            results += self.cursor.fetchall()
        usernames = [i["username"] for i in results]
        return usernames
