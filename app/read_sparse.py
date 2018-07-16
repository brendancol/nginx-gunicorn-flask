import numpy as np
from scipy import sparse


def read_sparse_element(row_i, col_i, data, rows, cols):
    '''
    Return an array from the elements in 'row_i' and 'col_i' list of indexes

    Rational: sparse matrices in python (through scipy/numpy) are represented
    in different ways (lists of lists, dictionaries or composed arrays). The
    composed/multiple arrays representation are 'CSR', 'CSC' and 'COO'.

    Here we will use 'COO' since it has a straight representation of the sparse
    matrix elements: COO is composed by three unidimensional arrays provinding
    the matrix data values, rows and columns indices where those values are
    positioned in a bidimensional representation.

    The arguments 'data', 'rows', 'cols' are the respective arguments (data,row,col)
    of the original COO sparse matrix.
    '''

    possible_rows = np.where(rows == row_i)[0]
    possible_cols = np.where(cols == col_i)[0]

    data_elem = list(set(possible_rows).intersection(possible_cols))

    return data_elem[0] if len(data_elem) else None


def read_sparse_elements(row_is, col_is, data, rows, cols):
    '''
    Here I am considering the `row_is` and `col_is` are lists
    of contiguous indexes representing slices in rows and columns, resp.
    E.g,
     * row_is = [2,3,4,5]
     * col_is = [4,5,6,7,8,9,10,11]
    '''
    assert isinstance(row_is, list) and len(row_is)
    assert isinstance(col_is, list) and len(col_is)

    from itertools import product

    pairs_out = list(product(range(len(row_is)), range(len(col_is))))
    pairs_in = list(product(row_is, col_is))
    assert len(pairs_in) == len(pairs_out)

    # If you want to have a dense matrix representing the sparse-matrix slice,
    # uncomment the lines below containing "dense_mat"
    #
    # dense_mat = np.zeros((len(row_is), len(col_is)))

    # If a dense-matrix is not of your interest, just use the "sparse_slice" path
    #
    sparse_slice = {'data': [],
                    'rows': [],
                    'cols': []}

    for i in range(len(pairs_in)):
        xy = pairs_in[i]
        zw = pairs_out[i]
        data_elem = read_sparse_element(xy[0], xy[1], data, rows, cols)
        if data_elem:
            # dense_mat[zw] = data[data_elem]
            sparse_slice['data'].append(data[data_elem])
            sparse_slice['rows'].append(zw[0])
            sparse_slice['cols'].append(zw[1])
        else:
            # dense_mat[zw] = 0
            pass

    # return dense_mat
    M = len(row_is)
    N = len(col_is)
    return sparse.coo_matrix((sparse_slice['data'],
                              (sparse_slice['rows'], sparse_slice['cols'])
                              ), shape=(M, N))
