from os import path
import uuid
import json
import datetime
import cStringIO as StringIO
from skimage.io import imsave, imread

from flask import Flask, send_file, jsonify, url_for

from kq import Queue, Job
queue = Queue()

app = Flask(__name__)
app.debug = True


def callback(status, job, result, exception, traceback):

    # update json file status
    job_id = job.id
    status_path = '{}.json'.format(str(job_id))

    with open('/Users/bcollins/HELLLEOOOE.txt', 'w') as f:
        f.write(__file__)
        f.write(status_path)
    
    print(status_path)
    if path.exists(status_path):
        with open(status_path) as f:
            content = json.loads(f.read())
    else:
        content = []

    content.append(dict(job=job_id,
                        status=status,
                        date=str(datetime.datetime.now())))

    with open(status_path, 'w') as f:
        f.write(json.dumps(content))


    # print status
    if status == 'success':
        print('The job returned: {}'.format(result))

    elif status == 'timeout':
        print('The job took too long and timed out')

    elif status == 'failure':
        print('The job raised an exception on runtime')
        print(exception)

        # should job be resubmitted to queue?


def run_model(job_id):

    # functions submitted via enqueue need handle their own imports
    import numpy as np
    from skimage.io import imsave
    from time import sleep

    # functions submitted via enqueue need handle their own imports
    num_tiles = 20
    tile_size = 30
    arr = np.random.randint(0, 255, (num_tiles, num_tiles, 3))
    arr = arr.repeat(tile_size, axis=0).repeat(tile_size, axis=1)
    file_name = '{}.png'.format(job_id)

    # extra sleep so we can see intermediate status values
    sleep(20)

    imsave(file_name, arr,
           plugin='pil', format_str='png')

    return file_name


def update_status(msg, job_id):
    status_path = '{}.json'.format(str(job_id))
    print(status_path)
    if path.exists(status_path):
        with open(status_path) as f:
            content = json.loads(f.read())
    else:
        content = []

    content.append(dict(job=job_id,
                        status=msg,
                        date=str(datetime.datetime.now())))

    with open(status_path, 'w') as f:
        f.write(json.dumps(content))

@app.route('/')
def main():
    job_id = str(uuid.uuid4())
    job = queue.enqueue_with_key(job_id, run_model, job_id)
    update_status('submitted', job_id)
    update_status('submitted2', job_id)
    return jsonify(dict(job_id=job_id,
                        link=url_for('.poll', job=job_id)))


@app.route('/<job>')
def poll(job):
    data_path = '{}.png'.format(job)
    status_path = '{}.json'.format(job)
    if path.exists(data_path):
        arr = imread(data_path)
        str_buff = StringIO.StringIO()
        imsave(str_buff, arr, plugin='pil', format_str='png')
        str_buff.seek(0)
        return send_file(str_buff, mimetype='image/png')
    elif path.exists(status_path):
        with open(status_path) as f:
            content = json.loads(f.read())
        return jsonify(dict(status=content))

@app.route('/<job>/status')
def status(job):
    status_path = '{}.json'.format(job)
    if path.exists(status_path):
        with open(status_path) as f:
            content = json.loads(f.read())
        return jsonify(dict(status=content))
    else:
        return jsonify(dict())

if __name__ == '__main__':
    app.run()
