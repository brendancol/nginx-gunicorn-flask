from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_cors import CORS

import logging
import logging.handlers
import os

from celery import Celery

__version__ = '0.1.0'

app = Flask(__name__)
app.debug = True


# ============================================
# Here is where we read our data structure
# and share it with the other worker through
# Flask config struct:
#
from app import data
# app.config['data'] = data.data
app.config['matrix_shape'] = data.sparse_matrix.shape
app.config['matrix_data'] = data.matrix_data
app.config['matrix_rows'] = data.matrix_rows
app.config['matrix_cols'] = data.matrix_cols
# ============================================


# Set CORS options on app configuration
app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'

cors = CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


def make_celery(app):

    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])

    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


formatter = logging.Formatter('%(asctime)s - %(name)s - \
                              %(levelname)s - %(message)s')

if not os.path.exists('./logs'):
    os.makedirs('./logs')

file_handler = logging.FileHandler('./logs/flask.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

app.logger.addHandler(file_handler)


# ============================================
# Here is where the app (practically speaking)
# in this example is loaded to next be
# instaniated in the queue/farm system
#
from app import views  # NOQA
# ============================================


celery = make_celery(app)
