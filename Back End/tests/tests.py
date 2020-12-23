import unittest
import mysql.connector
from user import *
import os
import config
import datetime
import database.request_utils
import werkzeug
import shutil


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
