
from kq import Worker
from app import callback

worker = Worker(
    callback=callback
)

worker.start()
