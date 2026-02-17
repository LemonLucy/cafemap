#!/bin/bash
# Load environment variables and start server

if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

python3 app_server.py
