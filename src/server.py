# !/usr/bin/env python

import json
from flask import Flask, request, jsonify
import time
from multiprocessing import Process, Value

import madrid_traffic_info as mt

TRAFFIC_UPDATE_LOOP_INTERVAL = 600 # 10 minutes

# Rest API using Flask
# https://pythonbasics.org/flask-rest-api/
# https://linuxhint.com/rest_api_python/
# https://flask.palletsprojects.com/en/2.0.x/testing/#testing-json-apis


app = Flask(__name__)


@app.route('/route', methods=['POST'])
def plan_route():
    print(request.get_json())
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def update_traffic_loop(loop_on):
    # TODO move to application.py
    while True:
        if loop_on.value:
            mt.get_latest_traffic_info(debug=True)
        time.sleep(TRAFFIC_UPDATE_LOOP_INTERVAL)


if __name__ == '__main__':
    # See https://stackoverflow.com/a/39337670
    recording_on = Value('b', True)
    p = Process(target=update_traffic_loop, args=(recording_on,))
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()

