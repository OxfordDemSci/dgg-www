from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

from app import routes

# Cross Origin Resource Sharing (for AJAX)
CORS(app)

# specify the Google Analytics key here
app.config["GA_KEY"] = ''
