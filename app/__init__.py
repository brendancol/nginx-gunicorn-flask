from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.cors import CORS

import logging
import logging.handlers
import os

__version__ = '0.1.0'

app = Flask(__name__)
app.debug = True

# Set CORS options on app configuration
app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}

cors = CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

formatter = logging.Formatter('%(asctime)s - %(name)s - \
                              %(levelname)s - %(message)s')

if not os.path.exists('./logs'):
    os.makedirs('./logs')

file_handler = logging.FileHandler('./logs/flask.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

app.logger.addHandler(file_handler)

from app import views
