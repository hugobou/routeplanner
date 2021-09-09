#!/bin/bash

SCRIPT_FOLDER=$(realpath $(dirname ${BASH_SOURCE[0]}))
SRC_FOLDER=${SCRIPT_FOLDER}/../

docker run -it -ti --rm -p 5000:5000 -v ${SRC_FOLDER}:/routeplanner  routeplanner:0.1 bash -c "cd /routeplanner/src && python3 server.py"
