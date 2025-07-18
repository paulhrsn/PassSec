#!/bin/bash

# Start Flask backend on port 5001
(cd backend && FLASK_APP=run.py FLASK_ENV=development flask run --port=5001) &

# Start React frontend
(cd frontend && npm run dev)
