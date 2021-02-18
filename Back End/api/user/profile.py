from flask_restful import Resource, reqparse
import werkzeug
import user
from errors import *
from PIL import Image

class Profile(Resource):
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
            userobj.profile.update(caption=params["caption"], public_visibility=params["public"], profile_picture=picture, username=params["username"], name=params["name"])
        except BestagramException as e:
            return e.get_response()
        return {"success": True}, 200