#!/bin/bash
set -e

echo "Applying database migrations..."
alembic upgrade head
echo "Migrations applied successfully!"
echo "Starting app..."
exec python main.py