#!/bin/bash
set -e 

cd "$(dirname "$0")/backend/seed"

if [ -f "../../.venv/bin/python" ]; then
    PYTHON_CMD="../../.venv/bin/python"
else
    PYTHON_CMD="python3"
fi

$PYTHON_CMD seed_lab_data.py
$PYTHON_CMD seed_quiz_data.py
