import numpy as np


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

#    ind_row = np.zeros(len(rows), dtype=bool)
#    for i in row_i:
#        ind_row |= (rows == i)
#    possible_rows = np.where(ind_row)[0]
#
#    ind_col = np.zeros(len(cols), dtype=bool)
#    for i in col_i:
#        ind_col |= (cols == i)
#    possible_cols = np.where(ind_col)[0]
    possible_rows = np.where(rows == row_i)[0]
    possible_cols = np.where(cols == col_i)[0]
    # print(possible_rows)
    # print(possible_cols)

    data_elem = list(set(possible_rows).intersection(possible_cols))

    return data_elem[0] if len(data_elem) else None


def read_sparse_elements(row_is, col_is, data, rows, cols):
    assert isinstance(row_is, list) and len(row_is)
    assert isinstance(col_is, list) and len(col_is)

    from itertools import product

    pairs_out = list(product(range(len(row_is)), range(len(col_is))))
    pairs_in = list(product(row_is, col_is))
    assert len(pairs_in) == len(pairs_out)

    mat = np.zeros((len(row_is), len(col_is)))

    for i in range(len(pairs_in)):
        xy = pairs_in[i]
        # print(xy)
        data_elem = read_sparse_element(xy[0], xy[1], data, rows, cols)
        # print('Data-elem',data_elem)
        # print(mat)
        zw = pairs_out[i]
        if data_elem:
            mat[zw] = data[data_elem]
        else:
            mat[zw] = 0

    return mat
