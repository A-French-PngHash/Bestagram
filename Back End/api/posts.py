from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import werkzeug
from user import User
from database.mysql_connection import *
from contextlib import closing
from errors import *


class Post(Resource):
    """
    Retrieve or post posts using this endpoint.
    """
    def post(self) -> (dict, int):
        """
        Uploading a post.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location="files")
        # Token.
        parser.add_argument("Authorization", location="headers")
        # Username associated with token.
        parser.add_argument("Username", location="headers")
        # Description of the image.
        parser.add_argument("description")
        params = parser.parse_args()

        if params["image"] == "" or params["description"] == "":
            return {"error": "Missing Information"}, 400

        try:
            user = User(username=params["Username"], token=params["Authorization"], cnx=cnx)
        except InvalidCredentials as e:
            return {"error": "Invalid Credentials"}, 401

        img = params["image"]
        user.create_post(img, description=params["description"])
        return {"status": "Image Received"}, 201
