from os import path
import uuid
import json
import cStringIO as StringIO
from skimage.io import imsave, imread

from flask import Flask, send_file, jsonify, url_for

from kq import Queue
queue = Queue()

app = Flask(__name__)
app.debug = True


def update_status(msg, job_id):
    from os import path
    import json
    import datetime

    here = path.abspath(path.dirname(__file__))
    status_path = path.join(here, '{}.json'.format(str(job_id)))

    if path.exists(status_path):
        with open(status_path) as f:
            content = json.loads(f.read())
    else:
        content = []

    status_msg = dict(job=job_id,
                      status=msg,
                      date=str(datetime.datetime.now()))
    content.insert(0, status_msg)
    with open(status_path, 'w') as f:
        f.write(json.dumps(content))


def callback(status, job, result, exception,
             traceback, update_func=update_status):

    if status == 'success':
        update_func(status, job.key)

    elif status == 'timeout':
        update_func(status, job.key)

    elif status == 'failure':
        update_func(status + '\nTraceback:\n' + exception, job.key)


def run_model(job_id, update_func=update_status):

    # functions submitted via enqueue need handle their own imports
    update_func('processing-started', job_id)

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
    sleep(10)

    imsave(file_name, arr,
           plugin='pil', format_str='png')

    update_func('processing-completed', job_id)
    return file_name


@app.route('/')
def main():
    job_id = str(uuid.uuid4())
    job = queue.enqueue_with_key(job_id, run_model,
                                 job_id, update_status)
    update_status('submitted', job_id)
    return jsonify(dict(job_id=job_id,
                        link=url_for('.poll', job=job_id)))


@app.route('/<job>')
def poll(job):
    data_path = '{}.png'.format(job)
    here = path.abspath(path.dirname(__file__))
    status_path = path.join(here, '{}.json'.format(str(job)))
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
    here = path.abspath(path.dirname(__file__))
    status_path = path.join(here, '{}.json'.format(str(job)))
    if path.exists(status_path):
        with open(status_path) as f:
            content = json.loads(f.read())
        return jsonify(dict(status=content))
    else:
        return jsonify(dict())


if __name__ == '__main__':
    app.run()
