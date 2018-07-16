from __future__ import division

import os
import gc

# - third-party
from flask import jsonify

from .read_sparse import read_sparse_elements

# - app specific
from app import app

import psutil
process = psutil.Process(os.getpid())


def read_matrix(cfg, row_idx, col_idx):
    data = cfg['matrix_data']
    rows = cfg['matrix_rows']
    cols = cfg['matrix_cols']
    return read_sparse_elements(row_idx, col_idx, data, rows, cols)


@app.route('/')
def root():
    wn = os.getpid()

    if True:
        result1 = {}

        cfg = app.config

        row_idx = list(range(10))
        col_idx = list(range(10,30))
        matrix = read_matrix(cfg, row_idx, col_idx)

        s = matrix.sum()
        m = matrix.mean()

        result1["Node_id"] = wn

        result1["sum"] = str(s)
        result1["mean"] = str(m)

        if hasattr(matrix, 'any'):
            result1["ANY"] = '{}'.format(matrix.any())
            result1["matrix"] = '{}'.format(matrix)
        else:
            result1["ANY"] = '{}'.format(matrix.toarray().any())
            result1["matrix"] = '{}'.format(matrix.data)

        result1["shape"] = '{}'.format(matrix.shape)

        result = 'predict'
        a = gc.collect()
        result1["Score"] = result
        result1["Rss"] = process.memory_info().rss/10**6
        result1["Shared"] = process.memory_info().shared/10**6
        result1["gc_count1"] = a

    return jsonify(result1)
