from flask_restful import Resource, reqparse
import user
import database.mysql_connection
from errors import *


class Login(Resource):
    def post(self, username) -> (dict, int):
        """
        Getting the token by sending login data.
        :return: Return a dict containing the requested data and an int which is the http status code.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("hash")
        params = parser.parse_args()
        params["username"] = username

        if not (params["username"] and params["hash"]):
            return MissingInformation.get_response()

        try:
            userobj = user.User(params["username"], hash=params["hash"])
        except BestagramException as e:
            return e.get_response()

        return {"success": True, "token": userobj.token, "refresh_token": userobj.refresh_token, "token_expiration_date": str(userobj.token_expiration_date)}, 200

    def put(self, **kwargs) -> (dict, int):
        """
        Register a user. Returns the token.
        :return: Return a dict containing the token and an int which is the http status code.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("hash")
        parser.add_argument("email")
        parser.add_argument("name")

        params = parser.parse_args()
        params["username"] = kwargs["username"]

        if not (params["username"] and params["hash"] and params["email"] and params["name"]):
            return MissingInformation.get_response()

        try:
            userobj = user.User.create(params["username"], params["name"], hash=params["hash"], email=params["email"])
        except BestagramException as e:
            return e.get_response()
        return {"success": True, "token": userobj.token, "refresh_token": userobj.refresh_token, "token_expiration_date": str(userobj.token_expiration_date)}, 200
