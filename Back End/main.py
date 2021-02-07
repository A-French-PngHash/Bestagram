from flask import Flask
from flask_restful import Api
from api import email
from api.user import posts, login, follow, search
import database.mysql_connection
import config
import mysql.connector

PORT = 5002
HOST = "0.0.0.0"

"""
WARNING: 
Endpoint classes are not that much documented as all of the documentation is in "api/Api Documentation.md".
Consult that file to get information on how to contact these endpoints to get access to the right data.
"""

#TODO: Add hash verification


app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Limit contents upload to 5 megabytes.

api = Api(app)

# Establishing connection.
database.mysql_connection.cnx = mysql.connector.connect(
    user=config.databaseUserName,
    password=config.password,
    host=config.host,
    database=config.databaseName,
    use_pure=True)
database.mysql_connection.cnx.autocommit = True

# Defining api resources.
api.add_resource(login.Login, "/user/login/<username>") # Done
api.add_resource(email.Email, "/email/<email>/taken") # Done
api.add_resource(posts.Post, "/user/post") # Done
api.add_resource(search.Search, "/user/search")
api.add_resource(follow.Follow, "/user/<id>/follow") # Done


if __name__ == "__main__":
    # Running the api.
    app.run(host=HOST, port=PORT, ssl_context=("ApiCertificate/0.0.0.0:5002.crt", "ApiCertificate/0.0.0.0:5002.key"))
