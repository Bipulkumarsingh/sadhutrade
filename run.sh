#!/bin/bash
set -e

# start pep8 standards test
#find . -type f -name "*.py" | xargs pylint  # It will find and check every single python file of this project.

# start server
gunicorn app:app -b 127.0.0.1:8006 -w 6 -k gevent --reload