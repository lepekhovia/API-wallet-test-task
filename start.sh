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

USER=${USER:-pinuser}
GROUP=${GROUP:-pingroup}
USER_ID=${USER_ID:-1000}
GROUP_ID=${GROUP_ID:-1000}

export USER GROUP USER_ID GROUP_ID

DEBUG=0
FORCE_RECREATE=""
BUILD=0
RUNSERVER=0
SHOWHELP=0


while [[ $# -gt 0 ]]; do
    case "$1" in
        -d|--debug)
            DEBUG=1
            ;;
        -f|--force)
            FORCE_RECREATE="--force-recreate"
            ;;
        -b|--build)
            BUILD=1
            ;;
        -r|--runserver)
            RUNSERVER=1
            ;;
        -h|--help)
            SHOWHELP=1
            ;;
        *)
            echo "Unknown option: $1, use --help to see the available options."
            exit 1
            ;;
    esac
    shift
done

if [ $SHOWHELP -eq 1 ]; then
    echo "Usage: ./dev.sh [OPTIONS]"
    echo "Options:"
    echo "  -d, --debug         Run the server in debug mode."
    echo "  -f, --force         Force recreate the containers."
    echo "  -b, --build         Build the containers."
    echo "  -r, --runserver     Run the backend server."
    echo "  -h, --help          Show this help message."
    exit 0
fi

if [ ! -d "$HOME/pin-database" ]; then
    echo "Creating the $HOME/pin-database directory..."
    mkdir -p $HOME/pin-database
fi

if [ ! -d "./static/admin" ]; then
    echo "Creating the ./static/* directories..."
    mkdir -p ./static/admin
    mkdir -p ./static/rest_framework
fi

if [ $DEBUG -eq 1 ]; then
    export BACKEND_RUN_SRVR_COMMAND="python manage.py runserver 0.0.0.0:8000"
else
    CPU_COUNT=$(nproc)
    export BACKEND_RUN_SRVR_COMMAND="uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers $WORKERS_COUNT"
fi

if [ $BUILD -eq 1 ]; then
    echo "Building the containers..."
    docker compose -f docker-compose.yml -p pin build
fi

if [ $RUNSERVER -eq 1 ]; then
    echo "Running the backend server..."
    docker compose -f docker-compose.yml -p pin up $FORCE_RECREATE
fi

echo "Script finished. You can pass --help or -h to see the available options."
exit 0