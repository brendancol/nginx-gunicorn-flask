from app import celery

@celery.task()
def simple_sum(a, b):
    return a + b
