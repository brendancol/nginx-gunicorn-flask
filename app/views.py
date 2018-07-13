from __future__ import division

import os
import random
import gc

# - third-party
from flask import jsonify
import numpy as np
# from scipy import sparse

from .read_sparse import read_sparse_elements

# - app specific
from app import app

import psutil
process = psutil.Process(os.getpid())

# from memory_profiler import profile
# # create logger
# import logging
# logger = logging.getLogger('memory_profile_log')
# logger.setLevel(logging.DEBUG)
#
# # create file handler which logs even debug messages
# fh = logging.FileHandler("/tmp/gunicorn_leak/memory_profile.log")
# fh.setLevel(logging.DEBUG)
#
# # add the handlers to the logger
# logger.addHandler(fh)
#
# from memory_profiler import LogFile
# import sys
# sys.stdout = LogFile('memory_profile_log', reportIncrementFlag=False)


# # @profile
def predict(buf):
    #start = gtrc()
    # Idx1 = random.randint(54,999)
    # Idx2 = random.randint(50,999)
    # d1 = data[Idx1]
    # d2 = data[Idx2]
#    ts1 =2+np.dot(app.config['data'][Idx1],app.config['data'][Idx2])
    # s=0
    # for v in d1*d2:
    #     s+=v
    # a = sum(d1*d2)
    # b = np.dot(d1, d2)
    data = array_from_buffer(buf)
    # data * 1
    r = type(buf).from_buffer(data + data)
    # assert a==b
    # a = np.ones(10000)
    # b = np.ones(10000)
    # c = np.dot(a,b)
    # tracer.runfunc(np.dot, d1, d2)
    # r = tracer.results()
    # r.write_results(summary=True)
    # ts1 = 2 #+ np.dot(d1, d2)
    # return ts1


def array_from_buffer(buf):
    data = np.frombuffer(buf)#.get_obj())
    # data = data.reshape(N, M)
    return data


# def read_matrix(app, idx_0=None, idx_1=None):
#     shape = app.config['matrix_shape']
#     data = app.config['matrix_data']
#     indices = app.config['matrix_indices']
#     indptr = app.config['matrix_indptr']
#     sparse_matrix = sparse.csr_matrix((data, indices, indptr),
#                                       shape=shape, copy=False)
#     return sparse_matrix
def read_matrix(app, row_idx, col_idx):
    data = app.config['matrix_data']
    rows = app.config['matrix_rows']
    cols = app.config['matrix_cols']
    return read_sparse_elements(row_idx, col_idx, data, rows, cols)


@app.route('/')
def root():
    # h=hpy()
    wn = os.getpid()
    # srv = app.config['server']
    # if wn in srv.info:
    #     srv.info[wn] += 1
    # else:
    #     srv.info[wn] = 1

    if True:
        result1 = {}

        Idx1 = random.randint(54,999)
        Idx2 = random.randint(50,999)
        # d1 = data[Idx1]
        # d2 = data[Idx2]

        row_idx = list(range(10))
        col_idx = list(range(10,30))
        matrix = read_matrix(app, row_idx, col_idx)
        # matrix = read_matrix(app)

        # predict(matrix)
        s = matrix.sum()
        m = matrix.mean()

        result1["Node_id"] = wn

        result1["sum"] = s
        result1["mean"] = m
        result1["ANY"] = '{}'.format(matrix.any())
        result1["shape"] = '{}'.format(matrix.shape)

        result = 'predict'
        a = gc.collect()
        result1["Score"] = result
        result1["Rss"] = process.memory_info().rss/10**6
        result1["Shared"] = process.memory_info().shared/10**6
        result1["gc_count1"] = a

    # srv.cnt += 1

    return jsonify(result1)
