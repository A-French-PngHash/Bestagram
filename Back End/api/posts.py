from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import werkzeug
from user import User
from database.request_utils import *
from errors import *
from tag import *
from json import loads


class Post(Resource):
    """
    Retrieve or put posts using this endpoint.

    Query parameters :
        - caption
        - tag : Contain tags information (position + username of person mentioned). Must look something like this :
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

    Header :
        - Authorization
        - Username

    Files :
        - image

    """

    def put(self) -> (dict, int):
        """
        Uploading a post.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location="files")
        # Token.
        parser.add_argument("Authorization", location="headers")
        # Caption of the image.
        parser.add_argument("caption")
        # Tag included with the image.
        parser.add_argument("tag")

        params = parser.parse_args()
        tags = params["tag"]
        tags = loads(tags)

        if params["image"] == "":  # Caption is not mandatory.
            return MissingInformation.get_dictionary(), 400

        try:
            user = User(token=params["Authorization"])
        except BestagramException as e:
            return e.get_dictionary(), 400

        # This part is where we retrieve tags.
        tags_list = []

        try:
            json = tags["tags"]
            for i in json:
                tag = json[i]
                try:
                    id = get_user_id_from_username(username=tag["username"])
                    tag = Tag(user_id=id, pos_x=tag["pos_x"], pos_y=tag["pos_y"])
                    if tag not in tags_list:  # Prevent redundant tags_list with the same person tagged.
                        tags_list.append(tag)
                except UsernameNotExisting:
                    pass
                except Exception as e:
                    # Error in json. Skipping to next tag.
                    print("Error while parsing json : ", e)
        except Exception as e:
            # This code is executed if there is an error while parsing the json, we just keep the already registered
            # tags in this case.
            print("Error while parsing json : ", e)

        img = params["image"]
        user.create_post(img, caption=params["caption"], tags=tags_list)
        return {"success": True}, 200
