class BestagramException(Exception):
    success = False
    description = "Error"
    errorCode = -1

    @classmethod
    def get_dictionary(cls) -> dict:
        """
        Return a dictionary describing the error that happened.
        :return: Dictionary
        """
        return {"success": cls.success, "errorCode": cls.errorCode, "message": cls.description}

    def __str__(self):
        return self.description


class InvalidCredentials(BestagramException):
    """
    Connection credentials are invalid.
    """
    success = False
    errorCode = 1
    description = "Invalid credentials"

    def __init__(self, username: str = None, hash: str = None, token: str = None):
        self.username = username
        self.hash = hash
        self.token = token

    def __str__(self):
        msg = "Invalid Credentials"
        if self.username:
            msg += f", username : {self.username}"
        if self.hash:
            msg += f", hash : {self.hash}"
        if self.token:
            msg += f", token : {self.token}"
        return msg


class UsernameTaken(BestagramException):
    """
    Called when a user try to register but the username he want is already taken.
    """
    success = False
    errorCode = 2
    description = "Username already taken"

    def __init__(self, username: str = None):
        self.username = username

    def __str__(self):
        msg = "Username Taken"
        if self.username:
            msg += f" (username : {self.username})"
        return msg


class EmailTaken(BestagramException):
    """
    Email adress already exists in database.
    """
    success = False
    errorCode = 3
    description = "Email already taken"

    def __init__(self, email: str = None):
        self.email = email

    def __str__(self):
        msg = "Email Taken"
        if self.email:
            msg += f" (email : {self.email})"
        return msg


class InvalidEmail(BestagramException):
    """
    Email doesn't comply with the normal syntax of email addresses.
    """
    success = False
    errorCode = 4
    description = "Invalid email"

    def __init__(self, email: str = None):
        self.email = email

    def __str__(self):
        msg = "Invalid email"
        if self.email:
            msg += f" (email : {self.email})"
        return msg


class InvalidUsername(BestagramException):
    """
    Username doesn't comply with the username syntax rules.
    """
    success = False
    errorCode = 5
    description = "Invalid username"

    def __init__(self, username: str = None):
        self.username = username

    def __str__(self):
        msg = "Invalid username"
        if self.username:
            msg += f" (username : {self.username})"
        return msg


class InvalidName(BestagramException):
    """
    Name doesn't comply with the name syntax rules.
    """
    success = False
    errorCode = 6
    description = "Invalid name"

    def __init__(self, name: str = None):
        self.name = name

    def __str__(self):
        msg = "Invalid name"
        if self.name:
            msg += f" (name : {self.name})"
        return msg


class MissingInformation(BestagramException):
    """
    Request made without all required information.
    """
    success = False
    errorCode = 7
    description = "Missing information"


class UsernameNotExisting(BestagramException):
    """
    This username is not registered in the database.
    """
    success = False
    errorCode = 8
    description = "Username not existing"

    def __init__(self, username: str = None):
        self.username = username

    def __str__(self):
        msg = "Username not existing"
        if self.username:
            msg += f" (username : {self.username})"
        return msg
