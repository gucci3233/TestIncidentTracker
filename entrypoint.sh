#!/bin/bash
set -e

echo "Applying Alembic migrations…"
alembic upgrade head

echo "Generating new Alembic revision (if any)…"
alembic revision --autogenerate -m "$(date +%Y_%m_%d_%H_%M_%S)" || true

echo "Applying Alembic migrations…"
alembic upgrade head

exec "$@"
