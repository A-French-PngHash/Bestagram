from flask import Flask
from flask_restful import Api
from api import login
from api import email
from api import posts

PORT = 5002
HOST = "0.0.0.0"

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # Limit contents upload to 5 megabytes.

api = Api(app)

# Defining api resources.
api.add_resource(login.Login, "/login")
api.add_resource(email.Email, "/email/taken")
api.add_resource(posts.Post, "/post")


# Running the api.
app.run(host=HOST, port=PORT, ssl_context=("ApiCertificate/0.0.0.0:5002.crt", "ApiCertificate/0.0.0.0:5002.key"))
