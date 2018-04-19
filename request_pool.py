from multiprocessing.pool import ThreadPool
import json
import requests

def foo():
    return requests.get('http://localhost').json()

def run(N):

    pool = ThreadPool(N)
    results = []
    for i in range(N):
        results.append(pool.apply_async(foo))
    
    pool.close()
    pool.join()
    for r in results:
        print(json.dumps(r.get(), indent=4))


if __name__ == "__main__":
    import sys
    N = 5
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    run(N)
