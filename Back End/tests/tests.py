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
import json
import random


class TestsVTwo(unittest.TestCase):
    """
    This is a new test class featuring the new version of testing the backend.
    Rather than testing the class methods independently, this will actually reproduce requests to the api endpoints
    leading to more accurate tests on customer expectation.
    """
    @property
    def image_square(self):
        with open('test_image.png') as file:
            return ('test_image.png', file, 'image/png')

    @property
    def image_portrait(self):
        with open('1280-1920.png') as file:
            return ('1280-1920.png', file, 'image/png')

    @property
    def image_landscape_big(self):
        with open("3840-2160.png") as file:
            return ("3840-2160.png", file, "image/png")

    @property
    def image_landscape_small(self):
        with open("474-266.png") as file:
            return ("474-266.png", file, "image/png")

    default_hash = "hash"
    default_username = "test_username"
    default_name = "test_name"
    default_email = "test.test@bestagram.com"
    default_tags = {"tags": {"0": {"pos_x": 0.43, "pos_y": 0.87, "username": "john.fries"},
                             "1": {"pos_x": 0.29, "pos_y": 0.44, "username": "titouan"}}}

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

    def add_user(self, username: str = None, email: str = None, name: str = None, hash: str = None):
        """
        Add a user in the test database.
        :param username: Username of the user to add. Optional.
        :param email: Email of the user. Optional.
        :param name: Name of the user. Optional.
        :param hash: Hash of the user. Optional.

        If the email, name or hash is not provided, they will be generated randomly.

        :return:
        """
        if not username:
            username = self.random_string(config.MAX_USERNAME_LENGTH)
        if not email:
            email = self.random_string(8) + "." + self.random_string(8) + "@" + self.random_string(
                5) + "." + self.random_string(4)
        if not name:
            name = self.random_string(config.MAX_NAME_LENGTH)
        if not hash:
            #  TODO: When implementing hash verification change this value.
            hash = self.random_string(50)

        add_user_query = f"""
        INSERT INTO UserTable (username, name, email, hash)
        VALUES ("{username}", "{name}", "{email}", "{hash}");
        """
        self.cursor.execute(add_user_query)

    def create_db(self):
        source_file = f"\"{os.getcwd()}/test_database.sql\""
        command = """mysql -u %s -p"%s" --host %s --port %s %s < %s""" % (
            config.databaseUserName, config.password, config.host, 3306, config.databaseName, source_file)
        os.system(command)

    def add_default_user(self):
        self.add_user(username=self.default_username,
                      name=self.default_name,
                      hash=self.default_hash,
                      email=self.default_email)

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

        authorization = token
        if default:
            if not self.user_in_db(self.default_username)[0]:
                self.add_default_user()
            _, authorization = self.login(self.default_username, self.default_hash)

        # When posting with valid credentials.

        code, content = self.ex_request(
            method="PUT",
            route="/post",
            params={"caption": caption, "tag": json.dumps(tag)},
            headers={"Authorization": authorization},
            file=file
        )
        return code, content

    def search(self, default: bool, search: str, offset: int, row_count: int, token: str = None) -> tuple:
        authorization = token
        if default:
            if not self.user_in_db(self.default_username)[0]:
                self.add_default_user()
            _, authorization = self.login(self.default_username, self.default_hash)

        code, content = self.ex_request(
            method="GET",
            route="/search",
            params={"rowCount": row_count, "search": search, "offset": offset},
            headers={"Authorization": authorization}
        )
        return code, content

    def follow(self, default: bool, user_id_followed: int = None, username_followed : str = None, user_id: int = None, username: str = None):
        """
        Add follow relation from one user to another.
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
        self.assertEqual(401, code)
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
            "name": self.default_name,
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
            "name": self.default_name,
            "hash": self.default_hash,
            "email": invalid_email
        })

        # Then is not created and raise invalid email.
        success, i = self.user_in_db(self.default_username)
        self.assertEqual(406, code)
        self.assertEqual(content["error"], InvalidEmail.description)
        self.assertFalse(success)

    def test_GivenUserWhenRegisteringWithSameUsernameThenIsNotCreatedAndRaiseUsernameTaken(self):
        # Given user.
        self.add_default_user()

        # When registering with same username.
        code, content = self.ex_request("PUT", route="login", params={
            "username": self.default_username,
            "name": self.default_name,
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
            "name": self.default_name,
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
            "name": self.default_name,
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
        code, content = self.post(default=False, file=self.image_square,
                                  token="invalid_token")

        # Then raise invalid credentials.
        self.assertEqual(code, 401)
        self.assertEqual(content["error"], InvalidCredentials.description)

    def test_GivenUserWhenPostingWithValidCredentialsThenIsSuccessful(self):
        # Given user.
        # When posting with valid credentials.
        code, content = self.post(default=True, file=self.image_square)

        # Then is successful.
        self.assertEqual(201, code, content)

    def test_GivenImageIsInPortraitModeWhenPostingThenIsSuccessfulAndCreatedInCorrectSize(self):
        # Given image is in portrait mode.
        image = self.image_portrait

        # When posting.
        code, content = self.post(default=True, file=image)

        # Then is successful and created in correct size.
        self.assertEqual(code, 201)
        new_im = Image.open(f"Posts/{self.default_username}/0.png")
        self.assertEqual(new_im.size, (config.DEFAULT_IMAGE_DIMENSION, config.DEFAULT_IMAGE_DIMENSION))
        new_im.close()

    def test_GivenImageIsInLandscapeModeWhenPostingThenIsSuccessfulAndCreatedInCorrectSize(self):
        # Given image is in landscape mode.
        image = self.image_landscape_big

        # When posting.
        code, content = self.post(default=True, file=image)

        # Then is successful and created in correct size.
        self.assertEqual(code, 201)
        new_im = Image.open(f"Posts/{self.default_username}/0.png")
        self.assertEqual(new_im.size, (config.DEFAULT_IMAGE_DIMENSION, config.DEFAULT_IMAGE_DIMENSION))
        new_im.close()

    def test_GivenImageUnderFinalResolutionWhenPostingThenIsSuccessfulAndCreatedInCorrectSize(self):
        # Given image under final resolution.
        image = self.image_landscape_small

        # When posting.
        code, content = self.post(default=True, file=image)

        # Then is successful and created in correct size.
        self.assertEqual(code, 201)
        new_im = Image.open(f"Posts/{self.default_username}/0.png")
        self.assertEqual(new_im.size, (config.DEFAULT_IMAGE_DIMENSION, config.DEFAULT_IMAGE_DIMENSION))
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
        self.assertEqual(result["image_path"], f"Posts/{self.default_username}/0.png")

    """
    Tag test
    """

    def test_GivenHavingTagLinkingNonExistingUserWhenPostingThenDoesntAddTags(self):
        # Given having tag linking existing user.
        tags = self.default_tags

        # When posting.
        code, content = self.post(default=True, file=self.image_square, tag=tags)

        # Then doesn't add tags.
        query = """
        SELECT * FROM Tag;
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.assertEqual(201, code)
        self.assertEqual(0, len(result))

    def test_GivenHavingTagLinkingExistingUserWhenPostingThenAddTags(self):
        # Given having tag with linking existing user.
        self.add_user(username="john.fries")
        self.add_user(username="titouan")
        tags = self.default_tags

        # When posting.
        code, content = self.post(default=True, file=self.image_square, tag=tags)

        # Then add tags.
        query = """
                SELECT * FROM Tag;
                """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.assertEqual(201, code)
        self.assertEqual(2, len(result))

    def test_GivenTagLinkingToTheSameUserWhenPostingThenAddOnlyOne(self):
        # Given tag linking to the same user.
        self.add_user(username="john.fries")
        tags = {"tags": {"0": {"pos_x": 0.5, "pos_y": 0.3, "username": "john.fries"},
                         "1": {"pos_x": 0.3, "pos_y": 0.5, "username": "john.fries"}}}

        # When posting.
        code, content = self.post(default=True, file=self.image_square, tag=tags)

        # Then add only one.
        query = """
                SELECT * FROM Tag;
                """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.assertEqual(201, code)
        self.assertEqual(1, len(result))

    """    
    --------------------------
    Search test
    --------------------------
    """

    def test_GivenNoUserWhenSearchingWithEmptyStringThenReturnsNothing(self):
        code, content = self.search(default=True, search="", offset=0, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(content, {})

    def test_GivenUsersWhenSearchingWithEmptyStringThenReturnsAllOfThem(self):
        for i in range(10):
            self.add_user()

        code, content = self.search(default=True, search="",  offset=0, row_count=100)
        self.assertEqual(200, code)
        self.assertNotEqual({}, content)
        self.assertEqual(10, len(content))

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
        self.assertEqual(len(matching_list), len(content))

    def test_GivenRowCountIs200WhenHavingResultsOver100MatchThenOnlyReturn100(self):
        for i in range(150):
            self.add_user()

        code, content = self.search(default=True, search="", offset=0, row_count=200)

        self.assertEqual(200, code)
        self.assertEqual(100, len(content))

    def test_GivenOffsetIsLessThan0WhenHavingResultsThenReturnTheResults(self):
        for i in range(10):
            self.add_user()

        code, content = self.search(default=True, search="", offset=-20, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(10, len(content))

    def test_GivenSearchingWhenHavingNumberOfResultsOverRowCountThenOnlyReturnRowCountResults(self):
        for i in range(10):
            self.add_user()
        row_count = 7

        code, content = self.search(default=True, search="", offset=0, row_count=row_count)

        self.assertEqual(200, code)
        self.assertEqual(len(content), row_count)

    def test_GivenUserFollowOtherUsersWhenSearchingThenReturnResultsWithFollowedUserFirst(self):
        followed = ["atrick", "btruck", "ctrack", "dtrock"]
        for i in followed:
            self.add_user(username=i, name=i)
            self.follow(default=True, username_followed=i)
        for i in range(4):
            self.add_user()

        code, content = self.search(default=True, search="", offset=0, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(8, len(content))
        for (index, element) in enumerate(followed):
            self.assertEqual(element, content[str(index)])

    def test_GivenUsersFollowingOtherUsersWhenSearchingThenReturnResultsSortedByNumberOfFollower(self):
        people = ["test1", "test2", "test3", "test4"]
        for i in people:
            self.add_user(username=i, name=i)

        for (index, element) in enumerate(people):
            for i in range(len(people) - index):
                self.follow(default=False, username=element, username_followed=people[index+i])

        code, content = self.search(default=True, search="", offset=0, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(len(people), len(content))

    def test_GivenUsersFollowingOtherUsersAndBeenFollowedByUserSearchingWhenSearchingThenResultsSortedByNumberOfFollowThenPeopleNotFollowed(self):
        people_followed = ["test1", "test2", "test3", "test4"]
        people_not_followed = ["frenchfries", "belgiumfries"]

        for i in people_followed:
            self.add_user(username=i, name=i)
        for i in people_not_followed:
            self.add_user(username=i, name=i)

        for (index, element) in enumerate(people_followed):
            for i in range(len(people_followed) - index):
                self.follow(default=False, username=people_followed[index + i], username_followed=element)
            self.follow(default=True, username_followed=element)
        self.follow(default=False, username=people_not_followed[1], username_followed=people_not_followed[0])

        code, content = self.search(default=True, search="", offset=0, row_count=100)

        self.assertEqual(200, code)
        self.assertEqual(len(people_followed) + len(people_not_followed), len(content))
        for i in range(len(people_followed)):
            # Follows have been made so that the first user of the list has the most follow and so on.
            self.assertEqual(people_followed[i], content[str(i)])
        for i in range(len(people_not_followed)):
            self.assertEqual(people_not_followed[i], content[str(i + len(people_followed))])

    def tearDown(self) -> None:
        try:
            shutil.rmtree("Posts")
        except:
            pass
