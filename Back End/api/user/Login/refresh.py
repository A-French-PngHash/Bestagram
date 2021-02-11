from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from user import *
import database.mysql_connection


class Refresh(Resource):
    def post(self, **kwargs):
        """
        Login a user. Use this endpoint when the user has already inputed his credentials once and you have your
        refresh token.
        :return:
        """
        refresh_token = kwargs["refresh_token"]

        try:
            user = User(refresh_token=refresh_token)
        except BestagramException as e:
            return e.get_response()

        return {"success": True, "token": user.token, "token_expiration_date": str(user.token_expiration_date)}
