from __future__ import division

import os
import sys

# - third-party
from flask import jsonify
from flask_restful import reqparse

# - app specific
from app import app

import psutil
process = psutil.Process(os.getpid())

class Server(object):
    def __init__(self):
        self.info = {"Init memory in use (Master)": process.memory_info().rss/10**6}

app.config['server'] = Server()

@app.route('/')
def root():
    info = dict(methods=['this a test'])

    info.update({"RSS memory being used (Worker)": process.memory_info().rss/10**6})
    info.update({"SHARED memory being used (Worker)": process.memory_info().shared/10**6})

    wn = os.getpid()

    srv = app.config['server']

    if wn in srv.info:
        srv.info[wn] += 1
    else:
        srv.info[wn] = 1

    info.update({"worker node '{}' has been here".format(wn) : "'{}' times".format(srv.info[wn])})

    if wn % 2:
        _ = app.config['data'].data
        info.update({"Array was read. RSS Memory in use:": process.memory_info().rss/10**6})
        info.update({"Array was read. SHARED Memory in use:": process.memory_info().shared/10**6})

    return jsonify(info)


#if __name__ == '__main__':
#    app.debug = True
#    app.run()
