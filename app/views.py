from __future__ import division

class Server(object):
   def __init__(self):
       self.data = {}

# - std library
import time

# - third-party
from flask import jsonify
from flask_restful import reqparse

# - app specific
from app import app

app.config['server'] = Server()

@app.route('/')
def root():
    import os
    wn = os.getpid()

    srv = app.config['server']
    if wn in srv.data:
        srv.data[wn] += 1
    else:
        srv.data[wn] = 1

    info = dict(methods=['this a test'])
    info.update({"worker node '{}' has been here".format(wn) : "'{}' times".format(srv.data[wn])})

    return jsonify(info)


if __name__ == '__main__':
    app.debug = True
    app.run()
