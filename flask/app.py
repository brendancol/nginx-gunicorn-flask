import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from flask.ext.mail import Mail, Message
from celery import Celery


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'db+mysql://parietal:parietal@localhost/processing'


# Initialize extensions
mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(bind=True)
def create_job(json):
    """ Celery task to create and process job
    """
    return job_id


@app.route('/submit', methods=['POST'])
def submit():
    validate(request.form)
    job_id = create_job.delay(request.form)
    results = {}
    results['job_id'] = job_id
    response = jsonify(results)
    response.status_code = 200 or 500 or something
    return response

if __name__ == '__main__':
    app.run(debug=True)
