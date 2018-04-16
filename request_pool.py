from multiprocessing.pool import ThreadPool
import json
import requests

def foo():
    return requests.get('http://localhost').json()

N = 5

pool = ThreadPool(N)
results = []
for i in range(N):
    results.append(pool.apply_async(foo))

pool.close()
pool.join()
for r in results:
    print(json.dumps(r.get(), indent=4))
#results = [r.get() for r in results]
#print(results)

