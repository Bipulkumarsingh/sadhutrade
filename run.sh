#!/bin/bash
set -e

# start pep8 standards test
#find . -type f -name "*.py" | xargs pylint  # It will find and check every single python file of this project.

uvicorn app:app