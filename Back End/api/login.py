from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from user import *
import database.mysql_connection


class Login(Resource):
    def get(self) -> (dict, int):
        """
        Getting the token by sending login data. Takes different required arguments in the request :
            - username
            - hash
        :return: Return a dict containing the requested data and an int which is the http status code.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("hash")
        params = parser.parse_args()

        if not (params["username"] and params["hash"]):
            return MissingInformation.get_dictionary(), 400

        try:
            user = User(params["username"], hash=params["hash"])
        except BestagramException as e:
            return e.get_dictionary(), 400

        return {"success": True, "token": user.token, "token_expiration_date": str(user.token_expiration_date)}, 200

    def put(self) -> (dict, int):
        """
        Register a user. Returns the token. Take the following required parameters in the request :
            - username
            - hash
            - email
        :return: Return a dict containing the token and an int which is the http status code.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("hash")
        parser.add_argument("email")
        parser.add_argument("name")
        params = parser.parse_args()

        if not (params["username"] and params["hash"] and params["email"] and params["name"]):
            return {"error": MissingInformation.description}, 400

        try:
            user = User.create(params["username"], params["name"], hash=params["hash"], email=params["email"])
        except BestagramException as e:
            print(e.get_dictionary())
            return e.get_dictionary(), 400
        return {"success": True, "token": user.token, "token_expiration_date": str(user.token_expiration_date)}, 200
