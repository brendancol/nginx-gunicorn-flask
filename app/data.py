import multiprocessing
import ctypes
import numpy as np

N=int(10**4)
M=int(10**4)

# This solution example comes from:
# https://stackoverflow.com/questions/5549190/is-shared-readonly-data-copied-to-different-processes-for-multiprocessing
#
# Referenced by this one:
# https://stackoverflow.com/questions/10721915/shared-memory-objects-in-multiprocessing
#
# Anallogously, this one goes with multiprocessing Array/Value containers:
# https://stackoverflow.com/questions/14124588/shared-memory-in-multiprocessing
#
# And all started here:
# https://stackoverflow.com/questions/45071875/memory-sharing-among-workers-in-gunicorn-using-preload
#
# Eventually we got back to the original question:
# https://stackoverflow.com/questions/18213619/sharing-a-lock-between-gunicorn-workers
#
# Which next to it, the next two can be placed:
# https://stackoverflow.com/questions/27240278/sharing-memory-in-gunicorn
# https://stackoverflow.com/questions/26854594/sharing-static-global-data-among-processes-in-a-gunicorn-flask-app
#
# But effectively, it is not really about 'gunicorn', but 'multiprocessing'.
#
# If this is an acceptable solution, we should be able to explore other data
# structures/objects in accordance to 'multiprocessing'.
#

_shared_array_base = multiprocessing.Array(ctypes.c_double, N*M)
data = np.ctypeslib.as_array(_shared_array_base.get_obj())
data = data.reshape(N, M)
