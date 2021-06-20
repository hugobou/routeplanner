# !/usr/bin/env python

import json
from flask import Flask, request, jsonify


# Rest API using Flask
# https://pythonbasics.org/flask-rest-api/
# https://linuxhint.com/rest_api_python/
# https://flask.palletsprojects.com/en/2.0.x/testing/#testing-json-apis


app = Flask(__name__)

@app.route('/route', methods=['POST'])
def plan_route():
    print(request.get_json())

if __name__ == '__main__':
    app.run(debug=True)