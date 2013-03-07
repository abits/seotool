#!/bin/sh
source venv/bin/activate
venv/bin/uwsgi -s /tmp/uwsgi.sock -w seotool:app --uid 33 --python-autoreload 3
