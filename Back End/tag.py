import database.mysql_connection


class Tag:
    """
    Represent a tag on a post.
    """

    def __init__(self, user_id: int, pos_x: float, pos_y: float, post_id: int= None):
        """
        Init for Tag class.

        :param user_id: User id of the user referenced.
        :param pos_x: X position of tag.
        :param pos_y: Y position of tag.
        """
        self.user_id = user_id
        self.pos_x = pos_x
        self.pos_y = pos_y

    def save(self, post_id: int):
        """
        Save this object in the Tag table.
        :param post_id:
        """
        query = f"""
        INSERT INTO Tag
        VALUES({post_id}, {self.user_id}, {self.pos_x}, {self.pos_y}); 
        """
        cursor = database.mysql_connection.cnx.cursor(dictionary=True)
        cursor.execute(query)
        cursor.close()

    def __eq__(self, other):
        try:
            return self.user_id == other.user_id
        except:
            return False
