import unittest
import mysql.connector
import user
import os
import config
import database.request_utils
import shutil
import database.mysql_connection
import errors
import main
from PIL import Image
import json
import random
import datetime
from errors import *


def create_db():
    source_file = f"\"{os.getcwd()}/test_database.sql\""
    command = """mysql -u %s -p"%s" --host %s --port %s %s < %s""" % (
        config.databaseUserName, config.password, config.host, 3306, config.databaseName, source_file)
    os.system(command)


class Tests(unittest.TestCase):
    """
    Test class executing requests to the api endpoints.
    """
    @property
    def image_square(self):
        with open('test_image.png') as file:
            return 'test_image.png', file, 'image/png'

    @property
    def image_portrait(self):
        with open('1280-1920.png') as file:
            return '1280-1920.png', file, 'image/png'

    @property
    def image_landscape_big(self):
        with open("3840-2160.png") as file:
            return "3840-2160.png", file, "image/png"

    @property
    def image_landscape_small(self):
        with open("474-266.png") as file:
            return "474-266.png", file, "image/png"

    default_hash = "hash"
    default_username = "test_username"
    default_name = "test_name"
    default_email = "test.test@bestagram.com"

    def tags(self, *args):
        """
        Return a list of tag.
        :param args: Ids of the tags.
        :return:
        """
        tags = {}
        for (i, e) in enumerate(args):
            tags[str(i)] = {"pos_x": 0.5, "pos_y": 0.5, "id": e}
        return tags

    def get_token(self, default: bool, token : str = None) -> str:
        """
        Many tests function have a signature with default present which allows for the use of the default user.
        This simplify testing but it also means additional db query in each function. This function does that.
        :param default:
        :param token:
        :return: The token.
        """

        authorization = token
        if default:
            if not self.user_in_db(self.default_username)[0]:
                self.add_default_user()
            authorization = self.login(self.default_username, self.default_hash)[1]["token"]
        return authorization

    def user_in_db(self, username: str) -> (bool, dict):
        """
        Fetch a user's data from the db if exists.
        :param username: Username of the user.
        :return: Operation successful, if yes the dict contain the data.
        """
        query = f"""
        SELECT * FROM UserTable
        WHERE username = "{username}";
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result) == 0:
            return False, None
        return True, result[0]

    def random_string(self, length: int) -> str:
        """
        Generate a random string of length length.
        :param length: Length of the string.
        :return:
        """
        letters = "abcdefghijklmnopqrstuvwxyz1234567890"
        output = ""
        for _ in range(length):
            output += random.choice(letters)
        return output

    def add_user(self, username: str = None, email: str = None, name: str = None, hash: str = None, token: str = None, refresh_token: str = None) -> int:
        """
        Add a user in the test database.
        :param username: Username of the user to add. Optional.
        :param email: Email of the user. Optional.
        :param name: Name of the user. Optional.
        :param hash: Hash of the user. Optional.

        If the username, email, name or hash is not provided, they will be generated randomly.

        :return: The id of the newly created user.
        """
        if not username:
            username = self.random_string(config.MAX_USERNAME_LENGTH)
        if not email:
            email = self.random_string(8) + "." + self.random_string(8) + "@" + self.random_string(
                5) + "." + self.random_string(4)
        if not name:
            name = self.random_string(config.MAX_NAME_LENGTH)
        if not hash:
            hash = self.random_string(50)
        else:
            # When the hash get to the server there is suppose to be some hashing on it. Because we don't go through
            # the endpoint in this method we need to simulate this hashing.
            hash = user.make_server_side_hash(old_hash=hash, username=username)

        if not refresh_token:
            refresh_token = user.generate_token()
        registration_date = None
        if token:
            registration_date = datetime.datetime.today().replace(microsecond=0)

        add_user_query = f"""
        INSERT INTO UserTable (username, name, email, hash, refresh_token {", token" if token else ""} {",token_registration_date" if registration_date else ""})
        VALUES ("{username}", "{name}", "{email}", "{hash}", "{refresh_token}"
        """
        if token:
            add_user_query += f""", "{token}" """
        if registration_date:
            add_user_query += f""", "{registration_date}" """
        add_user_query += ");"
        self.cursor.execute(add_user_query)
        id_u = self.user_in_db(username=username)[1]["id"]
        return id_u

    def login(self, username : str, hash: str):
        parameters = {"hash": hash}
        code, content = self.ex_request("POST", route=f"user/login/{username}", params=parameters)
        return code, content

    def register(self, username: str = None, name : str = None, hash: str = None, email: str = None):
        """
        Register user using api.
        All parameters are optionnal. If they are not provided the value is the default value.
        """
        if not username:
            username = self.default_username
        if not name:
            name = self.default_name
        if not hash:
            hash = self.default_hash
        if not email:
            email = self.default_email
        code, content = self.ex_request("PUT", route=f"user/login/{username}", params={
            "username": username,
            "name": name,
            "hash": hash,
            "email": email
        })
        return code, content

    def add_default_user(self, token: str = None, refresh_token: str = None):
        self.add_user(username=self.default_username,
                      name=self.default_name,
                      hash=self.default_hash,
                      email=self.default_email,
                      token=token,
                      refresh_token=refresh_token)

    def ex_request(self, method: str, route: str, params: dict = None, headers: dict = None, file=None,
                   json: dict = None) -> (int, dict):
        """
        Execute a request to the api using the provided parameters.

        :param method: Method to use to contact the api.
        :param route: Route leading to the resources
        :param params: Query parameters.
        :param headers: Request headers.
        :param file: File to send with the request in body.
        :param json: Body json.

        :return: Returns status code and json content of the response.
        """
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if json is None:
            json = {}
        else:
            json = (None, json, "application/json")

        data = dict(
            image=file,
            json=json
        )
        response = self.client.open(
            route,
            query_string=params,
            method=method,
            headers=headers,
            data=data
        )
        code = response.status_code
        content = response.get_json()

        return code, content

    def post(self, default: bool, file: tuple, caption=None, tag: dict = None,
             token: str = None) -> tuple:
        """
        Post a picture.

        :param default: Use default account or not. If the default account doesn't already exist, will create it and
        then use it to post the picture.
        :param file: Image file to post.
        :param caption: Caption to the image.
        :param tag: Tag to register with the picture.
        :param token: If the default option is set to false then this is the token that goes with the username of the
        account to use for posting.
        :return:
        """
        authorization = self.get_token(default, token)
        code, content = self.ex_request(
            method="PUT",
            route="/user/post",
            params={"caption": caption, "tag": json.dumps(tag)},
            headers={"Authorization": authorization},
            file=file
        )
        return code, content

    def search(self, default: bool, search: str, offset: int, row_count: int, token: str = None) -> tuple:
        authorization = self.get_token(default, token)

        code, content = self.ex_request(
            method="GET",
            route="/user/search",
            params={"rowCount": row_count, "search": search, "offset": offset},
            headers={"Authorization": authorization}
        )
        return code, content

    def follow_db(self, default: bool, user_id_followed: int = None, username_followed : str = None, user_id: int = None, username: str = None):
        """
        Add follow relation from one user to another DIRECTLY into the database.
        :param default: Use the default account as the following acccount.
        :param user_id_followed: Id of the followed account.
        :param username_followed: Username of the followed account. Necessary if the user_id_followed is not provided.
        :param user_id: If default is set to false then this is the id of the user following.
        :param username: If default is set to false and user_id is not provided then that is the username of the user following.
        :return:
        """
        user_id_followed = user_id_followed
        user_id = user_id
        if default:
            if not self.user_in_db(self.default_username)[0]:
                self.add_default_user()
            query = f"""SELECT id FROM UserTable WHERE username = "{self.default_username}";"""
            self.cursor.execute(query)
            user_id = self.cursor.fetchall()[0]["id"]
        if username_followed:
            query = f"""SELECT id FROM UserTable WHERE username = "{username_followed}";"""
            self.cursor.execute(query)
            user_id_followed = self.cursor.fetchall()[0]["id"]
        if username:
            query = f"""SELECT id FROM UserTable WHERE username = "{username}" """
            self.cursor.execute(query)
            user_id = self.cursor.fetchall()[0]["id"]

        add_follow_query = f"""INSERT INTO Follow VALUES ({user_id}, {user_id_followed});"""
        self.cursor.execute(add_follow_query)

    def follow_api(self, default: bool, id_followed : int, token: str = None):
        authorization = self.get_token(default, token)

        code, content = self.ex_request("POST", route=f"/user/{id_followed}/follow", headers={"Authorization" : authorization})
        return code, content

    def refresh_token(self, refresh_token: str) -> (int, dict):
        """
        Refresh the token by using the dedicated endpoint.
        """
        return self.ex_request("POST", route=f"/user/login/refresh/{refresh_token}")

    def profile(self, default: bool, caption : str = None, public : bool = None, image : tuple = None, username : str = None, name : str = None, token: str = None):
        authorization = self.get_token(default, token)
        code, content = self.ex_request("PATCH", route=f"/user/profile", headers={"Authorization" : authorization}, params={"caption" : caption, "public" : public, "username" : username, "name" : name}, file=image)
        return code, content

    @classmethod
    def setUpClass(cls):
        create_db()

    def setUp(self) -> None:
        main.app.testing = True
        self.client = main.app.test_client()

        database.mysql_connection.cnx = mysql.connector.connect(
            user=config.databaseUserName,
            password=config.password,
            host=config.host,
            database="BestagramTest",
            use_pure=True)
        database.mysql_connection.cnx.autocommit = True
        self.cursor = database.mysql_connection.cnx.cursor(dictionary=True)


        try:
            # Erase profile_picture_directory named Posts if exists.
            shutil.rmtree("Posts")
        except:
            pass

    """
    --------------------------
    Login tests
    --------------------------
    """

    def test_GivenNoUserInDatabaseWhenLoginWithAnyDataThenReturnInvalidCredentials(self):
        # Given no user in database.

        # When login with any data
        code, content = self.login(username="test", hash="hash")

        # Then return invalid credentials.
        self.assertEqual(400, code)
        self.assertEqual(False, content["success"])
        self.assertEqual(errors.InvalidCredentials.description, content["message"])

    def test_GivenUserInDatabaseWhenLoginWithIncorrectPasswordThenReturnInvalidCredentials(self):
        # Given user in database.
        self.add_default_user()
        incorrect_hash = "incorrect"

        # When login with incorrect password.
        code, content = self.login(username=self.default_username, hash=incorrect_hash)

        # Then raise invalid credentials.
        self.assertEqual(400, code, content)
        self.assertEqual(False, content["success"])
        self.assertEqual(content["message"], InvalidCredentials.description)

    def test_GivenUserInDatabaseWhenLoginWithCorrectDataThenSuccessfulLogin(self):
        # Given user in database.
        self.add_default_user()

        # When login with correct data.
        code, content = self.login(username=self.default_username, hash=self.default_hash)

        # Then successful login.
        self.assertEqual(True, content["success"])
        self.assertEqual(code, 200)

    """
    --------------------------
    Token expired tests
    --------------------------
    """

    def test_GivenTokenExpiredWhenAuthenticatingUserThenRaiseInvalidCredentials(self):
        """
        Exceptionally for this test we use the init of a class in the main program. This is because no endpoint checks
        if a token is valid but rather all endpoints with token should have the verification built in. This verification
        is present in the User class, that's why we test it directly.
        :return:
        """
        expired_registration_date = (datetime.datetime.today() - datetime.timedelta(seconds=config.TOKEN_EXPIRATION + 1)).replace(microsecond=0)
        token = "token"
        self.add_default_user(token=token)

        add_expire_token_query = f"""
        UPDATE UserTable
        SET token_registration_date = "{expired_registration_date}"
        WHERE UserTable.username = "{self.default_username}";
        """
        self.cursor.execute(add_expire_token_query)

        raised_invalid_credentials = False
        try:
            user.User(token=token)
        except InvalidCredentials:
            raised_invalid_credentials = True

        self.assertTrue(raised_invalid_credentials)

    def test_GivenTokenExpiredWhenSearchingThenRaiseInvalidCredentials(self):
        """
        Even though the previous test already check if the token expiration check is working, this directly checks on an
        endpoint. You can see this test as a double check.
        :return:
        """
        expired_registration_date = (
                    datetime.datetime.today() - datetime.timedelta(seconds=config.TOKEN_EXPIRATION + 1)).replace(
            microsecond=0)
        token = "token"
        self.add_default_user(token=token)
        add_expire_token_query = f"""
                UPDATE UserTable
                SET token_registration_date = "{expired_registration_date}"
                WHERE UserTable.username = "{self.default_username}";
                """
        self.cursor.execute(add_expire_token_query)

        code, content = self.search(default=False, search="", offset=0, row_count=5, token=token)
        expected_response = InvalidCredentials.get_response()
        self.assertEqual(code, expected_response[1])
        self.assertEqual(content, expected_response[0])

    """
    --------------------------
    Refresh Token Tests
    --------------------------
    """
    def test_GivenInvalidRefreshTokenWhenGettingTokenThenRaiseInvalidCredentials(self):
        code, content = self.refresh_token("invalidtoken")

        expected_response = InvalidCredentials.get_response()
        self.assertEqual(content, expected_response[0])
        self.assertEqual(code, expected_response[1])

    def test_GivenValidRefreshTokenWhenGettingTokenThenReturnCorrectToken(self):
        token = "mytoken"
        refresh_token = "myrefreshtoken"
        self.add_default_user(token=token, refresh_token=refresh_token)
        code, content = self.refresh_token(refresh_token)

        self.assertEqual(200, code)
        self.assertTrue(content["success"])
        self.assertEqual(token, content["token"])

    """
    --------------------------
    Sign up tests
    --------------------------
    """

    def test_GivenNoUserWhenRegisteringThenIsCreatedWithCorrectDataAndReturnNoError(self):
        # Given no user.

        # When registering.
        code, content = self.register()

        # Then is created with correct data and return no error.
        token = content["token"]
        success, user_data = self.user_in_db(username=self.default_username)
        self.assertTrue(success)  # If this is false then there war no user created.
        self.assertEqual(code, 200)
        self.assertEqual(True, content["success"])
        self.assertEqual(token, user_data["token"])
        self.assertNotEqual(self.default_hash, user_data["hash"])
        self.assertEqual(self.default_email, user_data["email"])

    def test_GivenNoUserWhenRegisteringWithInvalidEmailThenIsNotCreatedAndRaiseInvalidEmail(self):
        # Given no user.

        # When registering with invalid email.
        invalid_email = "invalid.email.@"
        code, content = self.register(email=invalid_email)

        # Then is not created and raise invalid email.
        success, i = self.user_in_db(self.default_username)
        self.assertEqual(400, code)
        self.assertEqual(False, content["success"])
        self.assertEqual(content["message"], InvalidEmail.description)
        self.assertFalse(success)

    def test_GivenUserWhenRegisteringWithSameUsernameThenIsNotCreatedAndRaiseUsernameTaken(self):
        # Given user.
        self.add_default_user()

        # When registering with same username.
        code, content = self.register(email="random.email@bestagram.com")

        # Then is not created and raise username taken.
        query = f"""
        SELECT * FROM UserTable
        WHERE username = "{self.default_username}";
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        self.assertEqual(len(result), 1)  # If equals two then another user has been created in db.
        self.assertEqual(400, code)
        self.assertEqual(False, content["success"])
        self.assertEqual(content["message"], UsernameTaken.description)

    def test_GivenUserWhenRegisteringWithSameEmailThenIsNotCreatedAndRaiseEmailTaken(self):
        # Given user.
        self.add_default_user()

        # When registering with same email.
        self.register()
        code, content = self.register(username="random_username")

        # Then is not created and raise email taken.
        query = f"""
        SELECT * FROM UserTable
        WHERE email = "{self.default_email}";
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        self.assertEqual(len(result), 1)  # If equals two then another user has been created in db.
        self.assertEqual(400, code)
        self.assertEqual(False, content["success"])
        self.assertEqual(content["message"], EmailTaken.description)

    def test_GivenNoUserWhenRegisteringWithTooLongUsernameThenIsNotCreatedAndRaiseInvalidUsername(self):
        # Given no user.

        # When registering with too long username.
        username = "a" * (config.MAX_USERNAME_LENGTH + 5)
        code, content = self.register(username=username)

        # Then is not created and raise invalid username.
        success, i = self.user_in_db(username)
        self.assertFalse(success)
        self.assertEqual(400, code)
        self.assertEqual(False, content["success"])
        self.assertEqual(content["message"], InvalidUsername.description)

    """
    --------------------------
    Email taken tests
    --------------------------
    """

    def test_GivenEmailNotTakenWhenCheckingIfEmailIsTakenThenIsNot(self):
        # Given email not taken.

        # When checking if email is taken.
        code, content = self.ex_request(method="GET", route=f"/email/{self.default_email}/taken")

        # Then is not.
        self.assertEqual(code, 200)
        self.assertEqual(True, content["success"])
        self.assertFalse(content["taken"])

    def test_GivenEmailTakenWhenCheckingIfEmailIsTakenThenIs(self):
        # Given email taken.
        self.add_default_user()

        # WHen checking if email is taken.
        code, content = self.ex_request(method="GET", route=f"/email/{self.default_email}/taken")

        # Then is.
        self.assertEqual(code, 200)
        self.assertEqual(True, content["success"])
        self.assertTrue(content["taken"])

    """
    --------------------------
    Post tests
    --------------------------
    """

    def test_GivenNoUserWhenPostingWithInvalidCredentialsThenRaiseInvalidCredentials(self):
        # Given no user.

        # When posting with invalid credentials.
        code, content = self.post(default=False, file=self.image_square,
                                  token="invalid_token")

        # Then raise invalid credentials.
        self.assertEqual(400, code)
        self.assertEqual(False, content["success"])
        self.assertEqual(content["message"], InvalidCredentials.description)

    def test_GivenUserWhenPostingWithValidCredentialsThenIsSuccessful(self):
        # Given user.
        # When posting with valid credentials.
        code, content = self.post(default=True, file=self.image_square)

        # Then is successful.
        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])

    def test_GivenImageIsInPortraitModeWhenPostingThenIsSuccessfulAndCreatedInCorrectSize(self):
        # Given image is in portrait mode.
        image = self.image_portrait

        # When posting.
        code, content = self.post(default=True, file=image)

        # Then is successful and created in correct size.
        self.assertEqual(code, 200)
        self.assertEqual(True, content["success"])
        new_im = Image.open(f"Medias/image/{self.default_username}/0.png")
        self.assertEqual(new_im.size, (config.IMAGE_DIMENSION, config.IMAGE_DIMENSION))
        new_im.close()

    def test_GivenImageIsInLandscapeModeWhenPostingThenIsSuccessfulAndCreatedInCorrectSize(self):
        # Given image is in landscape mode.
        image = self.image_landscape_big

        # When posting.
        code, content = self.post(default=True, file=image)

        # Then is successful and created in correct size.
        self.assertEqual(code, 200)
        self.assertEqual(True, content["success"])
        new_im = Image.open(f"Medias/image/{self.default_username}/0.png")
        self.assertEqual(new_im.size, (config.IMAGE_DIMENSION, config.IMAGE_DIMENSION))
        new_im.close()

    def test_GivenImageUnderFinalResolutionWhenPostingThenIsSuccessfulAndCreatedInCorrectSize(self):
        # Given image under final resolution.
        image = self.image_landscape_small

        # When posting.
        code, content = self.post(default=True, file=image)

        # Then is successful and created in correct size.
        self.assertEqual(code, 200)
        self.assertEqual(True, content["success"])
        new_im = Image.open(f"Medias/image/{self.default_username}/0.png")
        self.assertEqual(new_im.size, (config.IMAGE_DIMENSION, config.IMAGE_DIMENSION))
        new_im.close()

    def test_GivenPostingImageWhenRetrievingImageDataFromDatabaseThenIsCorrectData(self):
        # Given posting image.
        self.add_default_user()
        caption = "this is a caption"
        code, content = self.post(default=True, file=self.image_square, caption=caption)

        # When retrieving image data from database.
        query = """
        SELECT * FROM Post;"""  # There should be only one image inside so we can fetch everything.
        self.cursor.execute(query)
        result = self.cursor.fetchall()[0]

        self.assertEqual(result["caption"], caption)
        self.assertEqual(result["image_path"], f"Medias/image/{self.default_username}/0.png")

    """
    --------------------------
    Tag test
    --------------------------
    """

    def test_GivenHavingTagLinkingNonExistingUserWhenPostingThenDoesntAddTags(self):
        # Given having tag linking non existing user.
        tags = self.tags(5) # No user should have a id to 5 as there should only be one user in db (default)

        # When posting.
        code, content = self.post(default=True, file=self.image_square, tag=tags)

        # Then doesn't add tags.
        query = """
        SELECT * FROM Tag;
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(0, len(result))

    def test_GivenHavingTagLinkingExistingUserWhenPostingThenAddTags(self):
        # Given having tag with linking existing user.
        user1 = "john.fries"
        user2 = "titouan"
        id1 = self.add_user(username=user1)
        id2 = self.add_user(username=user2)
        tags = self.tags(id1, id2)

        # When posting.
        code, content = self.post(default=True, file=self.image_square, tag=tags)

        # Then add tags.
        query = """
                SELECT * FROM Tag;
                """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(2, len(result))

    def test_GivenTagLinkingToTheSameUserWhenPostingThenAddOnlyOne(self):
        # Given tag linking to the same user.
        id_john = self.add_user(username="john.fries")
        tags = self.tags(id_john, id_john)

        # When posting.
        code, content = self.post(default=True, file=self.image_square, tag=tags)

        # Then add only one.
        query = """
                SELECT * FROM Tag;
                """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(1, len(result))

    """    
    --------------------------
    Search test
    --------------------------
    """

    def test_GivenNoUserWhenSearchingWithEmptyStringThenReturnsNothing(self):
        code, content = self.search(default=True, search="", offset=0, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual({}, content["result"])

    def test_GivenUsersWhenSearchingWithEmptyStringThenReturnsAllOfThem(self):
        for i in range(10):
            self.add_user()

        code, content = self.search(default=True, search="",  offset=0, row_count=100)
        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(10, len(content["result"]))

    def test_GivenUsersWhenSearchingThenReturnsOnlyMatchingOnes(self):
        search = "abc"
        matching_list = [
            "ABRACADABRA",
            "gluta frisBee count",
            "abcpopo",
            "_ab_c_",
            "peopalebfjskchdy"
        ]
        non_matching_list = [
            "cba",
            "ab",
            "nonmatching",
            "should not match",
            "amazing bullet"
        ]
        for name in matching_list:
            self.add_user(username=name, name=name)
        for name in non_matching_list:
            self.add_user(username=name, name=name)

        code, content = self.search(default=True, search=search, offset=0, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(len(matching_list), len(content["result"]))

    def test_GivenRowCountIs200WhenHavingResultsOver100MatchThenStillOnlyReturn100(self):
        # (limitation in the max number of result sent back)
        for i in range(110):
            self.add_user()

        code, content = self.search(default=True, search="", offset=0, row_count=200)

        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(100, len(content["result"]))

    def test_GivenOffsetIsLessThan0WhenHavingResultsThenReturnTheResults(self):
        for i in range(10):
            self.add_user()

        code, content = self.search(default=True, search="", offset=-20, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(10, len(content["result"]))

    def test_GivenSearchingWhenHavingNumberOfResultsOverRowCountThenOnlyReturnRowCountResults(self):
        for i in range(10):
            self.add_user()
        row_count = 7

        code, content = self.search(default=True, search="", offset=0, row_count=row_count)

        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(len(content["result"]), row_count)

    def test_GivenUserFollowOtherUsersWhenSearchingThenReturnResultsWithFollowedUserFirst(self):
        followed = ["atrick", "btruck", "ctrack", "dtrock"]
        for i in followed:
            self.add_user(username=i, name=i)
            self.follow_db(default=True, username_followed=i)
        for i in range(4):
            self.add_user()

        code, content = self.search(default=True, search="", offset=0, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(8, len(content["result"]))
        for (index, element) in enumerate(followed):
            self.assertEqual(element, content["result"][str(index)]["username"])

    def test_GivenUsersFollowingOtherUsersWhenSearchingThenReturnResultsSortedByNumberOfFollower(self):
        people = ["test1", "test2", "test3", "test4"]
        for i in people:
            self.add_user(username=i, name=i)

        for (index, element) in enumerate(people):
            for i in range(len(people) - index):
                self.follow_db(default=False, username_followed=people[index + i], username=element)

        code, content = self.search(default=True, search="", offset=0, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(len(people), len(content["result"]))

    def test_GivenUsersFollowingOtherUsersAndBeenFollowedByUserSearchingWhenSearchingThenResultsSortedByNumberOfFollowThenPeopleNotFollowed(self):
        people_followed = ["test1", "test2", "test3", "test4"]
        people_not_followed = ["frenchfries", "belgiumfries"]

        for i in people_followed:
            self.add_user(username=i, name=i)
        for i in people_not_followed:
            self.add_user(username=i, name=i)

        for (index, element) in enumerate(people_followed):
            for i in range(len(people_followed) - index):
                self.follow_db(default=False, username_followed=element, username=people_followed[index + i])
            self.follow_db(default=True, username_followed=element)
        self.follow_db(default=False, username_followed=people_not_followed[0], username=people_not_followed[1])

        code, content = self.search(default=True, search="", offset=0, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(True, content["success"])
        self.assertEqual(len(people_followed) + len(people_not_followed), len(content["result"]))
        for i in range(len(people_followed)):
            # Follows have been made so that the first user of the list has the most follow and so on.
            self.assertEqual(people_followed[i], content["result"][str(i)]["username"])
        for i in range(len(people_not_followed)):
            self.assertEqual(people_not_followed[i], content["result"][str(i + len(people_followed))]["username"])

    """
    --------------------------
    Follow Tests
    --------------------------
    """

    def test_GivenNonExistingUserWhenFollowingItThenReturnNonExistingUser(self):
        code, content = self.follow_api(default=True, id_followed=123)

        self.assertFalse(content["success"])
        self.assertEqual(400, code)
        self.assertEqual(errors.UserNotExisting.get_response()[0], content)
        test_query = f"""
        SELECT * FROM Follow
        WHERE user_id_followed = {123};"""
        self.cursor.execute(test_query)
        result = self.cursor.fetchall()
        self.assertEqual(0, len(result))

    def test_GivenExistingUserWhenFollowingItThenIsSuccessfulAndFollowAddedInDatabase(self):
        id = self.add_user()
        code, content = self.follow_api(default=True, id_followed=id)

        self.assertEqual(200, code, content)
        self.assertTrue(content["success"])
        test_query = f"""
        SELECT * FROM Follow
        WHERE user_id_followed = {id};"""
        self.cursor.execute(test_query)
        result = self.cursor.fetchall()
        self.assertEqual(1, len(result))

    def test_GivenWrongTokenWhenFollowingUserThenRaiseInvalidCredentialsAndFollowNotAddedInDatabase(self):
        id = self.add_user()
        code, content = self.follow_api(default=False, id_followed=id, token="invalidtoken")

        self.assertEqual(400, code)
        self.assertEqual(errors.InvalidCredentials.get_response()[0], content)

        test_query = f"""
        SELECT * FROM Follow
        WHERE user_id_followed = {id};"""
        self.cursor.execute(test_query)
        result = self.cursor.fetchall()
        self.assertEqual(0, len(result))

    def test_GivenUserAlreadyFollowedWhenFollowingAgainThenRaiseUserAlreadyFollowed(self):
        id = self.add_user()
        self.follow_api(default=True, id_followed=id)
        code, content = self.follow_api(default=True, id_followed=id)

        self.assertEqual(400, code)
        self.assertEqual(errors.UserAlreadyFollowed.get_response()[0], content)

        test_query = f"""
                SELECT * FROM Follow
                WHERE user_id_followed = {id};"""
        self.cursor.execute(test_query)
        result = self.cursor.fetchall()
        self.assertEqual(1, len(result))

    """
    --------------------------
    Profile update tests
    --------------------------
    """

    def test_GivenNewProfileDataWhenUpdatingThenIsUpdatedInDatabase(self):
        caption = "test unique caption"
        public = False # By default profile visibility is set to public.
        new_username = "azertyuiojfkd"
        new_name = "thisismynewname"
        code, content = self.profile(default=True, public=public, caption=caption, username=new_username, name=new_name)

        get_profile_data_query = f"""
        SELECT public_profile, caption, username, name FROM UserTable
        WHERE username = "{new_username}";
        """
        self.cursor.execute(get_profile_data_query)
        result = self.cursor.fetchall()[0]
        self.assertEqual(200, code)
        self.assertEqual(content["success"], True)
        self.assertEqual(caption, result["caption"])
        self.assertEqual(public, result["public_profile"])
        self.assertEqual(new_username, result["username"])
        self.assertEqual(new_name, result["name"])

    def test_GivenNoProfilePictureWhenUpdatingWithNewProfilePictureThenIsAddedInFilesAndPathInDatabase(self):
        code, content = self.profile(default=True, image=self.image_landscape_small)

        get_profile_data_query = f"""
        SELECT profile_picture_path FROM UserTable
        WHERE username = "{self.default_username}";
        """
        self.cursor.execute(get_profile_data_query)
        result = self.cursor.fetchall()[0]
        self.assertEqual(200, code)
        self.assertEqual(content["success"], True)
        path = f'Medias/profile_picture/{self.default_username}'
        self.assertEqual(path + "/picture.png", result["profile_picture_path"])
        self.assertTrue(os.path.exists(path))
        self.assertEqual(1, len(os.listdir(path)))

    def test_GivenProfilePictureWhenUpdatingWithNewProfilePictureThenIsReplacedInFiles(self):
        # Given profile picture.
        self.profile(default=True, image=self.image_landscape_small)
        path = f"Medias/profile_picture/{self.default_username}"
        first_image = Image.open(path + "/picture.png")

        # When updating...
        code, content = self.profile(default=True, image=self.image_portrait)
        second_image = Image.open(path + "/picture.png")

        self.assertEqual(200, code)
        self.assertEqual(content["success"], True)
        self.assertEqual(1, len(os.listdir(path)))
        self.assertNotEqual(first_image, second_image)

    def test_GivenUserWhenUpdatingAnotherUserProfileWithSameUsernameThenRaiseUsernameTaken(self):
        self.add_default_user()
        token = "token"
        self.add_user(token=token)

        code, content = self.profile(default=False, username=self.default_username, token=token)

        self.assertEqual((content, code), UsernameTaken.get_response())

    def remove_all_from_db(self):
        delete_all_query = """
                DELETE FROM Follow;
                DELETE FROM Tag;
                DELETE FROM LikeTable;
                DELETE FROM Post;
                DELETE FROM UserTable;
                """
        result = self.cursor.execute(delete_all_query, multi=True)
        for i in result:
            pass

    def tearDown(self) -> None:
        self.remove_all_from_db()
        try:
            shutil.rmtree("Medias")
        except:
            pass
