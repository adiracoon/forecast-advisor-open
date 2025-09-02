#!/usr/bin/env bash
set -euo pipefail
. /etc/os-release >/dev/null 2>&1 || true
python -m pip install -q --upgrade pip
pip install -q black ruff
black .
ruff check . --fix
git status --porcelain
