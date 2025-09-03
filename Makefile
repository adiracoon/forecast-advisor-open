up: ; docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
down: ; docker compose -f docker-compose.yml -f docker-compose.dev.yml down --remove-orphans
test: ; docker compose -f docker-compose.yml -f docker-compose.dev.yml exec api sh -lc '/opt/venv/bin/python -m pytest -q'
smoke: ; scripts/dev_smoke.sh
ci-local: ; python -m pip install -U pip && pip install -r open/requirements.txt -r open/requirements-dev.txt && pytest -q
