#!/bin/sh

export DEBUG=1
export FLASK_ENV=development

# run our server locally:
PYTHONPATH=$(pwd):$PYTHONPATH
FLASK_APP=server.endpoints flask run --host=127.0.0.1 --port=8000
