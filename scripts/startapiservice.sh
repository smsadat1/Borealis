#!/bin/sh
# startapiservice.sh
uvicorn api.main:Borealis --host 0.0.0.0 --port ${PORT:-8000}