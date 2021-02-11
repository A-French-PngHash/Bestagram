from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from user import *
import database.mysql_connection


class Login(Resource):
    def post(self, **kwargs) -> (dict, int):
        """
        Getting the token by sending login data.
        :return: Return a dict containing the requested data and an int which is the http status code.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("hash")
        params = parser.parse_args()
        params["username"] = kwargs["username"]

        if not (params["username"] and params["hash"]):
            return MissingInformation.get_response()

        try:
            user = User(params["username"], hash=params["hash"])
        except BestagramException as e:
            return e.get_response()

        return {"success": True, "token": user.token, "refresh_token": user.refresh_token, "token_expiration_date": str(user.token_expiration_date)}, 200

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
            user = User.create(params["username"], params["name"], hash=params["hash"], email=params["email"])
        except BestagramException as e:
            return e.get_response()
        return {"success": True, "token": user.token, "refresh_token": user.refresh_token, "token_expiration_date": str(user.token_expiration_date)}, 200
