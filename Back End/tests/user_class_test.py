import unittest
import mysql.connector
from user import *
import os
import config
import datetime


class TestUserClass(unittest.TestCase):
    """
    Unit testing of user class.
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

    def test_GivenNoUserWhenLoginWithUsernameNotExistingThenRaiseInvalidCredentials(self):
        # Given no user.

        triggered_invalid_credentials = False

        # When login with username not existing.
        try:
            user = User(username="notexistingusername", hash="testhash", cursor=self.cursor)
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
            user = User(username="testusername", hash=hash + "wrong", cursor=self.cursor)
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
            user = User(username=username, hash=hash, cursor=self.cursor)
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
        user = User(username=username, hash=hash, cursor=self.cursor)
        new_token = user.token

        # Then is new one.
        self.assertNotEqual(token, new_token)

    def test_givenNoUserWhenCreatingOneWithUserMethodThenIsCreatedAndWithCorrectData(self):
        # Given no user.
        username = "username"
        hash = "hash"

        # When creating one with user method.
        new_user = User.create(username=username, hash=hash, cursor=self.cursor)

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
            new_user = User.create(username=username, hash=hash, cursor=self.cursor)
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
        new_user = User.create(username=username+"e", hash=hash, cursor=self.cursor)

        # Then is created with correct data.
        self.assertIsNotNone(new_user)
        self.assertEqual(username + "e", new_user.username)
        self.assertEqual(hash, new_user.hash)

    def tearDown(self) -> None:
        pass

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
