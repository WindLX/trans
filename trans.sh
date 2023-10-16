#!/bin/bash

# Function to activate Python virtual environment
activate_venv() {
    if [ -d "$1/.venv" ]; then
        source $1/.venv/bin/activate
    else
        python -m venv $1/.venv --prompt trans
        source $1/.venv/bin/activate
        pip install -r $1/requirements.txt
    fi
}

activate_venv "$1"
python $1/src-python/app.py
deactivate