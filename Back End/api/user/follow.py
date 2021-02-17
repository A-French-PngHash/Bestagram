from flask_restful import Resource, reqparse
import user
from errors import *

class Follow(Resource):
    """
    Follow a user.
    """

    def post(self, **kwargs):
        """
        Headers :
            - Authorization : Token of the current user.
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument("Authorization", location="headers")
        params = parser.parse_args()
        params["id"] = kwargs["id"]

        if not (params["id"] and params["Authorization"]):
            return MissingInformation.get_response()

        try:
            userobj = user.User(token=params["Authorization"])
        except BestagramException as e:
            return e.get_response()

        try:
            userobj.follow(int(params["id"]))
        except BestagramException as e:
            return e.get_response()
        return {"success": True}, 200
