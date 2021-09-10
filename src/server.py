# !/usr/bin/env python

import json
from flask import Flask, request, jsonify
import time
from multiprocessing import Process, Value

import app_create
import traffic

TRAFFIC_UPDATE_LOOP_INTERVAL = 600  # 10 minutes

# Rest API using Flask
# https://pythonbasics.org/flask-rest-api/
# https://linuxhint.com/rest_api_python/
# https://flask.palletsprojects.com/en/2.0.x/testing/#testing-json-apis


app = Flask(__name__)


@app.route('/route', methods=['POST'])
def plan_route():
    # TODO add logging
    req_data = request.get_json()
    print(req_data["src"])
    print(req_data["dst"])
    origin_point = (req_data["src"]["lon"], req_data["src"]["lat"])
    destination_point = (req_data["dst"]["lon"], req_data["dst"]["lat"])
    route = route_planner_app.get_formatted_route(origin_point, destination_point)
    return json.dumps({'route': route, }), 200, {'ContentType': 'application/json'}


def update_traffic_loop(loop_on):
    # TODO move to application.py
    # TODO add logging
    # TODO Check why sometimes it doesn't start
    while True:
        if loop_on.value:
            traffic.get_latest_traffic_info(debug=False)
            print("downloaded new data")
        time.sleep(TRAFFIC_UPDATE_LOOP_INTERVAL)


if __name__ == '__main__':
    # TODO add logging
    # See https://stackoverflow.com/a/39337670
    route_planner_app = app_create.app_create("../data/madrid.gml",
                                               "../data/traffic_measurement_points.csv",
                                               "../test/model_params")

    loop_on = Value('b', True)
    p = Process(target=update_traffic_loop, args=(loop_on,))
    p.start()
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    p.join()

