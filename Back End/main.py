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
<<<<<<< HEAD
app.run(host=HOST, port=PORT)#, ssl_context=("ApiCertificate/cert.pem", "ApiCertificate/key.pem"))
=======
app.run(host=HOST, port=PORT, ssl_context=("ApiCertificate/0.0.0.0:5002.crt", "ApiCertificate/0.0.0.0:5002.key"))
>>>>>>> LoginApi
