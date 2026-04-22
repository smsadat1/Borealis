#!/bin/sh
# startauthservice.sh
uvicorn auth.main:Borealis --host 0.0.0.0 --port ${PORT:-7000}