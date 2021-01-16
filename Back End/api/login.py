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
            return {"error": MissingInformation.description}, 400

        try:
            user = User(params["username"], hash=params["hash"])
        except InvalidCredentials:
            return {"error": InvalidCredentials.description}, 401

        return {"token": user.token}, 200

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
        params = parser.parse_args()

        if not (params["username"] and params["hash"] and params["email"]):
            return {"error": MissingInformation.description}, 400

        try:
            user = User.create(params["username"], hash=params["hash"], email=params["email"])
        except UsernameTaken:
            return {"error": UsernameTaken.description}, 409
        except EmailTaken:
            return {"error": EmailTaken.description}, 409
        except InvalidEmail:
            return {"error": InvalidEmail.description}, 406
        except InvalidUsername:
            return {"error": InvalidUsername.description}, 406

        return {"token": user.token}, 201
