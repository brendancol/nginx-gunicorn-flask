from __future__ import division

# - std library
import time

# - third-party
from flask import jsonify
from flask_restful import reqparse

# - app specific
from app import app


@app.route('/')
def root():
    info = dict(methods=['this a test'])
    return jsonify(info)


if __name__ == '__main__':
    app.debug = True
    app.run()
