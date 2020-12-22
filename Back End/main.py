from flask import Flask
from flask_restful import Api
from api import login
from api import email

PORT = 5002
HOST = "0.0.0.0"

app = Flask(__name__)
api = Api(app)

# Defining api resources.
api.add_resource(login.Login, "/login")
api.add_resource(email.Email, "/email/taken")

# Running the api.
app.run(host=HOST, port=PORT, ssl_context=("ApiCertificate/0.0.0.0:5002.crt", "ApiCertificate/0.0.0.0:5002.key"))
