from flask import Flask
from flask_cors import CORS

# Initial Flask application
app = Flask(__name__)
CORS(app)