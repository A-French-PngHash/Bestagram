from flask import Flask
from flask_restful import Api
from api import login

PORT = 5002
HOST = "0.0.0.0"

app = Flask(__name__)
api = Api(app)

# Defining api resources.
api.add_resource(login.Login, "/login")

# Running the api.
app.run(host=HOST, port=PORT, ssl_context='adhoc')
