#!/bin/bash
# Restore PostgreSQL Database
set -e

if [ -z "$1" ]; then
  echo "Usage: ./restore-postgres.sh <path-to-sql.gz>"
  exit 1
fi

FILE=$1
echo "Restoring PostgreSQL from $FILE..."

# Drop and recreate DB (DANGER in production, this is a local DR script)
docker exec -t msrtc-postgres psql -U postgres -c "DROP DATABASE IF EXISTS msrtc;"
docker exec -t msrtc-postgres psql -U postgres -c "CREATE DATABASE msrtc;"

# Restore
gunzip -c $FILE | docker exec -i msrtc-postgres psql -U postgres -d msrtc

echo "Restore complete!"
