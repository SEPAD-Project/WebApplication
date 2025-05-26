@echo off
title CeleryWorker
call .venv\Scripts\activate
python -m celery -A source.celery worker --loglevel=info -P threads
