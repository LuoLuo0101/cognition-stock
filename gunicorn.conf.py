# -*- coding: utf-8 -*-

bind = "0.0.0.0:8000"
workers = 4
worker_class = "sanic.worker.GunicornWorker"

# gunicorn -c gunicorn.conf.py manage:app
