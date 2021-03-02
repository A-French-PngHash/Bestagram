import base64

import flask
from flask_restful import Resource, reqparse
import werkzeug
import user
from errors import *
from PIL import Image
from profile import Profile
import io


class ProfileUpdate(Resource):
    """
    This class only has one method which updates a user profile.
    """

    def patch(self) -> (dict, int):
        """
        Update a user's profile data. All arguments are optional except for the authorization token.
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location="files")
        # Token.
        parser.add_argument("Authorization", location="headers")
        # New profile's caption.
        parser.add_argument("caption")
        # User's profile state (public/private). Boolean.
        parser.add_argument("public")
        # New username.
        parser.add_argument("username")
        # New name.
        parser.add_argument("name")

        params = parser.parse_args()

        try:
            userobj = user.User(token=params["Authorization"])
        except BestagramException as e:
            return e.get_response()
        picture = None
        if params["image"]:
            picture = Image.open(params["image"].stream)
        try:
            userobj.profile.update(caption=params["caption"], public_visibility=params["public"],
                                   profile_picture=picture, username=params["username"], name=params["name"])
        except BestagramException as e:
            return e.get_response()
        return {"success": True}, 200


class ProfileRetrieving(Resource):
    """
    Retrieving profile data.
    """

    def get(self, id):
        parser = reqparse.RequestParser()

        # Token.
        parser.add_argument("Authorization", location="headers")  # Optional.

        params = parser.parse_args()

        profile = Profile(id=id)

        try:
            profile_data = profile.get(token=params["Authorization"])
        except BestagramException as e:
            response = e.get_response()
            return e.get_response()

        return {"success": True, "data": profile_data}, 200


class ProfilePicture(Resource):
    """
    Endpoint that holds the profile pictures.
    """

    def get(self, id):
        """
        Returns the profile picture.
        :param id:
        :return:
        """
        profile = Profile(id=id)
        try:
            profile_picture = profile.profile_picture
        except BestagramException as e:
            return e.get_response()

        response = flask.make_response(profile_picture)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set(
            'Content-Disposition', 'attachment', filename='picture.png')
        return response
