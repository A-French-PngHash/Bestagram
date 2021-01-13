import unittest
import mysql.connector
from user import *
import os
import config
import datetime
import database.request_utils
import werkzeug
import shutil
import database.mysql_connection
from flask import Flask, request
from flask_restful import Api
from api import login, email, posts
import errors
import main

default_image_file = ('image', ('test_image.png', open('../tests/test_image.png', 'rb'), 'image/png'))

class TestsVTwo(unittest.TestCase):
    """
    This is a new test class featuring the new version of testing the backend.
    Rather than testing the class methods independently, this will actually reproduce requests to the api endpoints
    leading to more accurate tests on customer expectation.
    """

    default_hash = "hash"
    default_username = "test_username"
    default_email = "test.test@bestagram.com"

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

    def ex_request(self, method: str, route: str, params: dict = None, headers: dict = None, files: list = None,
                   payload: str = "") -> (int, dict):
        """
        Execute a request to the api using the provided parameters.

        :param method: Method to use to contact the api.
        :param route: Route leading to the resources
        :param params: Query parameters.
        :param headers: Request headers.
        :param files: File to send with the request in body.
        :param payload: Body json.

        :return: Returns status code and json content of the response.
        """
        if files is None:
            files = {}
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        response = self.client.open(
            route,
            query_string= params,
            method = method,
            headers=headers,
            data=payload
        )
        code = response.status_code
        content = response.get_json()

        return code, content

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
        code, content = self.ex_request("GET", "login", params={"username": self.default_username, "hash": incorrect_hash})

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
            "email": self.default_email}
                                   )

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

    def tearDown(self) -> None:
        try:
            shutil.rmtree("Posts")
        except:
            pass


