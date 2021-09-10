# !/usr/bin/env python

import json
from flask import Flask, request, jsonify
import time
from multiprocessing import Process, Value
import logging

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
    req_data = request.get_json()
    print(req_data["src"])
    print(req_data["dst"])
    origin_point = (req_data["src"]["lon"], req_data["src"]["lat"])
    destination_point = (req_data["dst"]["lon"], req_data["dst"]["lat"])

    logging.info("Request received: origin_point=%s, destination_point=%s" % (origin_point, destination_point))

    route = route_planner_app.get_formatted_route(origin_point, destination_point)

    logging.info("Request processed")

    return json.dumps({'route': route, }), 200, {'ContentType': 'application/json'}


def update_traffic_loop(loop_on):
    # TODO move to application.py
    while True:
        if loop_on.value:
            logging.info("Starting traffic info update")
            traffic.get_latest_traffic_info(debug=False)
            logging.info("Traffic info update complete")
        time.sleep(TRAFFIC_UPDATE_LOOP_INTERVAL)


if __name__ == '__main__':
    logging.basicConfig(filename='routeplanner.log', level=logging.DEBUG)
    # See https://stackoverflow.com/a/39337670

    logging.info("Starting application")
    route_planner_app = app_create.app_create()

    loop_on = Value('b', True)
    p = Process(target=update_traffic_loop, args=(loop_on,))
    p.start()
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    p.join()

