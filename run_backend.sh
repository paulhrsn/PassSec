#!/bin/bash
export FLASK_APP=backend/run.py
export PYTHONPATH=backend
export FLASK_ENV=development
flask run --port=5001
