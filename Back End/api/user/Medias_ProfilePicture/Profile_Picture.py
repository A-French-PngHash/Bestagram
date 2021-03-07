import flask

from errors import BestagramException
from profile import Profile

from flask_restful import Resource


class ProfilePicture(Resource):
    """
    Endpoint that holds the profile pictures.
    """

    def get(self, id):
        """
        Returns the profile picture.
        :param id:
        :return:
        """
        profile = Profile(id=id)
        try:
            profile_picture = profile.profile_picture
        except BestagramException as e:
            return e.get_response()

        response = flask.make_response(profile_picture)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set(
            'Content-Disposition', 'attachment', filename='picture.png')
        return response
