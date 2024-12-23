#!/bin/bash
set -a

echo "Checking if the .wttrc file exists..."
if [ ! -f ./.wttrc ]; then
    echo "The .wttrc file does not exist. Please create it before running this script."
    exit 1
fi

echo "Sourcing the .wttrc file..."

source ./.wttrc

USER=$(whoami)
GROUP=$(whoami)
USER_ID=$(id -u)
GROUP_ID=$(id -g)

export USER GROUP USER_ID GROUP_ID

SCRIPT_DIR=$(dirname "$0")
if [ ! -d "$HOME/wtt-database" ]; then
    echo "Creating the $HOME/wtt-database directory..."
    mkdir -p "$HOME/wtt-database"
fi

if [ ! -d "./static/admin" ]; then
    echo "Creating the ./static/* directories..."
    mkdir -p ./static/admin
    mkdir -p ./static/rest_framework
fi

export BACKEND_RUN_SRVR_COMMAND="uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers $WORKERS_COUNT"

docker compose -f docker-compose.yml -p wtt up

echo "Script finished. You can pass --help or -h to see the available options."
exit 0