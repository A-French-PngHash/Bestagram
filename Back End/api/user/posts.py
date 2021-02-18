from flask_restful import Resource, reqparse, request
import werkzeug
import user
from database import request_utils
from errors import *
import tag
import json
from PIL import Image


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
        if tags:
            tags = json.loads(tags)

        if params["image"] == "":  # Caption is not mandatory.
            return MissingInformation.get_response()

        try:
            userobj = user.User(token=params["Authorization"])
        except BestagramException as e:
            return e.get_response()

        # This part is where we retrieve tags.
        tags_list = []

        try:
            for i in tags:
                thistag = tags[i]
                try:
                    id = request_utils.get_user_id_from_username(username=thistag["username"])
                    thistag = tag.Tag(user_id=id, pos_x=thistag["pos_x"], pos_y=thistag["pos_y"])
                    if thistag not in tags_list:  # Prevent redundant tags_list with the same person tagged.
                        tags_list.append(thistag)
                except UserNotExisting:
                    pass
                except Exception as e:
                    # Error in json. Skipping to next tag.
                    print("Error while parsing json : ", e)
        except Exception as e:
            # This code is executed if there is an error while parsing the json, we just keep the already registered
            # tags in this case.
            print("Error while parsing json : ", e)

        img = Image.open(params["image"].stream)
        userobj.create_post(img, caption=params["caption"], tags=tags_list)
        return {"success": True}, 200
