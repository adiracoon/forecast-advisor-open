#!/usr/bin/env bash
set -euo pipefail
DC="docker compose -f docker-compose.yml -f docker-compose.dev.yml"

$DC down --remove-orphans
$DC up -d --build

$DC exec api sh -lc '
/opt/venv/bin/python -V &&
/opt/venv/bin/python -m pip show fastapi uvicorn httpx || true
'

for i in {1..45}; do curl -4 -sf http://127.0.0.1:8000/health && break || sleep 1; done

curl -4 -sf http://127.0.0.1:8000/health | cat; echo
curl -4 -sf http://127.0.0.1:8000/ | cat; echo

$DC exec api sh -lc '/opt/venv/bin/python -m pytest -q open/api/test_api.py'
$DC exec api sh -lc '/opt/venv/bin/python -m pytest -q open/api/test_integration.py || true'
