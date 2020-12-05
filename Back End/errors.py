class Error(Exception):
    """Exception that is base class for all other error exceptions."""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidCredentials(Error):
    pass
