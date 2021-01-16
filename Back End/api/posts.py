from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import werkzeug
from user import User
from database.request_utils import *
from errors import *
from tag import *


class Post(Resource):
    """
    Retrieve or put posts using this endpoint.

    Query parameters :
        - caption

    Header :
        - Authorization
        - Username

    Files :
        - image

    Body :
        - json body. Contain tags information (position + username of person mentioned). Must look something like this :
        {
            "tags" :
            {
                "0" :
                {
                    "x_pos" : 0.43,
                    "y_pos" : 0.87,
                    "username" : "john.fries"
                },
                "1" :
                {
                    "x_pos" : 0.29,
                    "y_pos" : 0.44,
                    "username" : "titouan"
                }
            }
        }

    """

    def put(self) -> (dict, int):
        """
        Uploading a post.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location="files")
        # Token.
        parser.add_argument("Authorization", location="headers")
        # Username associated with token.
        parser.add_argument("Username", location="headers")
        # Caption of the image.
        parser.add_argument("caption")

        json = request.get_json()
        params = parser.parse_args()

        # This part is where we retrieve tags.
        tags = []
        try:
            json = json["tags"]
            for i in json:
                tag = json[i]
                try:
                    id = get_user_id_from_username(username=tag["username"])
                    tag = Tag(user_id=id, pos_x=tag["pos_x"], pos_y=tag["pos_y"])
                    if tag not in tags: # Prevent redundant tags with the same person tagged.
                        tags.append(tag)
                except UsernameNotExisting:
                    pass
        except Exception as e:
            # This code is executed if there is an error while retrieving the json, we just assume there is no tag in
            # this case.
            print(e)

        if params["image"] == "" or params["caption"] == "":
            return {"error": MissingInformation.description}, 400

        try:
            user = User(username=params["Username"], token=params["Authorization"])
        except InvalidCredentials:
            return {"error": InvalidCredentials.description}, 401

        img = params["image"]
        user.create_post(img, caption=params["caption"], tags=tags)
        return {"status": "Image Received"}, 201
