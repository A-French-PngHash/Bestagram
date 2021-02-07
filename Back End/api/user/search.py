from flask_restful import Resource, reqparse
from errors import *
from user import *


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
            user = User(token=params["Authorization"])
        except BestagramException as e:
            return e.get_response()

        results = user.search_for(params["search"], offset=int(params["offset"]), row_count=int(params["rowCount"]))
        dictionary = {index+int(params["offset"]):element for (index, element) in enumerate(results)}
        response = {"result": dictionary, "success": True}
        return response, 200
