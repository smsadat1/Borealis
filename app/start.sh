#!/bin/sh
# start.sh
uvicorn app.borealis:Borealis --host 0.0.0.0 --port ${PORT:-8000}