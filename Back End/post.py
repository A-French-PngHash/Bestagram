import os
import database.mysql_connection
import config
from PIL import Image
import errors
import files
import images
import tag


class Post:
    """
    This class is managing a post uploaded by a user. You will note that the api calls refer to them as "medias". They
    are the same thing. The name "media" was chosen to prevent confusion with the POST http query which has nothing to
    do with this entity. It was also chosen to be more global as it also includes a user's profile picture. So when
    referring to a media it can either be a profile picture or a post.

    In the file structure you will also note that there is a "Medias" directory. This encompasses both the profile
    pictures and the post's image (located under Medias/image). Under the image directory, each user has a sub
    directory. This sub directory is named after the user's id. In those directories you will find all the images posted
    by this user. The name of an image is its id in the database. As you can understand, you can reconstruct the path
    leading to an image (if you have the post id and the user id), that's why this path is not stored in the database.
    """

    def __init__(self, id: int, user):
        """
        User object is used as a way to allow to get the post data. If the original poster's account is private then
        only its follower can see the post.
        If the user is the original poster then modification is allowed.

        :param id: Post's id.
        :param user: User who is accessing the post.
        :type user: user.User
        :type cursor: mysql.connector.connection.MySQLCursor
        """
        self.cursor = database.mysql_connection.cnx.cursor(dictionary=True)

        self._user = user
        self._id = id

        original_poster_id_query = f"""SELECT user_id FROM Post WHERE id = {id};"""
        self.cursor.execute(original_poster_id_query)
        self._original_poster_id = self.cursor.fetchall()[0]["user_id"]

        self._can_modify = False
        self._can_access_post = False
        if self._user.id == self._original_poster_id:  # User accessing post is OP.
            self._can_modify = True
            self._can_access_post = True

        original_poster_account_status_query = f"""SELECT public_profile FROM UserTable WHERE id = {self._original_poster_id};"""
        self.cursor.execute(original_poster_account_status_query)
        public_profile = self.cursor.fetchall()[0]["public_profile"]
        self._can_access_post = public_profile

        if not self._can_access_post:  # At that point it means the account is private. The user accessing the post
            # must be following the OP to access the post.
            is_following_query = f"""SELECT * FROM Follow WHERE user_id = {self._user.id} && user_id_followed = {self._original_poster_id};"""
            self.cursor.execute(is_following_query)
            is_following = len(self.cursor.fetchall()) == 1
            self._can_access_post = is_following

        if not self._can_access_post:  # The user is not allowed to view this post.
            raise errors.PostAccessRestricted()

        post_data_query = f"""SELECT * FROM Post WHERE id = {self.id};"""
        self.cursor.execute(post_data_query)
        result = self.cursor.fetchall()[0]
        self._post_time = result["post_time"]
        self._caption = result["caption"]

    @property
    def id(self):  # Only a getter.
        return self._id

    @property
    def post_time(self):
        return self._post_time

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        if self._can_modify:
            pass
            # TODO: Change value in db.

    def like(self):
        """
        Like this post.
        :return:
        """
        like_query = f"""INSERT INTO LikeTable (user_id, post_id) VALUES ({self._user.id}, {self.id});"""
        try:
            self.cursor.execute(like_query)
        except:
            # Post's already liked by this user.
            raise errors.PostAlreadyLiked()

    def unlike(self):
        unlike_query = f"""DELETE FROM LikeTable WHERE post_id = {self.id} && user_id = {self._user.id};"""
        try:
            self.cursor.execute(unlike_query)
        except:
            # Post's not liked by this user.
            raise errors.PostNotLiked()

    @staticmethod
    def create(user, image: Image, caption: str, tags: [tag.Tag]):
        """
        Create a post..
        :param image: Post's image.
        :param caption: Caption provided with the post.
        :param tags: List of this post's tags.
        :type user: user.User
        :return: The id of the newly created post.
        """
        files.prepare_directory(user.directory)

        resized_image = images.resize_image(image, config.IMAGE_DIMENSION)

        create_post_query = f"""
        START TRANSACTION;
            INSERT INTO Post
            VALUES(
            NULL, {user.id}, NOW(), "{caption}"
            );

            SELECT LAST_INSERT_ID();
        COMMIT;
        """

        iterable = user.cursor.execute(create_post_query, multi=True)
        # 4 request are made a the same time. The third is the select one.
        index = 0
        result: list = []

        for i in iterable:
            if index == 2:
                result = i.fetchall()
            index += 1

        post_id = result[0]["LAST_INSERT_ID()"]

        image.filename = f"{post_id}.png"
        # Dir where the image is stored.
        final_image_path = os.path.join(user.directory, image.filename)
        # Saving image.
        resized_image.save(final_image_path)

        for i in tags:
            try:
                i.save(post_id)
            except errors.UserNotExisting:
                print(f"User not existing. post_id : {post_id}, user_id : {i.user_id}")
        return Post(id=post_id, user=user)
