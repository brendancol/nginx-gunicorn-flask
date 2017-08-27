from __future__ import division

# - std library
import time

# - third-party
from flask import jsonify
from flask_restful import reqparse

# - app specific
from app import app


@app.before_first_request
def api_init():
    pass


@app.errorhandler(Exception)
def unhandled_exception(e):
    msg = 'An unknown exception'
    return api_response(msg, 500)


@app.errorhandler(500)
def unhandled_500(e):
    msg = 'An unknown exception'
    return api_response(msg, 500)


@app.errorhandler(404)
def page_not_found(e):
    msg = 'Page was not found'
    return api_response(msg, 404)


@app.errorhandler(403)
def page_forbidden(e):
    msg = 'Access Denied'
    return api_response(msg, 403)


@app.errorhandler(429)
def exceeded_usage(e):
    msg = 'Exceeded Rate Limit'
    return api_response(msg, 429)


def api_response(msg, code):
    result = {}
    result['message'] = msg
    response = jsonify(result)
    response.status_code = code
    return response


@app.route('/sleepdivision')
def sleepdivision():

    # validation & request deserialization
    parser = reqparse.RequestParser()

    parser.add_argument('sleeptime', type=int, required=False,
                        help="You must provide a sleep time")

    parser.add_argument('numerator', type=int, required=False,
                        help="You must provide a numerator")

    parser.add_argument('denominator', type=int, required=False,
                        help="You must provide a denominator")

    args = parser.parse_args()

    sleeptime = args.get('sleeptime', 5)
    numerator = args.get('numerator', 10)
    dominator = args.get('denominator', 1)

    # business logic
    time.sleep(sleeptime)
    quotient = numerator / dominator
    result = dict(quotient=quotient)

    # response serialization
    response = jsonify(result)
    response.status_code = 200
    return response


@app.route('/')
def root():
    info = dict(methods=['/sleepdivision'])
    return jsonify(info)


if __name__ == '__main__':
    app.debug = True
    app.run()
