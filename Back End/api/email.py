from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from user import *
import database.mysql_connection
import database.request_utils
import database.mysql_connection


class Email(Resource):
    def get(self) -> (dict, int):
        """
        Check if the given email adress is already taken by someone.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        params = parser.parse_args()

        if not params["email"]:
            return {"error": "Missing information"}, 400

        taken = database.request_utils.value_in_database("UserTable", "email", params["email"], cnx=database.mysql_connection.cnx)
        return {"taken": taken}, 200
