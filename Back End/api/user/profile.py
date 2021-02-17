from flask_restful import Resource, reqparse
import werkzeug
import user
from errors import *

class Profile(Resource):
    def post(self) -> (dict, int):
        """
        Update a user's profile data. All arguments are optional except for the authorization token.
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location="files")
        # Token.
        parser.add_argument("Authorization", location="headers")
        # Caption of the image.
        parser.add_argument("caption")
        # User's profile state (public/private). Boolean.
        parser.add_argument("public")

        params = parser.parse_args()

        try:
            userobj = user.User(token=params["token"])
        except BestagramException as e:
            return e.get_response()

        userobj.profile.update(caption=params["caption"], public_visibility=params["public"])
        return {"success": True}, 200