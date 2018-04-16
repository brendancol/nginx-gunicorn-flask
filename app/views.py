from __future__ import division

import os
import sys

import psutil
import resource

import random

N=int(10**7)

class Server(object):
    def __init__(self):
        self.array = tuple([random.random() for _ in range(N)])
        process = psutil.Process(os.getpid())
        self.data = {"Init memory in use (Master)": process.memory_info().rss}

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
    info = dict(methods=['this a test'])

    process = psutil.Process(os.getpid())
    info.update({"RSS memory being used (Worker)": process.memory_info().rss})
    info.update({"SHARED memory being used (Worker)": process.memory_info().shared})

    wn = os.getpid()

    srv = app.config['server']
    #info.update(srv.data)

    if wn in srv.data:
        srv.data[wn] += 1
    else:
        srv.data[wn] = 1

    info.update({"worker node '{}' has been here".format(wn) : "'{}' times".format(srv.data[wn])})

#    array = srv.array
#    _ = array
#
#    mem_array = sys.getsizeof(_)
#    info.update({"size in memory of the array(AAA):": mem_array})

    if wn % 2:
        _ = srv.array
        info.update({"Array was read. RSS Memory in use:": process.memory_info().rss})
        info.update({"Array was read. SHARED Memory in use:": process.memory_info().shared})


    return jsonify(info)


if __name__ == '__main__':
    app.debug = True
    app.run()
