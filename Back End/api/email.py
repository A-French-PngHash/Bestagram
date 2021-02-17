from flask_restful import Resource
from errors import *
from database import mysql_connection, request_utils


class Email(Resource):
    def get(self, **kwargs) -> (dict, int):
        """
        Check if the given email adress is already taken by someone.
        """
        params = {"email": kwargs["email"]}

        if not params["email"]:
            return MissingInformation.get_response(), 400

        taken = request_utils.value_in_database("UserTable", "email", params["email"])
        return {"success": True, "taken": taken}, 200
