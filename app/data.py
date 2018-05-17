import multiprocessing
import numpy as np
# import ctypes

from os import path
here = path.abspath(path.dirname(__file__))
datadir = path.join(here, 'sample_data')

# N=int(10**4)
# M=int(10**4)
#
# _shared_array_base = multiprocessing.Array(ctypes.c_double, N*M)
# data = np.ctypeslib.as_array(_shared_array_base.get_obj())
# data = data.reshape(N, M)

# Instead of generating the 'data' as done before (above comment lines)
# we will now load the array in the file 'random.npy'.
# The array in 'random.npy' was created as
# > arr = np.random.random(10**7)
# > np.save('random.npy', arr, allow_pickle=False)
# Pickle was disabled to guarantee the object file will be read by other systems.
#
fname = path.join(datadir, 'random.npy')
arr = np.load(fname, mmap_mode=None, allow_pickle=False)

arr = multiprocessing.Array(arr.dtype.kind, arr)
data = np.ctypeslib.as_array(arr.get_obj())
data = data.reshape(10**3, 10**4)
