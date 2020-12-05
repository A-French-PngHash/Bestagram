from flask import Flask, request
from flask_restful import Resource, Api, reqparse


class Login(Resource):
    def get(self):
        """
        Getting the token by sending login data.
        :return:
        """

        # This request takes two argument.
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("hash")
        params = parser.parse_args()

        if "username" not in params.keys() or "hash" not in params.keys():
            return {"error": "Missing information"}, 400

        return {"test": "successful"}, 200
