import user
import werkzeug

class Profile:
    """
    Profile of a user.
    """
    def __init__(self, user):
        self.user = user
        self.cursor = user.cursor

    def update(self, caption : str = None, profile_picture : werkzeug.datastructures.FileStorage = None, public_visibility : bool = None):
        """
        Update this profile values. All arguments are optional, if they are not provided the value stay as it is.
        :param caption:
        :param profile_picture:
        :param public_visibility:
        :return:
        """
        if not (caption or profile_picture or public_visibility):
            # No data is to be changed, every argument is set to None.
            return

        update_query = """
        UPDATE UserTable SET """
        if caption:
            update_query += f"caption = {caption},"
        if public_visibility:
            update_query += f"public_profile = {public_visibility},"

        update_query = update_query[:-1] # Removes the coma ","

        update_query += f" WHERE id = {self.user.id};"
        self.cursor.execute(update_query)
