class InvalidCredentials(Exception):
    """
    Connection credentials are invalid.
    """

    def __init__(self, username: str = None, hash: str = None):
        self.username = username
        self.hash = hash

    def __str__(self):
        msg = "Invalid Credentials"
        if self.username:
            msg += f", username : {self.username}"
        if self.hash:
            msg += f", hash : {self.hash}"
        return msg


class UsernameTaken(Exception):
    """
    Called when a user try to register but the username he want is already taken.
    """

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

    def __init__(self, email: str = None):
        self.email = email

    def __str__(self):
        msg = "Email Taken"
        if self.email:
            msg += f" (email : {self.email})"
        return msg
