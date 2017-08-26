import json
import urllib

from app import views

app = views.app.test_client()


def test_successful_sleep_division_get():
    test_job = {}
    test_job['sleeptime'] = 1
    test_job['numerator'] = 5
    test_job['denominator'] = 3

    url = '/sleepdivision?' + urllib.urlencode(test_job)
    result = app.get(url)
    assert result.status_code == 200

    result_obj = json.loads(result.data)
    assert 'quotient' in result_obj.keys()


def test_bad_input_400():
    test_job = {}
    test_job['sleeptime'] = 'jarjarbinks'

    url = '/sleepdivision?' + urllib.urlencode(test_job)
    result = app.get(url)
    assert result.status_code == 400
