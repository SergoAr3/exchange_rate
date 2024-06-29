#!/bin/bash

make migration

make migrate

exec uvicorn main:app --reload --workers 2

