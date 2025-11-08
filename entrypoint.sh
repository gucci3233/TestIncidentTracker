#!/bin/bash
set -e

# Alembic versions folder
if [ ! -d "/app/alembic/versions" ]; then
  echo "Alembic versions folder not found. Creating..."
  mkdir -p /app/alembic/versions
fi

echo "Applying Alembic migrations…"
alembic upgrade head

echo "Generating new Alembic revision (if any)…"
alembic revision --autogenerate -m "$(date +%Y_%m_%d_%H_%M_%S)" || true

echo "Applying Alembic migrations…"
alembic upgrade head

exec "$@"
