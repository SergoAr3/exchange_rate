#!/bin/bash

make migration

make migrate

exec gunicorn -k uvicorn.workers.UvicornH11Worker main:app --bind 0.0.0.0:8000 --workers 2


