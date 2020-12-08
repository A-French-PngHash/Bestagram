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

        if "username" not in params.keys() or "hash" not in params.keys():
            return {"error": "Missing information"}, 400

        try:
            user = User(params["username"], params["hash"], cursor=database.mysql_connection.cursor)
        except InvalidCredentials as e:
            return {"error": "Invalid Credentials", "code": 3}, 401

        return {"token": user.token}, 200

    def put(self) -> (dict, int):
        """
        Register a user. Returns the token. Take the following required parameters in the request :
            - username
            - hash
        :return: Return a dict containing the token and an int which is the http status code.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("hash")
        params = parser.parse_args()

        if "username" not in params.keys() or "hash" not in params.keys():
            return {"error": "Missing information"}, 400

        try:
            user = User.create(params["username"], params["hash"], cursor=database.mysql_connection.cursor)
        except UsernameTaken as e:
            return {"error": "Username already taken"}, 409

        return {"token": user.token}, 201
