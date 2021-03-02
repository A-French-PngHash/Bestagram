from flask_restful import Resource, reqparse
from errors import *
import user


class Search(Resource):
    def get(self) -> (int, dict):
        """
        Send the username results for a username query. Will send the result in the interval provided.
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument("search")
        parser.add_argument("offset")
        parser.add_argument("rowCount")
        parser.add_argument("Authorization", location="headers")

        params = parser.parse_args()

        # Search string is optional. User can search with an empty string.
        if not (params["offset"] and params["rowCount"] and params["Authorization"]):
            return MissingInformation.get_response()
        try:
            userobj = user.User(token=params["Authorization"])
        except BestagramException as e:
            return e.get_response()

        results = userobj.search_for(params["search"], offset=int(params["offset"]), row_count=int(params["rowCount"]))
        response = {"result": results, "success": True}
        return response, 200
