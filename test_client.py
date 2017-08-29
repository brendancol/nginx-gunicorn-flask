import requests
from time import sleep


def poll(href):
    print 'polling'
    sleep(1)
    url = 'http://localhost:8000/v1{}'.format(href)
    resp = requests.get(url)
    resp_obj = resp.json()
    if resp_obj['status'] == 'COMPLETED':
        new_href = resp_obj['link']['href']
        new_url = 'http://localhost:8000/v1{}'.format(new_href)
        new_resp = requests.get(new_url)
        print new_resp.json()
        return new_resp.json()
    elif resp_obj['status'] == 'FAILED':
        print 'JOB FAILED :('
        return
    elif resp_obj['status'] == 'PENDING':
        poll(href)

params = {}
params['market'] = 'IN'
params['lob'] = 'COMMERICAL'
params['product'] = 'ALL'
params['specialties'] = ['Neurology']
params['is_open_pcp'] = False
params['include_multispecialty'] = False
params['dist_threshold'] = ["d:10"]

url = 'http://localhost:8000/v1/network'
print 'Request to start job'
resp = requests.post(url, json=params)
resp.raise_for_status()
resp_obj = resp.json()

href = resp_obj['link']['href']
poll(href)
