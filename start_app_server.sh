#!/bin/bash
source venv/bin/activate
venv/bin/python -m seotool.fixtures
venv/bin/uwsgi -s /tmp/uwsgi.sock -w seotool:app --uid 1000 --python-autoreload 3
