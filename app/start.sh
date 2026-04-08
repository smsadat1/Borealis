#!/bin/sh
# start.sh
uvicorn borealis:Borealis --host 0.0.0.0 --port ${PORT:-8000}