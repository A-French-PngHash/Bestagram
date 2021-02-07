from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from user import *
import database.mysql_connection
import database.request_utils
import database.mysql_connection


class Email(Resource):
    def get(self, **kwargs) -> (dict, int):
        """
        Check if the given email adress is already taken by someone.
        """
        params = {"email": kwargs["email"]}

        if not params["email"]:
            return MissingInformation.get_response(), 400

        taken = database.request_utils.value_in_database("UserTable", "email", params["email"])
        return {"success": True, "taken": taken}, 200
