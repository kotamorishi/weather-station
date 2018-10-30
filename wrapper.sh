#!/bin/bash -ex

BASEDIR=$(dirname "$0")
MAIN=weather.py

pkill -f ${MAIN} || true
nohup python ${BASEDIR}/${MAIN} >${BASEDIR}/log.txt 2>&1 &

echo "Weather started"