class Tests(unittest.TestCase):
    """
    Unit testing for functions related to the database.
    """

    def create_db(self):
        source_file = f"\"{os.getcwd()}/test_database.sql\""
        command = """mysql -u %s -p"%s" --host %s --port %s %s < %s""" % (
            config.databaseUserName, config.password, config.host, 3306, config.databaseName, source_file)
        os.system(command)

    def setUp(self) -> None:
        self.create_db()
        self.test_cnx = mysql.connector.connect(
            user=config.databaseUserName,
            password=config.password,
            host=config.host,
            database="BestagramTest",
            use_pure=True)
        self.test_cnx.autocommit = True
        self.cursor = self.test_cnx.cursor(dictionary=True)
        try:
            shutil.rmtree("Posts")
        except:
            pass

    """
    --------------------------
    User functions
    --------------------------
    """

    def test_GivenNoUserWhenLoginWithUsernameNotExistingThenRaiseInvalidCredentials(self):
        # Given no user.

        triggered_invalid_credentials = False

        # When login with username not existing.
        try:
            user = User(username="notexistingusername", hash="testhash", cnx=self.test_cnx)
        # Then raise invalid credentials.
        except InvalidCredentials as e:
            triggered_invalid_credentials = True

        self.assertTrue(triggered_invalid_credentials)

    def test_givenUserWhenLoginWithWrongHashThenRaiseInvalidCredentials(self):
        # Given user.
        username = "testusername"
        hash = "thisisahash"
        self.add_user(fields={"username": username, "hash": hash})

        triggered_invalid_credentials = False

        # When login with wrong hash.
        try:
            user = User(username="testusername", hash=hash + "wrong", cnx=self.test_cnx)
        # Then raise invalid credentials.
        except InvalidCredentials as e:
            triggered_invalid_credentials = True
        self.assertTrue(triggered_invalid_credentials)

    def test_givenUserWhenLoginSuccesfullyThenRaiseNoErrorAndCorrectToken(self):
        # Given user.
        username = "username"
        hash = "hash"
        token = "token"
        token_registration = datetime.datetime.now().replace(microsecond=0)
        self.add_user(
            {"username": username, "hash": hash, "token": token, "token_registration_date": token_registration})

        # When login successfully.
        user = None
        try:
            user = User(username=username, hash=hash, cnx=self.test_cnx)
        # Then raise no error and correct token.
        except Exception as e:
            self.assertTrue(False, f"error triggered : {e}")

        self.assertEqual(token, user.token)

    def test_givenUserWithExpiredTokenWhenGettingTokenThenIsNewOne(self):
        # Given user with expired token.
        username = "username"
        hash = "hash"
        token = "token"
        # Creating an expired date by taking the date right now and removing the token expiration number of seconds
        # plus a security interval (here 2).
        token_registration = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(
            seconds=config.TOKEN_EXPIRATION + 2)
        self.add_user(
            {"username": username, "hash": hash, "token": token, "token_registration_date": token_registration})

        # When getting token.
        user = User(username=username, hash=hash, cnx=self.test_cnx)
        new_token = user.token

        # Then is new one.
        self.assertNotEqual(token, new_token)

    def test_givenNoUserWhenCreatingOneWithUserMethodThenIsCreatedAndWithCorrectData(self):
        # Given no user.
        username = "username"
        hash = "hash"

        # When creating one with user method.
        new_user = User.create(username=username, hash=hash, cnx=self.test_cnx, email="email")

        # Then is created with correct data.
        self.assertIsNotNone(new_user)
        self.assertEqual(username, new_user.username)
        self.assertEqual(hash, new_user.hash)

    def test_givenUserExistWhenCreatingOneWithSameUsernameThenIsNotCreatedAndRaiseErrors(self):
        # Given user exist.
        username = "username"
        hash = "hash"
        self.add_user({"username": username, "hash": hash})

        raise_error = False
        new_user = None
        # When creating one with same username.
        try:
            new_user = User.create(username=username, hash=hash, cnx=self.test_cnx, email="email")
        except UsernameTaken:
            raise_error = True

        # Then is not created and raise errors.
        self.assertIsNone(new_user)
        self.assertTrue(raise_error)

    def test_givenUserExistWhenCreatingOneWithDifferentUsernameThenIsCreatedAndWithCorrectData(self):
        # Given no user.
        username = "username"
        hash = "hash"
        self.add_user({"username": username, "hash": hash})

        # When creating one with user method.
        new_user = User.create(username=username + "e", hash=hash, cnx=self.test_cnx, email="email")

        # Then is created with correct data.
        self.assertIsNotNone(new_user)
        self.assertEqual(username + "e", new_user.username)
        self.assertEqual(hash, new_user.hash)

    """
    --------------------------
    Check if value exist
    --------------------------
    """

    def testGivenEmailInDatabaseWhenCheckingIfExistThenIsTrue(self):
        # Given email in database.
        email = "test@bestagram.com"
        self.add_user({"username": "t", "hash": "t", "email": email})

        # When checking if exist.
        exist = database.request_utils.value_in_database("UserTable", "email", email, cnx=self.test_cnx)

        # Then is true.
        self.assertTrue(exist)

    def testGivenEmailNotInDatabaseWhenCheckingIfExistThenIsFalse(self):
        # Given email not in database.
        email = "notexisting@bestagram.com"

        # When checking if exist.
        exist = database.request_utils.value_in_database("UserTable", "email", email, cnx=self.test_cnx)

        # Then is false.
        self.assertFalse(exist)

    """
    --------------------------
    Create post functions.
    --------------------------
    """

    def test_givenNoDirectoryForStoringImagesWhenPreparingDirectoryForUserThenIsCreatedCorrectly(self):
        # Given no directory for storing images.
        try:
            shutil.rmtree("Posts")
        except:
            pass

        # When preparing directory for user.
        name = "test"
        hash = "hash"
        self.add_user({"username": name, "hash": hash})
        user = User(name, self.test_cnx, hash=hash)
        user.prepare_directory()

        # Then is created correctly.
        self.assertTrue(os.path.exists(f"Posts/{name}"))

    def test_givenNoImageInDatabaseWhenCreatingImageThenIsInDatabaseWithCorrectData(self):
        # Given no image in database.
        name = "test"
        hash = "hash"
        self.add_user({"username": name, "hash": hash})

        # When creating image.
        user = User(name, self.test_cnx, hash=hash)
        description = "Test image."
        with open("test_image.png", "r") as img:
            image = werkzeug.datastructures.FileStorage(img)
            print(image)
            user.create_post(image=image, description=description)
            image.close()

        # Then is in database with correct data.
        get_post_query = f"""
        SELECT * FROM Post
        WHERE user_id = {user.id};
        """
        self.cursor.execute(get_post_query)
        result = self.cursor.fetchall()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["description"], description)

    def tearDown(self) -> None:
        try:
            shutil.rmtree("Posts")
        except:
            pass
        pass
