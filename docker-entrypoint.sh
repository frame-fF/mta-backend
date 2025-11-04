#!/bin/bash
set -e

echo "Collecting static files..."
uv run manage.py collectstatic --noinput --clear

echo "Starting server..."
exec "$@"