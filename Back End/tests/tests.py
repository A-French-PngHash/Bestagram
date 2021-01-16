import unittest
import mysql.connector
from user import *
import os
import config
import database.request_utils
import shutil
import database.mysql_connection
import errors
import main
from PIL import Image


class TestsVTwo(unittest.TestCase):
    """
    This is a new test class featuring the new version of testing the backend.
    Rather than testing the class methods independently, this will actually reproduce requests to the api endpoints
    leading to more accurate tests on customer expectation.
    """

    image_square = ('test_image.png', open('test_image.png'), 'image/png')
    image_portrait = ('1280-1920.png', open('1280-1920.png'), 'image/png')
    image_landscape_big = ("3840-2160.png", open("3840-2160.png"), "image/png")
    image_landscape_small = ("474-266.png", open("474-266.png"), "image/png")
    default_hash = "hash"
    default_username = "test_username"
    default_email = "test.test@bestagram.com"
    default_json = {
        "tags":
            {
                "0":
                    {
                        "x_pos": 0.43,
                        "y_pos": 0.87,
                        "username": "john.fries"
                    },
                "1":
                    {
                        "x_pos": 0.29,
                        "y_pos": 0.44,
                        "username": "titouan"
                    }
            }
    }

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

    def add_user(self, fields: dict):
        """
        Add a user in the test database.
        :param fields: Dictionary of the field for the user. Key is the field and value is the value.

        :return:
        """
        add_user_query = """
            INSERT INTO UserTable (
            """
        # Adding columns name.
        for i in fields.keys():
            add_user_query += i + ","
        # Removing unwanted comma.
        add_user_query = add_user_query[:-1] + ") VALUES ("
        # Adding values name.
        for i in fields.values():
            add_user_query += "\"" + str(i) + "\","
        # Removing unwanted comma.
        add_user_query = add_user_query[:-1] + ");"
        self.cursor.execute(add_user_query)

    def create_db(self):
        source_file = f"\"{os.getcwd()}/test_database.sql\""
        command = """mysql -u %s -p"%s" --host %s --port %s %s < %s""" % (
            config.databaseUserName, config.password, config.host, 3306, config.databaseName, source_file)
        os.system(command)

    def add_default_user(self):
        self.add_user(
            fields={"username": self.default_username, "hash": self.default_hash, "email": self.default_email})

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

        data = dict(
            image=file,
            json=(json, "application/json")
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

    def login(self, username: str, password: str) -> (bool, str):
        """
        Login a user using provided credentials.
        :param username:
        :param password:
        :return: Return success of operation and token if successful.
        """
        code, content = self.ex_request("GET", "login",
                                        params={"username": username, "hash": password})
        if code == 200:
            return True, content["token"]
        else:
            return False, ""

    def setUp(self) -> None:
        self.create_db()
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
            # Erase directory named Posts if exists.
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
        parameters = {"username": "test", "hash": "hash", "email": "test@bestagram"}
        code, content = self.ex_request("GET", route="login", params=parameters)

        # Then return invalid credentials.
        self.assertEqual(code, 401)
        self.assertEqual(errors.InvalidCredentials.description, content["error"])

    def test_GivenUserInDatabaseWhenLoginWithIncorrectPasswordThenRaiseInvalidCredentials(self):
        # Given user in database.
        self.add_default_user()
        incorrect_hash = "incorrect"

        # When login with incorrect password.
        code, content = self.ex_request("GET", "login",
                                        params={"username": self.default_username, "hash": incorrect_hash})

        # Then raise invalid credentials.
        self.assertEqual(code, 401)
        self.assertEqual(content["error"], InvalidCredentials.description)

    def test_GivenUserInDatabaseWhenLoginWithCorrectDataThenSuccessfulLogin(self):
        # Given user in database.
        self.add_default_user()

        # When login with correct data.
        code, content = self.ex_request("GET", "login",
                                        params={"username": self.default_username, "hash": self.default_hash})

        # Then successful login.
        self.assertEqual(code, 200)

    def test_GivenUserInDatabaseWhenLoginWithoutProvidingPasswordThenRaiseMissingInformation(self):
        # Given user in database.
        self.add_default_user()

        # When login without providing password.
        code, content = self.ex_request("GET", "login", params={"username": self.default_username})

        # Then raise missing information.
        self.assertEqual(code, 400)
        self.assertEqual(MissingInformation.description, content["error"])

    def test_GivenUserInDatabaseWhenLoginWithoutProvidingUsernameThenRaiseMissingInformation(self):
        # Given user in database.
        self.add_default_user()

        # When login without providing username.
        code, content = self.ex_request("GET", "login", params={"hash": self.default_hash})

        # Then raise missing information.
        self.assertEqual(code, 400)
        self.assertEqual(MissingInformation.description, content["error"])

    """
    --------------------------
    Sign up tests
    --------------------------
    """

    def test_GivenNoUserWhenRegisteringThenIsCreatedWithCorrectDataAndReturnNoError(self):
        # Given no user.

        # When registering.
        code, content = self.ex_request("PUT", route="login", params={
            "username": self.default_username,
            "hash": self.default_hash,
            "email": self.default_email})

        # Then is created with correct data and return no error.
        token = content["token"]
        success, user_data = self.user_in_db(username=self.default_username)
        self.assertTrue(success)  # If this is false then there war no user created.
        self.assertEqual(code, 201)
        self.assertEqual(token, user_data["token"])
        self.assertEqual(self.default_hash, user_data["hash"])
        self.assertEqual(self.default_email, user_data["email"])

    def test_GivenNoUserWhenRegisteringWithInvalidEmailThenIsNotCreatedAndRaiseInvalidEmail(self):
        # Given no user.

        # When registering with invalid email.
        invalid_email = "invalid.email.@"
        code, content = self.ex_request("PUT", route="login", params={
            "username": self.default_username,
            "hash": self.default_hash,
            "email": invalid_email
        })

        # Then is not created and raise invalid email.
        success, i = self.user_in_db(self.default_username)
        self.assertEqual(code, 406)
        self.assertEqual(content["error"], InvalidEmail.description)
        self.assertFalse(success)

    def test_GivenUserWhenRegisteringWithSameUsernameThenIsNotCreatedAndRaiseUsernameTaken(self):
        # Given user.
        self.add_default_user()

        # When registering with same username.
        code, content = self.ex_request("PUT", route="login", params={
            "username": self.default_username,
            "hash": self.default_hash,
            "email": "random.email@bestagram.com"
        })

        # Then is not created and raise username taken.
        query = f"""
        SELECT * FROM UserTable
        WHERE username = "{self.default_username}";
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        self.assertEqual(len(result), 1)  # If two then another user has been created in db.
        self.assertEqual(code, 409)
        self.assertEqual(content["error"], UsernameTaken.description)

    def test_GivenUserWhenRegisteringWithSameEmailThenIsNotCreatedAndRaiseEmailTaken(self):
        # Given user.
        self.add_default_user()

        # When registering with same email.
        code, content = self.ex_request("PUT", route="login", params={
            "username": "random_username",
            "hash": self.default_hash,
            "email": self.default_email
        })

        # Then is not created and raise email taken.
        query = f"""
        SELECT * FROM UserTable
        WHERE email = "{self.default_email}";
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        self.assertEqual(len(result), 1)  # If two then another user has been created in db.
        self.assertEqual(code, 409)
        self.assertEqual(content["error"], EmailTaken.description)

    def test_GivenNoUserWhenRegisteringWithTooLongUsernameThenIsNotCreatedAndRaiseInvalidUsername(self):
        # Given no user.

        # When registering with too long username.
        username = "a" * (config.MAX_USERNAME_LENGTH + 5)
        code, content = self.ex_request("PUT", route="login", params={
            "username": username,
            "hash": self.default_hash,
            "email": self.default_email
        })

        # Then is not created and raise invalid username.
        success, i = self.user_in_db(username)
        self.assertFalse(success)
        self.assertEqual(code, 406)
        self.assertEqual(content["error"], InvalidUsername.description)

    """
    --------------------------
    Email taken tests
    --------------------------
    """

    def test_GivenEmailNotTakenWhenCheckingIfEmailIsTakenThenIsNot(self):
        # Given email not taken.

        # When checking if email is taken.
        code, content = self.ex_request(method="GET", route="/email/taken", params={"email": self.default_email})

        # Then is not.
        self.assertEqual(code, 200)
        self.assertFalse(content["taken"])

    def test_GivenEmailTakenWhenCheckingIfEmailIsTakenThenIs(self):
        # Given email taken.
        self.add_default_user()

        # WHen checking if email is taken.
        code, content = self.ex_request(method="GET", route="/email/taken", params={"email": self.default_email})

        # Then is.
        self.assertEqual(code, 200)
        self.assertTrue(content["taken"])

    """
    --------------------------
    Post tests
    --------------------------
    """

    def test_GivenNoUserWhenPostingWithInvalidCredentialsThenRaiseInvalidCredentials(self):
        # Given no user.

        # When posting with invalid credentials.
        code, content = self.ex_request(
            method="PUT",
            route="/post",
            params={"caption": "an image"},
            headers={"Authorization": "invalid_token", "username": self.default_username},
            file=self.image_square
        )

        # Then raise invalid credentials.
        self.assertEqual(code, 401)
        self.assertEqual(content["error"], InvalidCredentials.description)

    def test_GivenUserWhenPostingWithValidCredentialsThenIsSuccessful(self):
        # Given user.
        self.add_default_user()
        _, token = self.login(self.default_username, self.default_hash)

        # When posting with valid credentials.
        code, content = self.ex_request(
            method="PUT",
            route="/post",
            params={"caption": "an image"},
            headers={"Authorization": token, "Username": self.default_username},
            file=self.image_square
        )

        # Then is successful.
        self.assertEqual(code, 201)

    def test_GivenImageIsInPortraitModeWhenPostingThenIsSuccessfulAndCreatedInCorrectSize(self):
        # Given image is in portrait mode.
        image = self.image_portrait
        self.add_default_user()
        _, token = self.login(self.default_username, self.default_hash)

        # When posting.
        code, content = self.ex_request(
            method="PUT",
            route="/post",
            params={"caption": "an image"},
            headers={"Authorization": token, "Username": self.default_username},
            file=image
        )

        # Then is successful and created in correct size.
        self.assertEqual(code, 201)
        new_im = Image.open(f"Posts/{self.default_username}/0.png")
        self.assertEqual(new_im.size, (config.DEFAULT_IMAGE_DIMENSION, config.DEFAULT_IMAGE_DIMENSION))
        new_im.close()

    def test_GivenImageIsInLandscapeModeWhenPostingThenIsSuccessfulAndCreatedInCorrectSize(self):
        # Given image is in portrait mode.
        image = self.image_landscape_big
        self.add_default_user()
        _, token = self.login(self.default_username, self.default_hash)

        # When posting.
        code, content = self.ex_request(
            method="PUT",
            route="/post",
            params={"caption": "an image"},
            headers={"Authorization": token, "Username": self.default_username},
            file=image
        )

        # Then is successful and created in correct size.
        self.assertEqual(code, 201)
        new_im = Image.open(f"Posts/{self.default_username}/0.png")
        self.assertEqual(new_im.size, (config.DEFAULT_IMAGE_DIMENSION, config.DEFAULT_IMAGE_DIMENSION))
        new_im.close()

    def test_GivenImageUnderFinalResolutionWhenPostingThenIsSuccessfulAndCreatedInCorrectSize(self):
        # Given image is in portrait mode.
        image = self.image_landscape_small
        self.add_default_user()
        _, token = self.login(self.default_username, self.default_hash)

        # When posting.
        code, content = self.ex_request(
            method="PUT",
            route="/post",
            params={"caption": "an image"},
            headers={"Authorization": token, "Username": self.default_username},
            file=image
        )

        # Then is successful and created in correct size.
        self.assertEqual(code, 201)
        new_im = Image.open(f"Posts/{self.default_username}/0.png")
        self.assertEqual(new_im.size, (config.DEFAULT_IMAGE_DIMENSION, config.DEFAULT_IMAGE_DIMENSION))
        new_im.close()

    def test_GivenPostingImageWhenRetrievingImageDataFromDatabaseThenIsCorrectData(self):
        # Given posting image.
        self.add_default_user()
        _, token = self.login(self.default_username, self.default_hash)
        caption = "a big image"
        code, content = self.ex_request(
            method="PUT",
            route="/post",
            params={"caption": caption},
            headers={"Authorization": token, "Username": self.default_username},
            file=self.image_square
        )

        # When retrieving image data from database.
        query = """
        SELECT * FROM Post;""" # There should be only one image inside so we can fetch everything.
        self.cursor.execute(query)
        result = self.cursor.fetchall()[0]

        self.assertEqual(result["caption"], caption)
        self.assertEqual(result["image_path"], f"Posts/{self.default_username}/0.png")

    def test_post(self):
        self.add_default_user()
        token = User(username=self.default_username, hash=self.default_hash).token

    def tearDown(self) -> None:
        self.image_landscape_small[1].close()
        self.image_portrait[1].close()
        self.image_landscape_big[1].close()
        self.image_square[1].close()
        try:
            shutil.rmtree("Posts")
        except:
            pass
