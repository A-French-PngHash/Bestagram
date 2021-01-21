class InvalidCredentials(Exception):
    """
    Connection credentials are invalid.
    """
    description = "Invalid credentials"

    def __init__(self, username: str = None, hash: str = None, token : str = None):
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


class UsernameTaken(Exception):
    """
    Called when a user try to register but the username he want is already taken.
    """
    description = "Username already taken"

    def __init__(self, username: str = None):
        self.username = username

    def __str__(self):
        msg = "Username Taken"
        if self.username:
            msg += f" (username : {self.username})"
        return msg


class EmailTaken(Exception):
    """
    Email adress already exists in database.
    """
    description = "Email already taken"

    def __init__(self, email: str = None):
        self.email = email

    def __str__(self):
        msg = "Email Taken"
        if self.email:
            msg += f" (email : {self.email})"
        return msg


class InvalidEmail(Exception):
    """
    Email doesn't comply with the normal syntax of email addresses.
    """
    description = "Invalid email"

    def __init__(self, email: str = None):
        self.email = email

    def __str__(self):
        msg = "Invalid email"
        if self.email:
            msg += f" (email : {self.email})"
        return msg


class InvalidUsername(Exception):
    """
    Username doesn't comply with the username syntax rules.
    """
    description = "Invalid username"

    def __init__(self, username: str = None):
        self.username = username

    def __str__(self):
        msg = "Invalid username"
        if self.username:
            msg += f" (username : {self.username})"
        return msg


class InvalidName(Exception):
    """
    Name doesn't comply with the name syntax rules.
    """
    description = "Invalid name"

    def __init__(self, name: str = None):
        self.name = name

    def __str__(self):
        msg = "Invalid name"
        if self.name:
            msg += f" (name : {self.name})"
        return msg


class MissingInformation(Exception):
    """
    Request made without all required information.
    """
    description = "Missing information"


class UsernameNotExisting(Exception):
    """
    This username is not registered in the database.
    """

    def __init__(self, username: str = None):
        self.username = username

    def __str__(self):
        msg = "Username not existing"
        if self.username:
            msg += f" (username : {self.username})"
        return msg
