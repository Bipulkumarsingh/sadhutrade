#!/bin/bash
set -e

# start pep8 standards test
#find . -type f -name "*.py" | xargs pylint  # It will find and check every single python file of this project.

gunicorn -b 127.0.0.1:8002 main:app --reload --threads 2 --workers 4 -t 300 -k gevent