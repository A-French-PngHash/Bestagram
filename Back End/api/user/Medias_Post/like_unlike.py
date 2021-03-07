from flask_restful import Resource, reqparse
import user, post
import errors

class Like_Unlike(Resource):

    def post(self, id):
        parser = reqparse.RequestParser()
        # Token.
        parser.add_argument("Authorization", location="headers")
        params = parser.parse_args()

        userobj = user.User(token=params["Authorization"])
        postobj = post.Post(id, userobj)

        try:
            postobj.like()
        except errors.BestagramException as e:
            return e.get_response()

        return {"success": True}, 200

    def delete(self, id):
        parser = reqparse.RequestParser()
        # Token.
        parser.add_argument("Authorization", location="headers")
        params = parser.parse_args()

        userobj = user.User(token=params["Authorization"])
        postobj = post.Post(id, userobj)

        try:
            postobj.unlike()
        except errors.BestagramException as e:
            return e.get_response()

        return {"success": True}, 200
